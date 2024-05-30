import sys; args = sys.argv[1:]
import math
import re
def parseCommaSplices(esplits,graph_ds):
    size_list  = [i for i in range(int(graph_ds[1]))]
    vertices = []
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
    return vertices
def checkAdd(edge, graph_ds,direction):
    if edge[1] not in graph_ds[4][edge[0]]:
        graph_ds[4][edge[0]].append(edge[1])
    if direction == '=':
        if edge[0] not in graph_ds[4][edge[1]]:
            graph_ds[4][edge[1]].append(edge[0])
    
    return graph_ds
def checkRemove(edge, graph_ds,ePropsdict,direction):
    if edge[1] in graph_ds[4][edge[0]] and (edge[0],edge[1]) not in ePropsdict:
        graph_ds[4][edge[0]].remove(edge[1])
    if direction == '=':
        if edge[0] in graph_ds[4][edge[1]] and (edge[1],edge[0]) not in ePropsdict:
            graph_ds[4][edge[1]].remove(edge[0])
    
    
    return graph_ds
def modifyEPropsFormOne(ePropsdict,graph_ds,edges,reward,direction,management_type):
    
    if management_type=='~':
        
        for edge in set(edges):
            if edge in ePropsdict:
                del ePropsdict[edge]
                graph_ds = checkRemove(edge,graph_ds,ePropsdict,direction)
            else:
                if reward != '':
                    ePropsdict[edge] = {'rwd':reward}
                    graph_ds = checkAdd(edge,graph_ds,direction)
                else:
                   
                    ePropsdict[edge] = {}
                    graph_ds = checkAdd(edge,graph_ds,direction)
    elif management_type=='!':
        for edge in set(edges):
            if edge in ePropsdict:
                del ePropsdict[edge]
                graph_ds = checkRemove(edge,graph_ds,ePropsdict,direction)
    elif management_type=='+':
        
        for edge in set(edges):
            if edge not in ePropsdict:
                if reward != '':
                    ePropsdict[edge] = {'rwd':reward}
                    graph_ds = checkAdd(edge,graph_ds,direction)
                else:
                    ePropsdict[edge] = {}
                    graph_ds = checkAdd(edge,graph_ds,direction)
    elif management_type=='*':
        for edge in set(edges):
            if edge not in ePropsdict:
                if reward != '':
                    ePropsdict[edge] = {'rwd':reward}
                    graph_ds = checkAdd(edge,graph_ds,direction)
                else:
                    ePropsdict[edge] = {}
                    graph_ds = checkAdd(edge,graph_ds,direction)
            else:
                if reward != '':
                    ePropsdict[edge] = {'rwd':reward}
                
    elif management_type=='@':
        for edge in set(edges):
            if edge in ePropsdict:
                if reward != '':
                    ePropsdict[edge] = {'rwd':reward}
                

    return ePropsdict,graph_ds
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
        if 0<=vertex+graph_ds[2]<graph_ds[1]:
            edges.append((vertex,vertex+graph_ds[2]))
    if direction == '=':
        
        to_add = []
        for edge in set(edges):
            to_add.append((edge[1],edge[0]))
        edges+=to_add
    # print(edges)
    if management_type=='~':
        for edge in set(edges):
            if edge in ePropsdict:
                del ePropsdict[edge]
                graph_ds = checkRemove(edge,graph_ds,ePropsdict,direction)
            else:
                if reward != '':
                    ePropsdict[edge] = {'rwd':reward}
                    graph_ds = checkAdd(edge,graph_ds,direction)
                else:
                    ePropsdict[edge] = {}
                    graph_ds = checkAdd(edge,graph_ds,direction)
    elif management_type=='!':
        for edge in set(edges):
            if edge in ePropsdict:
                del ePropsdict[edge]
                graph_ds = checkRemove(edge,graph_ds,ePropsdict,direction)
    elif management_type=='+':
        
        for edge in set(edges):
            if edge not in ePropsdict:
                if reward != '':
                    ePropsdict[edge] = {'rwd':reward}
                    graph_ds = checkAdd(edge,graph_ds,direction)
                else:
                    ePropsdict[edge] = {}
                    graph_ds = checkAdd(edge,graph_ds,direction)
    elif management_type=='*':
        for edge in set(edges):
            if edge not in ePropsdict:
                if reward != '':
                    ePropsdict[edge] = {'rwd':reward}
                    graph_ds = checkAdd(edge,graph_ds,direction)
                else:
                    ePropsdict[edge] = {}
                    graph_ds = checkAdd(edge,graph_ds,direction)
            else:
                if reward != '':
                    ePropsdict[edge] = {'rwd':reward}
                
    elif management_type=='@':
        for edge in set(edges):
            if edge in ePropsdict:
                if reward != '':
                    ePropsdict[edge] = {'rwd':reward}
                

    return ePropsdict,graph_ds

