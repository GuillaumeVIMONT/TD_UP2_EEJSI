import random
import time
global edges_in_stream
edges_in_stream = []
global edges_out_stream
edges_out_stream = []
global components_edges_stream
components_edges_stream = []
global components_nodes_stream
components_nodes_stream = []

#Assume the edge_out is in one of the components
#Assume lists are coherent


def suppress_stream(edges_out_stream):
    global components_edges_stream
    global components_nodes_stream
    global bchange_stream, change_stream
    #Assume the edge_out is in one of the components
    #Assume lists are coherent
    a=edges_out_stream[0]
    b=edges_out_stream[1]
    t=edges_out_stream[2]
    change_stream=0
    bchange_stream=0

    # a=node origin  b=node extremity

    # which component is a in ?  i is the index of the component

    for ln in components_nodes_stream:
            if a in ln:
                    i=components_nodes_stream.index(ln)
                    break

    #print ("Component=", i)

    # Do we disconnect Component i ?

    le=components_edges_stream[i]

    # is the component a single edge? remove the components
    if len(le)==1:
            components_edges_stream.pop(i)
            components_nodes_stream.pop(i)
            change_stream=-i
            bchange_stream=-1
            

    # is the set component single? remove the edge
    elif len(set(le))==1:
            components_edges_stream[i].remove((a,b,t))
            bchange_stream=0
            
            
    # is the component a self-loop? maybe remove the node (check=0 ), remove  the edge
    elif a==b:
            components_edges_stream[i].remove((a,b,t))
            check=0
            bchange_stream=0
            for e in le:
                    if e[0]==a or e[1]==a:
                             check=1
            if check==0:
                    components_nodes_stream[i].remove(a)
                    
                    
    else:   
    # print ("Component edges =", le)
     le.remove((a,b,t))
    # print ("Component =", le)
     m=len(le)
     ln=components_nodes_stream[i]

    # print ("Component nodes =", ln)

    #le is the list of edges,  m the size of le, ln the list of nodes
    #We expand A={a}, the new elements: we reach B from A, and recompute the new elements
    #U1 is the previous set, U is the new set. We stop when A is empty
     A=set([a])
     U=A
     U1=A
     while A:
      for a in A:
            B=set([])
            for e in le:
                            if e[0]==a:
                             B.add(e[1])
                            if e[1]==a:
                             B.add(e[0])
    #       print ("Set B =", B,a)
            U=U.union(B)
    #       print (" U1=", U1)
    #       print (" U=", U)
            
      A=U-U1
      U1=U
    #  print ("Difference A=", A)

     nu=len(U)
     n=len(components_nodes_stream[i])
    # we can decide if we reach b, i.e. if we split b in U (or n=nu)
    # le is one connected component, a component and a single point, or two components

    # print ("nu et n", nu,n)
     check=0
     check1=0
     if b in U:
    #       print("one component",nu)
            components_edges_stream[i]=le
            
    #  a component and a single point a (nu=1) or b (nu=n-1) to be checked
     elif nu==1 or nu==n-1:
    #       print("one component after removing maybe one node and one edge",nu,n)
            components_edges_stream[i]=le
            if nu==1:
                    check=0
                    for e in le:
                            if e[0]==a or e[1]==a:
                             check=1
                    if check==0:
                            components_nodes_stream[i].remove(a)
                    
    #               print("case nu==1")
            if nu==n-1:
                    check1=0
                    for e in le:
                            if e[0]==b or e[1]==b:
                             check1=1
                    if check1==0:
                            components_nodes_stream[i].remove(b)
    #       print("case nu>1,list=",components_nodes_stream[i])
    #               print("case nu>1",check1)
            if (check1==1 and check==1) or (check1==1 and nu!=1) or (check==1 and nu!=n-1):
    #               print("case of 2 components")           
                    NU=set(components_nodes_stream[i])-U
                    components_nodes_stream[i]=list(NU)
                    components_nodes_stream.insert_stream(i, list(U))  
    #update the edges  NE and E
                    NE=[]
                    for e in le:
                       for node in NU:
                         if e[0]==node or e[1]==node:
                            NE.append(e)
                            break
                    NF=NE[:]
                    E=[j for j in le if not j in NF or NF.remove(j)]
                    components_edges_stream[i]=NE
                    components_edges_stream.insert_stream(i, E)
                    change_stream=i
                    bchange_stream=1  
                    
    #       print("Node components case 1b",components_nodes_stream)       
     else:
    #       print("two components",nu)
    #update the nodes  NU and U
            NU=set(components_nodes_stream[i])-U
            components_nodes_stream[i]=list(NU)
            components_nodes_stream.insert_stream(i, list(U))  
    #update the edges  NE and E
            NE=[]
            for e in le:
                for node in NU:
                         if e[0]==node or e[1]==node:
                            NE.append(e)
                            break
            NF=NE[:]
            E=[j for j in le if not j in NF or NF.remove(j)]
            components_edges_stream[i]=NE
            components_edges_stream.insert_stream(i, E)
            change_stream=i
            bchange_stream=1
    return components_edges_stream

