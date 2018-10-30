import random
import time
import datetime
import csv


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

global mt, m, mh0, il, ih, i, L, sample, rate, sample, time_init
mt=0
m=[]
mh0=0
# while mt <= int(lamb/tau):
#    m.append(0); mt += 1
mt=0
#i is the index of the windows: 0,1,2,... "il" est l'index de ml et "ih" est l'index de mh
il=0
ih=0
i=0
#L is the length of the Reservoir
L=0
time_init = 0
sample_window_stream = []
def reservoir_sampling_window_stream(edge, k, lamb, tau):
    global m, mh0, L, i, sample_window_stream, time_init, tau_window, lamb_window, il, mt, ih
    if time_init == 0:
        time_init = int(edge[2])
        tau_window = time_init+tau
        lamb_window = time_init+lamb
        while mt <= int(lamb/tau):
            m.append(0); mt += 1
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
        tau_window = tau_window+tau
        write_edge_reservoir(sample_window_stream, i)
        print("il =",il)
        print("ih =",ih)
        print("i =",i)
    if L < k:
        sample_window_stream.append(edge)
        L +=1
    else:
        j = random.randint(0, mh0-m[0])
        if j < k:
            del sample_window_stream[j]
            sample_window_stream.append(edge)
    return sample_window_stream