def form_one(ePropsdict,graph_ds,directive):
    size_list = [i for i in range(int(graph_ds[1]))]
    mngmnt = {'!','+','*','~','@'}
    directionality =''
    reward = ''
    eslc = directive
    if 'R' in eslc:
                 
                 if r:=re.search('R\d+',eslc):
                         reward = int(r.group()[1:])
                 else:
                       reward = graph_ds[3]
                 eslc = eslc[:eslc.index('R')]
    management_type = '~'
    if eslc[0] in mngmnt:
        management_type = eslc[0]
        eslc = eslc[1:]
    # print(eslc,management_type,reward)
    
    if '=' in eslc:
        directionality = '='
    else:
        directionality = '~'
    sides = eslc.split(directionality)
    
    edges = [i for i in zip(parseCommaSplices(sides[0].split(','),graph_ds),parseCommaSplices(sides[1].split(','),graph_ds))]
    if directionality == '=':
        to_add = []
        for edge in set(edges):
            to_add.append((edge[1],edge[0]))
        edges+=to_add
    ePropsdict,graph_ds = modifyEPropsFormOne(ePropsdict,graph_ds,edges,reward,directionality,management_type)
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
    vertices = parseCommaSplices(esplits,graph_ds)
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
        # old_blocked_set = )
        if 'E' in directive:
            
            eslc = directive[1:]
            # print(eslc)
            if 'N' in eslc or 'E' in eslc or 'W' in eslc or 'S' in eslc:
                ePropsdict,graph_ds = form_two(ePropsdict,graph_ds,eslc)
            
            else:
                ePropsdict,graph_ds = form_one(ePropsdict,graph_ds,eslc)


        '''
        For blocking 
        Identify jumps
        get rid of them first
        then toggle all default edges
        have a set of vertices W which is vertices you are working with
        Have a set of verticeds X = V-W

        Regex "^V([-\d:,]+)((R\d*)?|([B])?)*$"
        '''
        if directive[0] == 'V':
            reward = ''
            blocking = False
            breakdown_regex = "^V([-\d:,]+)((R\d*)?|([B])?)*$"
            if m:=re.search(breakdown_regex,directive):
                if v:=m.group(1):
                    vslc = v
                if r:=m.group(3):
                    if r=="R":
                        reward = graph_ds[3]
                    else:
                        reward = int(r[1:])
                if m.group(4):
                    blocking = True
                
            # print(vslcs)
            splits = vslc.split(',')
            # print(splits)
            
            vertices = parseCommaSplices(splits,graph_ds)
            if reward!='':
                    for vertex in vertices:
                            vPropsDict[vertex] = {'rwd':reward}
            if blocking:

                    for vertex in set(vertices):
                        north_south_east_west = []
                        if graph_ds[1]>vertex-graph_ds[2]>=0:
                            north_south_east_west.append(vertex-graph_ds[2])
                        if vertex%graph_ds[2]!=graph_ds[2]-1 and 0<=vertex+1<graph_ds[1]:
                            north_south_east_west.append(vertex+1)
                        if vertex%graph_ds[2]!=0 and 0<=vertex-1<graph_ds[1]:
                            north_south_east_west.append(vertex-1)
                        if 0<=vertex+graph_ds[2]<graph_ds[1]:
                            north_south_east_west.append(vertex+graph_ds[2])
                        jumps = []
                        for nbr in graph_nbrs[vertex]:
                            if nbr not in north_south_east_west:
                                jumps.append((vertex,nbr))
                        for jump in jumps:
                            if jump[0] == jump[1]:
                                continue
                            elif jump in ePropsdict:
                                del ePropsdict[jump]
                                graph_ds = checkRemove(jump,graph_ds,ePropsdict,'~')
                            elif (jump[1],jump[0]) in ePropsdict:
                                del ePropsdict[(jump[1],jump[0])]
                                graph_ds = checkRemove((jump[1],jump[0]),graph_ds,ePropsdict,'~')
                        
                        # ePropsdict,graph_ds = modifyEProps(ePropsdict,graph_ds,'NEWS',vertex,'','=',management_type='~')

                        s_edges = []
                        # if graph_ds[1]>vertex-graph_ds[2]>=0:
                        #     s_edges.append((vertex,vertex-graph_ds[2]))
                        # if vertex%graph_ds[2]!=graph_ds[2]-1 and 0<=vertex+1<graph_ds[1]:
                        #     s_edges.append((vertex,vertex+1))
                        # if vertex%graph_ds[2]!=0 and 0<=vertex-1<graph_ds[1]:
                        #     s_edges.append((vertex,vertex-1))
                        # if vertex+graph_ds[2]<graph_ds[1]:
                        #     s_edges.append((vertex,vertex+graph_ds[2]))
                        
                        for v in north_south_east_west:
                            s_edges.append((vertex,v))
                            s_edges.append((v,vertex))
                        ePropsdict,graph_ds = modifyEPropsFormOne(ePropsdict,graph_ds,s_edges,'',direction='~',management_type='~')
                        
                        to_remove = []
                        for edge in ePropsdict:
                            if edge[1] == vertex and edge[0] not in north_south_east_west:
                                to_remove.append(edge)

                        for edge in to_remove:
                            del ePropsdict[edge]
                            graph_ds = checkRemove(edge,graph_ds,ePropsdict,'~')
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
    jumps = ''
    for i,nbr in enumerate(nbrs):
        # print(nbr)
        not_jump_vertices = []
        symbol =''
        if i+1 in nbr and i%graph[0][2]!=graph[0][2]-1:
            # print('E added')
            symbol+='E'
            not_jump_vertices.append(i+1)
        if i-1 in nbr and i%graph[0][2]!=0:
            symbol+='W'
            not_jump_vertices.append(i-1)
        if i+graph[0][2] in nbr:
            # print('S added')
            symbol+='S'
            not_jump_vertices.append(i+graph[0][2])
        if i-graph[0][2] in nbr:
            symbol+='N'
            not_jump_vertices.append(i-graph[0][2])
        for n in nbr:
            if n not in not_jump_vertices:
                jumps+=f"{i}~{n};"
        representation+=symbol_dict[symbol]
    jumps = jumps[:-1]
    # print(0 + graph[0][2] in [1,5])
    # print(graph[0][-2])
    if jumps:
        jumps = 'Jumps:'+jumps
    return representation+'\n'+jumps

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
def BFS(graph,v,north_south_east_west_lookup):
    if grfVProps(graph,v) != {}: return [v],[]
    parseMe = [v]
    dctSeen = {v:''}
    visited_edges = []
    while parseMe:
        node = parseMe.pop(0)
        for nbr in grfNbrs(graph,node):
            if nbr not in dctSeen:
                visited_edges.append((node,nbr))
                if grfVProps(graph,nbr) != {} or grfEProps(graph,node,nbr) != {}:
                    dctSeen[nbr] = node
                    
                    return reconstruct_path(v,nbr,dctSeen,north_south_east_west_lookup)
                    # return dctSeen,nbr
                dctSeen[nbr] = node
                parseMe.append(nbr)
            else:
                '''
                check if ive visited the edge before

                '''
                if (node,nbr) not in visited_edges:
                    visited_edges.append((node,nbr))
                    if grfEProps(graph,node,nbr) != {}:
                    
                        r = reconstruct_path(v,nbr,dctSeen,north_south_east_west_lookup)
                        return r[0] + [node] +[nbr], r[1]
                        # return dctSeen,nbr
    return -1
