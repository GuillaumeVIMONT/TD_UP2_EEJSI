import random
import time
import datetime
import csv
import os.path
# import os
# import sys
def diameter(first):

 #first=comp1[i]
 l=first[2]
 a=l[0]
#print("First point",a)
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
 dist=list(dc.values())
 ma=max(dist)
 for a, i in dc.items():
   if i==ma: last=a
   
# we keep last  !!  
# do it again !!

 a=last
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
 dist=list(dc.values())
 ma=max(dist)
 for a, i in dc.items():
   if i==ma: last=a
 return(max(dist))

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

def write_edge_reservoir(edge_reservoir, window_counter):
    now = datetime.datetime.now()
    f = open("data/%s_window_reservoir_edges_%s.csv" % (now.strftime("%Y_%m_%d"), window_counter), "w")
    header_csv = "Source, Target, Timestamp"
    f.write(header_csv +"\n")
    for i in edge_reservoir:
        a = str(i[0])
        b = str(i[1])
        c = str(i[2])
        e = a + ',' + b + ',' + c
        f.write(e +"\n")
    f.close()

def write_components_reservoir(i, c, n, m_i, n_m, d, keyword, mh0, mhm):
    now = datetime.datetime.now()
    datetime_export = now.strftime("%Y/%m/%d %H:%M:%S")
    if os.path.isfile("data/%s_%s_components.csv" % (now.strftime("%Y_%m_%d"), keyword)):
        w = csv.writer(open("data/%s_%s_components.csv" % (now.strftime("%Y_%m_%d"), keyword), "a"))
        e = (str(datetime_export), str(keyword), str(i), str(c), str(n), str(m_i), str(n_m), str(d), str(mh0), str(mhm))
        w.writerow(e)
    else:
        w = csv.writer(open("data/%s_%s_components.csv" % (now.strftime("%Y_%m_%d"), keyword), "a"))
        header_csv = ("Date", "Keyword", "Window", "Component", "n", "m", "n/m", "Diameter", "mh0", "mh0-m[0]")
        w.writerow(header_csv)
        e = (str(datetime_export), str(keyword), str(i), str(c), str(n), str(m_i), str(n_m), str(d), str(mh0), str(mhm))
        w.writerow(e)
    # w.close()

global mt, m, mh0, il, ih, i, L, rate, sample_window_stream, time_init
mt=0
m=[]
mh0=0
mt=0
#i is the index of the windows: 0,1,2,... "il" est l'index de ml et "ih" est l'index de mh
il=0
ih=0
i=0
#L is the length of the Reservoir
L=0
time_init = 0
sample_window_stream = []
def reservoir_sampling_window_stream(edge, k, lamb, tau, threshold, keyword):
    global m, mh0, L, i, sample_window_stream, time_init, tau_window, lamb_window, il, mt, ih
    if time_init == 0:
        time_init = int(edge[2])
        tau_window = time_init+tau
        lamb_window = time_init+lamb
        rate=int(lamb/tau)
        while mt <= int(lamb/tau):
            m.append(0)
            mt += 1
        mt=0
    else:
        pass
    if int(edge[2]) <= time_init+(il+1)*tau and int(edge[2]) <= lamb_window:
        m[mt+1] += 1
    elif int(edge[2]) <= lamb_window:
        il += 1
        mt += 1
        m[mt+1] = m[mt] + 1
    else:
        pass

    if int(edge[2]) <= tau_window:
        pass 
    else: 
        ih += 1
        if ih == 1:
            del m[rate]
        m.append(mh0-1)
        del m[0]
    if int(edge[2]) > lamb_window:
        lamb_window = lamb_window+lamb
    else:
        pass
    #L on lit les premiers tau's  et on définit ml et m
    # mh0 compte tous les données
    mh0 += 1
    if int(edge[2]) <= tau_window:
        pass
    else:
        m.append(mh0-1)
        del m[0]
    if L < k:
        sample_window_stream.append(edge)
        L +=1
    while int(sample_window_stream[0][2]) < tau_window-tau and L > 0:
        del sample_window_stream[0]
        L -=1
    if int(edge[2]) > tau_window: 
        i += 1
        print(sample_window_stream)
        print("L= ",L)
        print("Numéro réservoir",i)
        print("Nombre de tuple global", mh0)
        print("Nombre de tuple dans la fenêtre", mh0-m[0])
        mhm = mh0-m[0]
        tau_window = tau_window+tau
        comp = components(sample_window_stream)
        comp1=sorted(comp,reverse=True)
        c=0
        for a in comp1:
            n = a[0]
            if int(n) > int(threshold):
                m_i = a[1]
                n_m = n/m_i
                d = diameter(a)
                write_components_reservoir(i, c, n, m_i, n_m, d, keyword, mh0, mhm)
                c+=1            
        write_edge_reservoir(sample_window_stream, i)
    if L < k:
        sample_window_stream.append(edge)
        L +=1
    else:
        j = random.randint(0, mh0-m[0])
        if j < k:
            del sample_window_stream[j]
            sample_window_stream.append(edge)
    return sample_window_stream
