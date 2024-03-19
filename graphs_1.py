import sys; args = sys.argv[1:]
import math
import re
def checkAdd(edge, graph_ds):
    if edge[0] not in graph_ds[4][edge[1]]:
        graph_ds[4][edge[1]].append(edge[0])
    if edge[1] not in graph_ds[4][edge[0]]:
        graph_ds[4][edge[0]].append(edge[1])
    return graph_ds
def checkRemove(edge, graph_ds):
    if edge[0] in graph_ds[4][edge[1]]:
        graph_ds[4][edge[1]].remove(edge[0])
    if edge[1] in graph_ds[4][edge[0]]:
        graph_ds[4][edge[0]].remove(edge[1])
    return graph_ds
def modifyEProps(ePropsdict,graph_ds,n_e_w_s,vertex,reward,direction,management_type):
    edges = []
    if 'N' in n_e_w_s:
        if graph_ds[1]>vertex-graph_ds[2]>=0:
            edges.append((vertex,vertex-graph_ds[2]))
    if 'E' in n_e_w_s:
        if vertex%graph_ds[2]!=graph_ds[2]-1 and 0<=vertex+1<graph_ds[1]:
            edges.append((vertex,vertex+1))
    if 'W' in n_e_w_s:
        if vertex%graph_ds[2]!=0 and 0<=vertex-1<graph_ds[1]:
            edges.append((vertex,vertex-1))
    if 'S' in n_e_w_s:
        if vertex+graph_ds[2]<graph_ds[1]:
            edges.append((vertex,vertex+graph_ds[2]))
    if direction == '=':
        
        to_add = []
        for edge in edges:
            to_add.append((edge[1],edge[0]))
        edges+=to_add
    
    if management_type=='~':
        for edge in edges:
            if edge in ePropsdict:
                del ePropsdict[edge]
                graph_ds = checkRemove(edge,graph_ds)
            else:
                if reward:
                    ePropsdict[edge] = {'rwd':reward}
                    graph_ds = checkAdd(edge,graph_ds)
                else:
                    ePropsdict[edge] = {}
                    graph_ds = checkAdd(edge,graph_ds)
    elif management_type=='!':
        for edge in edges:
            if edge in ePropsdict:
                del ePropsdict[edge]
                graph_ds = checkRemove(edge,graph_ds)
    elif management_type=='+':
        
        for edge in edges:
            if edge not in ePropsdict:
                if reward:
                    ePropsdict[edge] = {'rwd':reward}
                    graph_ds = checkAdd(edge,graph_ds)
                else:
                    ePropsdict[edge] = {}
                    graph_ds = checkAdd(edge,graph_ds)
    elif management_type=='*':
        for edge in edges:
            if edge not in ePropsdict:
                if reward:
                    ePropsdict[edge] = {'rwd':reward}
                    graph_ds = checkAdd(edge,graph_ds)
                else:
                    ePropsdict[edge] = {}
                    graph_ds = checkAdd(edge,graph_ds)
            else:
                if reward:
                    ePropsdict[edge] = {'rwd':reward}
                else:
                    ePropsdict[edge] = {}
    elif management_type=='@':
        for edge in edges:
            if edge in ePropsdict:
                if reward:
                    ePropsdict[edge] = {'rwd':reward}
                else:
                    ePropsdict[edge] = {}

    return ePropsdict,graph_ds

def form_one(ePropsdict,graph_ds,directive):
    return ePropsdict,graph_ds