# print("Node components",components_nodes_stream)
# print("Edge components",components_edges_stream)
def insert_stream(edges_in_stream):
    global components_edges_stream
    global components_nodes_stream
    global change_stream, bchange_stream

    #List of 3 main cases

    insert_stream=0
    merge_stream=0
    smerge_stream=0
    change_stream=0
    bchange_stream=0

    a=edges_in_stream[0]
    b=edges_in_stream[1]
    t=edges_in_stream[2]
    # a=node origin  b=node extremity
    # case 1  origin or extremity (not both) in the components_nodes_stream:  smerge_stream=1
    # case 2  both in the components_nodes_stream   merge_stream=1
    # case 3  none in the components_nodes_stream: insert_stream=1

    # looking for case 1 or 2
    for ln in components_nodes_stream:
        if a in ln and b  in ln:
    # case 2 detected with i=j
            i=components_nodes_stream.index(ln)
            j=i
            merge_stream=1
            #print ("merge_stream j=",j)
            break
            
        elif a in ln and b not in ln:
            i=components_nodes_stream.index(ln)
    # case 1a check for case 2  a is before b   
            for ln1 in components_nodes_stream:
                if b in ln1:
    # case 2 detected   
                    j=components_nodes_stream.index(ln1)
                    #print ("merge_stream j=",j)
                    merge_stream=1
                    break
            
    #       break  ????
    # case 1a
            if merge_stream==0:
                ln.append(b)
                components_edges_stream[i].append((a,b,t))
                #print ("smerge_stream")
                smerge_stream=1
            break
            
        elif a not in ln and b  in ln:
    # case 1b
            i=components_nodes_stream.index(ln)
    # case 1a check for case 2      b is before a 
            for ln1 in components_nodes_stream:
                if a in ln1:
    # case 2 detected: inverse i and j
                    
                    j=components_nodes_stream.index(ln1)
                    #print ("merge_stream j=",j)
                    merge_stream=1
                    break
            
    # case 1b
            if merge_stream==0:
                ln.append(a)
                components_edges_stream[i].append((a,b,t))
                #print ("smerge_stream")
                smerge_stream=1
            break
            
        else:
            continue
            
    #  case 3 detected :  will have to insert_stream new lists     
    if merge_stream==0 and smerge_stream==0:
        insert_stream=1
        change_stream=len(components_nodes_stream)
        bchange_stream=1
        #print ("insert_stream")
        
    #  dealing wih case 3 detected :  new  items in the lists   
    if insert_stream==1:
            if a==b:
                components_nodes_stream.append([a])
            else:
                components_nodes_stream.append([a,b])
            components_edges_stream.append([(a,b,t)])
        
    #  dealing with case 2:  merge_stream elements i and j if they are different   i<j
    if merge_stream==1:
        if i!=j:
            #print ("i=", i)
            #print ("j=", j)
            change_stream=-j
            bchange_stream=-1
            components_nodes_stream[i]=components_nodes_stream[i]+components_nodes_stream[j]
            components_nodes_stream.pop(j)
            components_edges_stream[i]=components_edges_stream[i]+components_edges_stream[j]
            components_edges_stream[i].append((a,b,t))
            components_edges_stream.pop(j)
        elif i==j:
    #  dealing with case 2:  merge_stream edges only   
            components_edges_stream[i].append((a,b,t))
            bchange_stream=0
    return components_edges_stream

sample_window_stream = []

def reservoir_sampling_window_stream(edge, k, window_sliding):
    a=edge[0]
    b=edge[1]
    t=edge[2]
    edge=(a,b,t)
    current_milli_time = int(t)
    #current_milli_time = lambda: int(round(time.time() * 1000))
    last_15 = current_milli_time-window_sliding
    for i in sample_window_stream:
        if current_milli_time < last_15:
            suppress_stream((i))
            del sample_window_stream[i]
        else:
            continue
    for a, b in enumerate([edge]):
        if len(sample_window_stream) < k:
            insert_stream((edge))
            sample_window_stream.append((edge))
        else:
            i = random.randint(0, k)
            if i < k:
                edge_out = sample_window_stream[i]
                suppress_stream(edge_out)
                del sample_window_stream[i]
                sample_window_stream.append((edge))
                insert_stream((edge))
    return components_edges_stream

