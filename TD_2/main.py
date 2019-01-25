from peony import EventStream, PeonyClient, event_handler, events
import asyncio
import json
from generate_graph import create_graph
import random
from config import TwitterAuth
import datetime
import sys
import time
# all the event handlers are included in peony.events

# Get date
now = datetime.datetime.now()

print("Before start Twitter capture we need some informations")
# Reservoir Sampling Size
window_k = input("1/4 Please enter number of edges in the reservoir (eg 200): ")
window_k = int(window_k)

# tracking Twitter Stream
tracking = input("2/4 Please enter tracking word (eg CNN) if multi keywords (eg CNN Foxnews): ")

threshold = input("3/4 Please enter threshold for the connected component export (eg 5) : ")
timeout = input("4/4 Please enter duration of the capture in minutes (eg 30): ")
timeout = int(timeout)*60000
start = int(round(time.time() * 1000))

def components(edges):
  global d
  d={}
  n=0
  for e in edges:
     a=e[0]
     b=e[1]
     if a in d.keys(): d[a].add(b)
     else: d[a]=set([b])
     if b in d.keys(): d[b].add(a)
     else: d[b]=set([a])
     
     
  #print ("Dict=", d, len(d))
  n=len(d)
  m=0
  #Breadth-first search from first point, first component
  a=list(d.keys())[0]

  #dc keeps b:i  if i is the length of the shortest path from a to b in the first component
  dc={}
  dc[a]=0
  for b in d[a]: 
    if b in dc.keys(): pass
    else: dc[b]=1

  #Initialize S ans S1, Start iterating
  S=d[a]
  comp=[]
  S1=set([a])
  S=S.union(S1)
  #print("S=",S)
  while S > S1:
      S1=S
      for u in S:
         S=S.union(d[u])
         for v in d[u]:
           if v in dc.keys(): dc[v]=min(dc[v],dc[u]+1)
           else: dc[v]=dc[u]+1
  for u in S:
       m=m+len(d[u])

  comp.append((len(S),int(m/2),list(S)))
    
  #print("Component",comp)

  ST=S
    
  #print("ST=",ST)

  #The other components: origin must be outside ST, same treatment
  i=1
  while i<len(d):
   m=0
   while  list(d.keys())[i] not in ST:
    a=list(d.keys())[i]
    S=d[a]
    S1=set([a])
    S=S.union(S1)
    while S > S1:
      S1=S
      for u in S:
         S=S.union(d[u])
    for u in S:
       m=m+len(d[u])
    comp.append((len(S),int(m/2),list(S)))
    ST=ST.union(S)  
   i+=1     
  return comp


def comp_edges(comp1):
 compedges=[]
 j0=0
 while j0<len(comp1):
   l1 = comp1[j0][2]
   j=0
   cp=[]
   while j <len(l1):
     a=l1[j]
     j1=0
     while j1< len(d[l1[j]]):
      f=(a,list(d[l1[j]])[j1])
      cp.append(f)
      j1 +=1
     j +=1
   j0 +=1
   compedges.append(cp)
 return compedges

def write_edge_reservoir(i, time_export):
    f = open("data/%s_window_reservoir_edges.csv" % (time_export), "a")
    # f.write("Source, Destination \n")
    for j in i:
        try:
            f.write("%s, %s\n" %j)
        except:
            pass
    f.close()

global L, sample_window_stream, global_counter, time_counter, interval_counter
L=0
sample_window_stream = []
global_counter = 0
interval_counter = 0
time_counter = (time.time()*1000)+60000
def reservoir_sampling_window_stream(edge, k):
    global L, sample_window_stream
    L+=1
    if L < k:
        sample_window_stream.append(edge)
    else:
        j = random.randint(0, L)
        if j < k-1:
           sample_window_stream[j] = edge
    return sample_window_stream


async def consume(queue):
    while True:
        # wait for an item from the producer
        item = await queue.get()
        twitter_edges_graph = create_graph(item)
        queue.task_done()
        global time_counter, global_counter, interval_counter
        if len(twitter_edges_graph) > 0:
            # process the item
            # print('consuming {}...'.format(twitter_edges_graph))
            # Notify the queue that the item has been processed
            for edge in twitter_edges_graph:
                if tracking[0] in edge[1].lower():
                    pass
                else:
                    global_counter+=1
                    interval_counter+=1
                    window_reservoir_sampling = reservoir_sampling_window_stream(edge, window_k)
        if time.time()*1000 > time_counter:
            print("nombre de tuples global", global_counter)
            print("nombre de tuples intervalle", interval_counter)
            interval_counter = 0
            time_counter+=60000
        if time.time()*1000 > start + timeout:
            #print("Nombre de tuple global", L)
            print("Taille du réservoir", len(window_reservoir_sampling)+1)
            comp = components(window_reservoir_sampling)
            comp1 = sorted(comp, reverse=True)
            xx = comp_edges(comp1)
            now = datetime.datetime.now()
            time_export = now.strftime("%Y_%m_%d_%Hh%M")
            f = open("data/%s_window_reservoir_edges.csv" % (time_export), "a")
            f.write("Source, Target\n")
            f.close()
            index = 0
            for i in comp1:
                if int(i[0]) >= int(threshold):
                    try:
                        write_edge_reservoir(xx[index], time_export)
                    except:
                        pass
                    index+=1
                else:
                    break
            sys.exit('Capture terminated')



class Client(PeonyClient):
    pass

# every class inheriting from `PeonyClient` or `BasePeonyClient` has
# an event_stream function that can be used on an `EventStream`
@Client.event_stream
class UserStream(EventStream):

    def stream_request(self):
        """
            The stream_request method returns the request
            that will be used by the stream
        """
        return self.stream.statuses.filter.post(track=tracking)


    # the on_connect event is triggered on connection to an user stream
    # https://dev.twitter.com/streaming/overview/messages-types#friends-lists-friends
    @events.on_connect.handler
    def connection(self, data):
        consumer = asyncio.ensure_future(consume(queue))
        print("Connected to stream!")

    # the on_tweet event is triggered when a tweet seems to be sent on
    # the stream, by default retweets are included
    @events.on_tweet.handler
    async def tweet(self, data):
        await queue.put(data)
        #print("producing")


if __name__ == '__main__':
    queue = asyncio.Queue()
    client = Client(consumer_key=TwitterAuth.consumer_key,
                     consumer_secret=TwitterAuth.consumer_secret,
                     access_token=TwitterAuth.access_token,
                     access_token_secret=TwitterAuth.access_token_secret)
    client.run()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(client.run())
    # loop.close()