def form_two(ePropsdict,graph_ds,directive):
    size_list = [i for i in range(int(graph_ds[1]))]

    mngmnt = {'!','+','*','~','@'}
    directionality = {'~','='}
    reward = ''
    eslc = directive
    if 'R' in eslc:
                 if r:=re.search('R\d+',eslc):
                         reward = int(r.group()[1:])
                 else:
                       reward = graph_ds[3]
    management_type = '~'
    if eslc[0] in mngmnt:
        management_type = eslc[0]
        eslc = eslc[1:]
    for i,c in enumerate(eslc):
        if c in 'NEWS':
            idx = i
            break
    esplits = eslc[:idx].split(',')
    # stop = len(eslc)
    for i,c in enumerate(eslc[idx:]):
        if c not in 'NEWS':
            stop = i+idx
            break
    n_e_w_s = eslc[idx:stop]
    vertices = []
    # print(eslc)
    for esplit in esplits:
                if esplit.count(':')==0:
                    vertices.append(size_list[int(esplit)])
                    
                if esplit.count(':')==1:
                    if esplit == ':':
                        
                        vertices+=size_list
                    elif esplit[-1]==':':
                        
                        vertices+=size_list[int(esplit[:esplit.index(':')]):]
                    elif esplit[0] == ':':
                        
                        vertices+=size_list[:int(esplit[esplit.index(':')+1:])]
                    else:
                        
                        vertices+=size_list[size_list[int(esplit[:esplit.index(':')])]:int(esplit[esplit.index(':')+1:])]
                if esplit.count(':')==2:
                    esplit_splits = esplit.split(':')
                    if not any(esplit_splits):
                         
                         vertices+=size_list
                    elif(esplit_splits[0] =='' and esplit_splits[2]==''):
                         
                         vertices+=size_list[:int(esplit_splits[1]):]
                    elif(esplit_splits[1] =='' and esplit_splits[2]==''):
                        
                        vertices+=size_list[int(esplit_splits[0])::]
                    elif(esplit_splits[1] =='' and esplit_splits[0]==''):
                        
                        vertices+=size_list[::int(esplit_splits[2])]
                    elif(esplit_splits[0]==''):
                        
                        vertices+=size_list[:int(esplit_splits[1]):int(esplit_splits[2])]
                    elif(esplit_splits[1]==''):
                         
                         vertices+=size_list[int(esplit_splits[0])::int(esplit_splits[2])]
                    elif(esplit_splits[2]==''):
                        
                        vertices+=size_list[int(esplit_splits[0]):int(esplit_splits[1]):]
                    else:
                        
                        vertices+=size_list[int(esplit_splits[0]):int(esplit_splits[1]):int(esplit_splits[2])]
    for vertex in vertices:
        ePropsdict,graph_ds = modifyEProps(ePropsdict,graph_ds,n_e_w_s,vertex,reward,eslc[stop],management_type)

                
    return ePropsdict,graph_ds