def reconstruct_path(start,goal,dctSeen,north_south_east_west_lookup):
    jumps = []
    path_list = [goal]
    temp=goal
    while temp!=start:
        if temp in dctSeen:
        
            if dctSeen[temp] not in north_south_east_west_lookup[temp]:
                jumps.append(f"{dctSeen[temp]}~{temp}")
            temp=dctSeen[temp]
            path_list.append(temp)
        else:
            return -1
    return path_list, jumps
def m(args):
    graph = grfParse(args)
    # print(graph)
    size = grfSize(graph)
    properties = grfGProps(graph)
    representation  = grfStrEdges(graph)
    # print(grfNbrs(graph,1))
    jumps = ''
    if 'Jumps' in representation:
        jumps = representation[representation.index('Jumps'):]
        representation = representation[:representation.index('Jumps')]
    if jumps:
        print('\n'.join(representation[i:i+graph[0][2]] for i in range(0,graph[0][1],graph[0][2])))
        print(jumps)

    elif representation:
        print('\n'.join(representation[i:i+graph[0][2]] for i in range(0,graph[0][1],graph[0][2])))
        
    print(grfStrProps(graph))
def m2(args):
    graph = grfParse(args)
    # print(graph)
    symbol_dict = {'E':'E','W':'W','N':'N','S':'S','EN':'L','WN':'J','WSN':'<','WS':'7','EWN':'^','EWSN':'+','EWS':'v','ES':'r','ESN':'>','':'.','EW':'-','SN':'|'}
    jumps = []
    res = ''
    north_south_east_west_lookup  = {}
    for i in range(graph[0][1]):
        north_south_east_west_lookup[i] = []
        if i-graph[0][2]>=0:
            north_south_east_west_lookup[i].append(i-graph[0][2])
        if i+graph[0][2]<graph[0][1]:
            north_south_east_west_lookup[i].append(i+graph[0][2])
        if i%graph[0][2]!=0:
            north_south_east_west_lookup[i].append(i-1)
        if i%graph[0][2]!=graph[0][2]-1:
            north_south_east_west_lookup[i].append(i+1)
    for i,nbrs in enumerate(graph[0][-2]):
        
        if grfVProps(graph,i) == {}:
            nbr_paths = {}
            for nbr in nbrs:
                if grfEProps(graph,i,nbr) != {}:
                    nbr_paths[nbr] = [nbr]
                elif (b:=BFS(graph,nbr,north_south_east_west_lookup)) != -1:
                    
                    
                    nbr_paths[nbr],t_jumps = b
                    # print(i,nbr, nbr_paths[nbr])
                    jumps+=t_jumps

            if nbr_paths=={}:
                res+='.'
            else:
                symbol = ''
                min_path_len = min(len(path) for path in nbr_paths.values())
                for nbr in nbr_paths:
                    
                    if len(nbr_paths[nbr])==min_path_len:
                        if nbr not in north_south_east_west_lookup[i]:
                            jumps.append(f"{i}~{nbr}")
                        if nbr == i+1 and nbr in north_south_east_west_lookup[i]:
                            symbol+='E'
                        if nbr == i-1 and nbr in north_south_east_west_lookup[i]:
                            symbol+='W'
                        if nbr == i+graph[0][2] and nbr in north_south_east_west_lookup[i]:
                            symbol+='S'
                        if nbr == i-graph[0][2] and nbr in north_south_east_west_lookup[i]:
                            symbol+='N'
                key = ''
                if 'E' in symbol:
                    key+='E'
                if 'W' in symbol:
                    key+='W'
                if 'S' in symbol:
                    key+='S'
                if 'N' in symbol:
                    key+='N'
                res+=symbol_dict[key]
        else:
            res+='*'
    res = '\n'.join(res[i:i+graph[0][2]] for i in range(0,graph[0][1],graph[0][2]))
    print("Policy: ")
    print(res)
    print(';'.join(set(jumps)))
