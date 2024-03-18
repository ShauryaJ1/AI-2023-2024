import sys; args = sys.argv[1:]
import math
import re
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

    size_list = [i for i in range(int(graph_ds[1]))]
    graph_nbrs = [[] for i in range(int(graph_ds[1]))]
    if graph_ds[2]!=0 and graph_ds[0]!='N':

        
        for i,nbr in enumerate(graph_nbrs):
            if i%graph_ds[2]!=0:
                graph_nbrs[i].append(i-1)
            if i%graph_ds[2]!=graph_ds[2]-1:
                graph_nbrs[i].append(i+1)
            if i//graph_ds[2]!=0:
                graph_nbrs[i].append(i-graph_ds[2])
            if i//graph_ds[2]!=(graph_ds[1]//graph_ds[2])-1:
                graph_nbrs[i].append(i+graph_ds[2])
            
    graph_ds.append(graph_nbrs)
    graph_ds.append([])
    blocked_list = []
    blocked_set = set()
    for directive in lstArgs[1:]:
        ls = []
        old_blocked_set = set(blocked_list)
        if directive[0] == 'V':
            
            vslcs = directive[1:]
            # print(vslcs)
            splits = vslcs.split(',')
            # print(splits)
            for vsplit in splits:
                ls = []
                if 'R' in vsplit:
                    ls.append(vsplit.index('R'))
                if 'B' in vsplit:
                    ls.append(vsplit.index('B'))
                if ls:
                     vslc= vsplit[:min(ls)]
                else:
                    vslc = vsplit[:]
                if vslc.count(':')==0:
                    graph_ds[-1].append(size_list[int(vslc)])
                    if 'B' in directive:
                        blocked_list+=[size_list[int(vslc)]]
                if vslc.count(':')==1:
                    if vslc == ':':
                        if 'B' in directive:
                            blocked_list+=size_list
                        graph_ds[-1].append(size_list)
                    elif vslc[-1]==':':
                        if 'B' in directive:
                            blocked_list+=size_list[int(vslc[:vslc.index(':')]):]
                        graph_ds[-1].append(size_list[int(vslc[:vslc.index(':')]):])
                    elif vslc[0] == ':':
                        if 'B' in directive:
                            blocked_list+=size_list[:int(vslc[vslc.index(':')+1:])]
                        graph_ds[-1].append(size_list[:int(vslc[vslc.index(':')+1:])])
                    else:
                        if 'B' in directive:
                            blocked_list+=size_list[size_list[int(vslc[:vslc.index(':')])]:int(vslc[vslc.index(':')+1:])]
                        graph_ds[-1].append(size_list[size_list[int(vslc[:vslc.index(':')])]:int(vslc[vslc.index(':')+1:])])
                if vslc.count(':')==2:
                    vslc_splits = vslc.split(':')
                    if not any(vslc_splits):
                         if 'B' in directive:
                             blocked_list+=size_list
                         graph_ds[-1].append(size_list)
                    elif(vslc_splits[0] =='' and vslc_splits[2]==''):
                         if 'B' in directive:
                             blocked_list+=size_list[:int(vslc_splits[1]):]
                         graph_ds[-1].append(size_list[:int(vslc_splits[1]):])
                    elif(vslc_splits[1] =='' and vslc_splits[2]==''):
                        if 'B' in directive:
                            blocked_list+=size_list[int(vslc_splits[0])::]
                        graph_ds[-1].append(size_list[int(vslc_splits[0])::])
                    elif(vslc_splits[1] =='' and vslc_splits[0]==''):
                        if 'B' in directive:
                            blocked_list+=size_list[::int(vslc_splits[2])]
                        graph_ds[-1].append(size_list[::int(vslc_splits[2])])
                    elif(vslc_splits[0]==''):
                        if 'B' in directive:
                            blocked_list+=size_list[:int(vslc_splits[1]):int(vslc_splits[2])]
                        graph_ds[-1].append(size_list[:int(vslc_splits[1]):int(vslc_splits[2])])
                    elif(vslc_splits[1]==''):
                         if 'B' in directive:
                            blocked_list+=size_list[int(vslc_splits[0])::int(vslc_splits[2])]
                         graph_ds[-1].append(size_list[int(vslc_splits[0])::int(vslc_splits[2])])
                    elif(vslc_splits[2]==''):
                        if 'B' in directive:
                            blocked_list+=size_list[int(vslc_splits[0]):int(vslc_splits[1]):]
                        graph_ds[-1].append(size_list[int(vslc_splits[0]):int(vslc_splits[1]):])
                    else:
                        if 'B' in directive:
                            blocked_list+=size_list[int(vslc_splits[0]):int(vslc_splits[1]):int(vslc_splits[2])]
                        graph_ds[-1].append(size_list[int(vslc_splits[0]):int(vslc_splits[1]):int(vslc_splits[2])])
        blocked_set = set(blocked_list)
        # to_remove = []
        # for b in blocked_set:
        #     if b in old_blocked_set:
        #         to_remove.append(b)
        # for r in to_remove:
        #     blocked_set.remove(r)
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
    
                    

    # print(graph_ds)
    # print(graph_ds)
    # print(graph_nbrs)
    return graph_ds, graph_nbrs
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
    return {}

def grfEProps(graph,v1,v2):
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
    if 'width' in properties:
        return f"rwd: {properties['rwd']}, width: {properties['width']}"

    return f"rwd: {properties['rwd']}"

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