def grfParse(lstArgs):
    #regex
    #/(GG|GN|G)\d+/
    numberString = '0123456789'
    regex_1 = '(G|GG|GN)\d+'
    regex_2 = 'W\d+'
    regex_3 = 'R\d+'
    graph_ds = []
    
    graph_directive = lstArgs[0]
    # print(graph_directive)
    if(s:=re.search(regex_1,graph_directive)):
        
        for i,c in enumerate(s.group()):
            if c in numberString:
                if graph_directive.count('N')==1:
                    graph_ds+=['N',int(s.group()[i:])]
                else:
                    graph_ds+=['G',int(s.group()[i:])]
                break

    # print(graph_ds)
    if(w:=re.search(regex_2,graph_directive)):
        if w.group()[1:] == '0':
            # graph_ds[0] = 'N'
            graph_ds.append(0)
        else:
            graph_ds.append(int(w.group()[1:]))
    else:
        height,width=0,0
        for i in range(1,int(math.sqrt(graph_ds[1])+1)):
            if graph_ds[1]%i==0:
                height=i
                width=graph_ds[1]//i
        graph_ds.append(width)
    if(r:=re.search(regex_3,graph_directive)):
        graph_ds.append(int(r.group()[1:]))
    else:
        graph_ds.append(12)
    # print(graph_ds)
    ePropsdict={}

    size_list = [i for i in range(int(graph_ds[1]))]
    graph_nbrs = [[] for i in range(int(graph_ds[1]))]
    if graph_ds[2]!=0 and graph_ds[0]!='N':

        
        for i,nbr in enumerate(graph_nbrs):
            if i%graph_ds[2]!=0:
                graph_nbrs[i].append(i-1)
                ePropsdict[(i,i-1)] = {}
            if i%graph_ds[2]!=graph_ds[2]-1:
                graph_nbrs[i].append(i+1)
                ePropsdict[(i,i+1)] = {}
            if i//graph_ds[2]!=0:
                graph_nbrs[i].append(i-graph_ds[2])
                ePropsdict[(i,i-graph_ds[2])] = {}
            if i//graph_ds[2]!=(graph_ds[1]//graph_ds[2])-1:
                graph_nbrs[i].append(i+graph_ds[2])
                ePropsdict[(i,i+graph_ds[2])] = {}
            
    graph_ds.append(graph_nbrs)
    graph_ds.append([])
    vPropsDict = {}
    blocked_set = set()
    for directive in lstArgs[1:]:
        reward = ''
        newly_added = []
        ls = []
        blocked_list = []
        # old_blocked_set = set(blocked_list)
        if 'E' in directive:
            
            eslc = directive[1:]
            # print(eslc)
            if 'N' in eslc or 'E' in eslc or 'W' in eslc or 'S' in eslc:
                ePropsdict,graph_ds = form_two(ePropsdict,graph_ds,eslc)
            
            else:
                ePropsdict,graph_ds = form_one(ePropsdict,graph_ds,eslc)
        if directive[0] == 'V':
            
            vslcs = directive[1:]
            # print(vslcs)
            splits = vslcs.split(',')
            # print(splits)
            for vsplit in splits:
                ls = []
                if 'R' in vsplit:
                    ls.append(vsplit.index('R'))
                    if r:=re.search(regex_3,vsplit):
                         reward = int(r.group()[1:])
                    else:
                       reward = graph_ds[3]
                    
                if 'B' in vsplit:
                    ls.append(vsplit.index('B'))
                if ls:
                     vslc= vsplit[:min(ls)]
                else:
                    vslc = vsplit[:]
                if vslc.count(':')==0:
                    graph_ds[-1].append(size_list[int(vslc)])
                    newly_added+=[size_list[int(vslc)]]
                    if 'B' in directive:
                        blocked_list+=[size_list[int(vslc)]]
                if vslc.count(':')==1:
                    if vslc == ':':
                        if 'B' in directive:
                            blocked_list+=size_list
                        graph_ds[-1].append(size_list)
                        newly_added+=size_list
                    elif vslc[-1]==':':
                        if 'B' in directive:
                            blocked_list+=size_list[int(vslc[:vslc.index(':')]):]
                        graph_ds[-1].append(size_list[int(vslc[:vslc.index(':')]):])
                        newly_added+=size_list[int(vslc[:vslc.index(':')]):]
                    elif vslc[0] == ':':
                        if 'B' in directive:
                            blocked_list+=size_list[:int(vslc[vslc.index(':')+1:])]
                        graph_ds[-1].append(size_list[:int(vslc[vslc.index(':')+1:])])
                        newly_added+=size_list[:int(vslc[vslc.index(':')+1:])]
                    else:
                        if 'B' in directive:
                            blocked_list+=size_list[size_list[int(vslc[:vslc.index(':')])]:int(vslc[vslc.index(':')+1:])]
                        graph_ds[-1].append(size_list[size_list[int(vslc[:vslc.index(':')])]:int(vslc[vslc.index(':')+1:])])
                        newly_added+=size_list[size_list[int(vslc[:vslc.index(':')])]:int(vslc[vslc.index(':')+1:])]
                if vslc.count(':')==2:
                    vslc_splits = vslc.split(':')
                    if not any(vslc_splits):
                         if 'B' in directive:
                             blocked_list+=size_list
                         graph_ds[-1].append(size_list)
                         newly_added+=size_list
                    elif(vslc_splits[0] =='' and vslc_splits[2]==''):
                         if 'B' in directive:
                             blocked_list+=size_list[:int(vslc_splits[1]):]
                         graph_ds[-1].append(size_list[:int(vslc_splits[1]):])
                         newly_added+=size_list[:int(vslc_splits[1]):]
                    elif(vslc_splits[1] =='' and vslc_splits[2]==''):
                        if 'B' in directive:
                            blocked_list+=size_list[int(vslc_splits[0])::]
                        graph_ds[-1].append(size_list[int(vslc_splits[0])::])
                        newly_added+=size_list[int(vslc_splits[0])::]
                    elif(vslc_splits[1] =='' and vslc_splits[0]==''):
                        if 'B' in directive:
                            blocked_list+=size_list[::int(vslc_splits[2])]
                        graph_ds[-1].append(size_list[::int(vslc_splits[2])])
                        newly_added+=size_list[::int(vslc_splits[2])]
                    elif(vslc_splits[0]==''):
                        if 'B' in directive:
                            blocked_list+=size_list[:int(vslc_splits[1]):int(vslc_splits[2])]
                        graph_ds[-1].append(size_list[:int(vslc_splits[1]):int(vslc_splits[2])])
                        newly_added+=size_list[:int(vslc_splits[1]):int(vslc_splits[2])]
                    elif(vslc_splits[1]==''):
                         if 'B' in directive:
                            blocked_list+=size_list[int(vslc_splits[0])::int(vslc_splits[2])]
                         graph_ds[-1].append(size_list[int(vslc_splits[0])::int(vslc_splits[2])])
                         newly_added+=size_list[int(vslc_splits[0])::int(vslc_splits[2])]
                    elif(vslc_splits[2]==''):
                        if 'B' in directive:
                            blocked_list+=size_list[int(vslc_splits[0]):int(vslc_splits[1]):]
                        graph_ds[-1].append(size_list[int(vslc_splits[0]):int(vslc_splits[1]):])
                        newly_added+=size_list[int(vslc_splits[0]):int(vslc_splits[1]):]
                    else:
                        if 'B' in directive:
                            blocked_list+=size_list[int(vslc_splits[0]):int(vslc_splits[1]):int(vslc_splits[2])]
                        graph_ds[-1].append(size_list[int(vslc_splits[0]):int(vslc_splits[1]):int(vslc_splits[2])])
                        newly_added+=size_list[int(vslc_splits[0]):int(vslc_splits[1]):int(vslc_splits[2])]
        # blocked_set = set(blocked_list)
        if reward !='':
            
            for node in newly_added:
                # print(node)
                vPropsDict[node] = {'rwd':reward}
        to_remove = []
        for b in blocked_set:
            if b in blocked_list:
                to_remove.append(b)
        for r in to_remove:
            blocked_set.remove(r)
            blocked_list.remove(r)
        blocked_set = blocked_set.union(set(blocked_list))
        to_remove = []
        for b in blocked_set:
            for key in ePropsdict:
                if b in key:
                    to_remove.append(key)
        for r in to_remove:
            if r in ePropsdict:
                del ePropsdict[r]
        # blocked_list  = list(blocked_set)
    # blocked_set = set(blocked_list)
    # print(blocked_set)
    # print(blocked_list)
    for idx in blocked_set:
        # if blocked_list.count(idx)%2==0:
        #     continue
        for i,nbr_array in enumerate(graph_ds[-2]):
            if i==idx:
                # print(nbr_array)
                to_remove = []
                for n in nbr_array:
                    # print(n)
                    if n not in blocked_set:
                        to_remove.append(n)
                        # graph_ds[-2][i].remove(n)
                for r in to_remove:
                    graph_ds[-2][i].remove(r)
            if idx in nbr_array and i not in blocked_set:
                graph_ds[-2][i].remove(idx)
    
    
            
            
            
            
    # print(graph_ds[4][21])
    # print(ePropsdict)
    # print(graph_ds)
    # print(graph_nbrs)
    return graph_ds, graph_nbrs, vPropsDict,ePropsdict
    # if graph_directive[1]=='N':
    #     graph_ds+=['N',int(graph_directive[2])]
    # elif(graph_directive[1]=='G'):
    #    graph_ds+=['G',int(graph_directive[2])]
    # else:
    #     graph_ds+=['G',int(graph_directive[1])]
    # if 'W' in graph_directive:
    #     width = int(graph_directive[graph_directive.index('W')+1])
    #     if width==0:
    #         graph_ds[0] = 'N'
    #         height = -1
    #     else:
    #         height = graph_ds[1]//width
    # else:
    #     height,width=0,0
    #     for i in range(1,int(math.sqrt(graph_ds[1])+1)):
    #         if graph_ds[1]%i==0:
    #             height=i
    #             width=graph_ds[1]//i
    # graph_ds+=[height,width]
    # if 'R' in graph_directive:
    #     reward = int(graph_directive[graph_directive.index('R')+1:])
    # else:
    #     reward = 12
    # graph_ds+=[reward]
    # return graph_ds