def main():
    graph = grfParse(args)
    # print(graph)
    symbol_dict = {'E':'E','W':'W','N':'N','S':'S','EN':'L','WN':'J','WSN':'<','WS':'7','EWN':'^','EWSN':'+','EWS':'v','ES':'r','ESN':'>','':'.','EW':'-','SN':'|'}
    jumps = []
    res = ''
    north_south_east_west_lookup  = {}
    for i in range(graph[0][1]):
        north_south_east_west_lookup[i] = []
        if i-graph[0][2]>=0:
            north_south_east_west_lookup[i].append(i-graph[0][2])
        if i+graph[0][2]<graph[0][1]:
            north_south_east_west_lookup[i].append(i+graph[0][2])
        if i%graph[0][2]!=0:
            north_south_east_west_lookup[i].append(i-1)
        if i%graph[0][2]!=graph[0][2]-1:
            north_south_east_west_lookup[i].append(i+1)
    
    for i,nbrs in enumerate(graph[0][-2]):
        
        if grfVProps(graph,i) == {}:
            nbr_paths = {}
            for nbr in nbrs:
                if grfEProps(graph,i,nbr) != {}:
                    nbr_paths[nbr] = [nbr]
                elif (b:=BFS(graph,nbr,north_south_east_west_lookup)) != -1:
                    
                    
                    nbr_paths[nbr],t_jumps = b
                    # print(i,nbr, nbr_paths[nbr])
                    jumps+=t_jumps
            if nbr_paths=={}:
                res+='.'
            else:
                symbol = ''
                min_path_len = min(len(path) for path in nbr_paths.values())
                for nbr in nbr_paths:
                    
                    if len(nbr_paths[nbr])==min_path_len:
                        if nbr not in north_south_east_west_lookup[i]:
                            jumps.append(f"{i}~{nbr}")
                        if nbr == i+1 and nbr in north_south_east_west_lookup[i]:
                            symbol+='E'
                        if nbr == i-1 and nbr in north_south_east_west_lookup[i]:
                            symbol+='W'
                        if nbr == i+graph[0][2] and nbr in north_south_east_west_lookup[i]:
                            symbol+='S'
                        if nbr == i-graph[0][2] and nbr in north_south_east_west_lookup[i]:
                            symbol+='N'
                key = ''
                if 'E' in symbol:
                    key+='E'
                if 'W' in symbol:
                    key+='W'
                if 'S' in symbol:
                    key+='S'
                if 'N' in symbol:
                    key+='N'
                res+=symbol_dict[key]
        else:
            res+='*'
    res = '\n'.join(res[i:i+graph[0][2]] for i in range(0,graph[0][1],graph[0][2]))
    print("Policy: ")
    print(res)
    print(';'.join(set(jumps)))
            
    # print(graph[1][17])

if __name__ == '__main__': main()

#Shaurya Jain, pd 3, 2023