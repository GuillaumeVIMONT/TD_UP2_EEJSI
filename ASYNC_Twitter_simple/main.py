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
print("This is the simple mode, default paramters is : \n k = 100, \n tau = 3, \n lambda = 1")
# tracking Twitter Stream
tracking = input("1/3 Please enter tracking word (eg CNN) if multi keywords (eg CNN Foxnews): ")

threshold = input("2/3 Please enter threshold for the connected component export (eg 5) : ")
timeout = input("3/3 Please enter duration of the capture in minutes (eg 30): ")
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
    f = open("data/%s_step_reservoir_edges.csv" % time_export, "a")
    # f.write("Source, Destination \n")
    for j in i:
        f.write("%s, %s\n" %j)
    f.close()
    return True

global L, sample_window_stream, global_counter, time_counter, interval_counter
L=0
sample_window_stream = []
global_counter = 0
interval_counter = 0
time_counter = (time.time()*1000)+60000


# k is the size of the reservoir (number of edges floato the reservoir)
k = 100

# tau is the lenght of the window
tau =  3*60000

# lamb is the lenght of strate floato the window
lamb = 1*60000

# rate is the number of strates per window
rate = tau/lamb

# M contain steps floato the window, for each strates we have a edges counter
M = [0] * int(rate)

# init it's a default parameters to configure somes variables when the reservoir strart
init = 0

reservoir = []

def step_reservoir_sampling(edge):
    global init, w_i, M, window_counter, lamb, t_i, dict_test, tau, t
    if init == 0:
        # initialise w_i
        w_i = int(edge[2])+tau
        t_i = int(edge[2])+lamb
        # window counter
        window_counter = 1
        # terminate initialisation
        init+=1
    # check if edge is indide w_i
    if int(edge[2]) < t_i:
        M[-1]+=1
    if int(edge[2]) >= t_i:
        print(M)
        comp = components(reservoir)
        comp1 = sorted(comp, reverse=True)
        xx = comp_edges(comp1)
        now = datetime.datetime.now()
        time_export = now.strftime("%Y_%m_%d_%Hh%M")
        f = open("data/%s_step_reservoir_edges.csv" % (time_export), "a")
        f.write("Source, Target\n")
        f.close()
        index = 0
        for i in comp1:
            if int(i[0]) >= int(threshold):
                write_edge_reservoir(xx[index], time_export)
                index+=1
            else:
                break
        while len(reservoir) > 0 and int(reservoir[0][2]) < w_i-tau:
            # while the previous condition is satisfy do
            del reservoir[0]
        window_counter +=1
        del M[0]
        M.append(1)
        t_i += lamb
        w_i += lamb
    if sum(M) < k:
        reservoir.append(edge)
    else:
        j = random.randint(0, sum(M))
        if j < k:
            if len(reservoir) < k:
                reservoir.append(edge)
            else:
                del reservoir[j]
                reservoir.append(edge)

    return reservoir


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
                    window_reservoir_sampling = step_reservoir_sampling(edge)
        if time.time()*1000 > start + timeout:
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