def grfSize(graph):
    # print(graph[1])
    return graph[0][1]

def grfNbrs(graph,v):
    nbrs = graph[0][-2]

    return nbrs[v]

def grfGProps(graph):
    # print(graph)
    if graph[0][0] =='N' :
        return {'rwd':graph[0][-3]}
    return {'width':graph[0][-4],'rwd':graph[0][-3]}

def grfVProps(graph,v):
    
    if v in graph[2]:
        return graph[2][v]
    return {}

def grfEProps(graph,v1,v2):
    if (v1,v2) in graph[3]:
        return graph[3][(v1,v2)]
    return {}
def grfStrEdges(graph):
    if graph[0][0] == 'N':
        return ''
    if graph[0][2] ==0:
        return ''
    symbol_dict = {'E':'E','W':'W','N':'N','S':'S','EN':'L','WN':'J','WSN':'<','WS':'7','EWN':'^','EWSN':'+','EWS':'v','ES':'r','ESN':'>','':'.','EW':'-','SN':'|'}
    nbrs = graph[0][-2]
    # print(nbrs)
    representation = ''
    for i,nbr in enumerate(nbrs):
        # print(nbr)
        symbol =''
        if i+1 in nbr:
            # print('E added')
            symbol+='E'
        if i-1 in nbr:
            symbol+='W'
        if i+graph[0][2] in nbr:
            # print('S added')
            symbol+='S'
        if i-graph[0][2] in nbr:
            symbol+='N'
        representation+=symbol_dict[symbol]
    
    # print(0 + graph[0][2] in [1,5])
    # print(graph[0][-2])
    return representation

def grfStrProps(graph):
    properties = grfGProps(graph)
    # print(properties)
    res = ''
    if 'width' in properties:
        res+=f"rwd: {properties['rwd']}, width: {properties['width']}"

    else:
        res+=f"rwd: {properties['rwd']}"
    for key in graph[2]:
        res+='\n'+f"{key}:rwd:{graph[2][key]['rwd']}"
    for key in graph[3]:
        if 'rwd' in graph[3][key]:
            res+='\n'+f"({key[0]},{key[1]}):rwd:{graph[3][key]['rwd']}"
    return res

def main():
    graph = grfParse(args)
    # print(graph)
    size = grfSize(graph)
    properties = grfGProps(graph)
    representation  = grfStrEdges(graph)
    # print(grfNbrs(graph,1))
    if representation:
        print('\n'.join(representation[i:i+graph[0][2]] for i in range(0,graph[0][1],graph[0][2])))
    print(grfStrProps(graph))
    
if __name__ == '__main__': main()
#Shaurya Jain, pd 3, 2025