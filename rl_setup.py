import sys; args = sys.argv[1:]
import math
import re
global symbols_dict
def grfParse(lstargs):
    to_maximize = 1
    implied_reward = 12
    size = int(lstargs[0])        
    width = -1
    start = 1
    cellProps ={}
    if lstargs[1][0] in '1234567890':
        width = int(lstargs[1])
        start = 2
    if width == -1:
        height,width=0,0
        for i in range(1,int(math.sqrt(size)+1)):
            if size%i==0:
                height=i
                width=size//i
    else:
        height = size//width

    links = [[] for i in range(size)]
    for i in range(size):
        if i%width!=0 and size>i-1>=0:
            links[i].append(i-1)
        if i%width!=width-1 and size>i+1>=0:
            links[i].append(i+1)
        if size>i-width>=0:
            links[i].append(i-width)
        if size>i+width>=0:
            links[i].append(i+width)
    
    for arg in lstargs[start:]:
        if arg[0] == 'R' or arg[0] == 'r':
            if ':' in arg:
                splits = arg[1:].split(':')
                if splits[0] == '':
                    implied_reward = int(splits[1])
                else:
                    cellProps[splits[0]] = int(splits[1])
            else:
                cellProps[arg[1:]] = implied_reward
        if arg[0]=='B':
            my_regex_1 = 'B\d+'
            my_regex_2 = '[NSEW]+'
            if m:=re.match(my_regex_1,arg):
                cell = int(m.group()[1:])
                
            if m:=re.search(my_regex_2,arg):
                for direction in m.group():
                    if direction == 'N' and size>cell-width>=0:
                        if cell-width in links[cell]:
                            links[cell].remove(cell-width)
                            links[cell-width].remove(cell)
                        else:
                            links[cell].append(cell-width)
                            links[cell-width].append(cell)
                    if direction == 'S' and size>cell+width>=0:
                        if cell+width in links[cell]:
                            links[cell].remove(cell+width)
                            links[cell+width].remove(cell)
                        else:
                            links[cell].append(cell+width)
                            links[cell+width].append(cell)
                    if direction == 'E' and size>cell+1>=0 and cell%width!=width-1:
                        if cell+1 in links[cell]:
                            links[cell].remove(cell+1)
                            links[cell+1].remove(cell)
                        else:
                            links[cell].append(cell+1)
                            links[cell+1].append(cell)
                    if direction == 'W' and size>cell-1>=0 and cell%width!=0:
                        if cell-1 in links[cell]:
                            links[cell].remove(cell-1)
                            links[cell-1].remove(cell)
                        else:
                            links[cell].append(cell-1)
                            links[cell-1].append(cell)

            else:

                    if size>cell-width>=0:
                        if cell-width in links[cell]:
                            links[cell].remove(cell-width)
                            links[cell-width].remove(cell)
                        else:
                            links[cell].append(cell-width)
                            links[cell-width].append(cell)
                    if size>cell+width>=0:
                        if cell+width in links[cell]:
                            links[cell].remove(cell+width)
                            links[cell+width].remove(cell)
                        else:
                            links[cell].append(cell+width)
                            links[cell+width].append(cell)
                    if size>cell+1>=0 and cell%width!=width-1:
                        if cell+1 in links[cell]:
                            links[cell].remove(cell+1)
                            links[cell+1].remove(cell)
                        else:
                            links[cell].append(cell+1)
                            links[cell+1].append(cell)
                    if size>cell-1>=0 and cell%width!=0:
                        if cell-1 in links[cell]:
                            links[cell].remove(cell-1)
                            links[cell-1].remove(cell)
                        else:
                            links[cell].append(cell-1)
                            links[cell-1].append(cell)
            
        if arg[0]=='G':
            to_maximize = int(arg[1:])
    return size,width,height,links,cellProps,to_maximize
def reconstruct_path(start, goal, dctSeen):
    path_list = [goal]
    temp = goal
    while temp != start:
        if temp in dctSeen:
            temp = dctSeen[temp]
            path_list.append(temp)
        else:
            return -1
    return path_list[::-1]
def BFS(size,start_cell,goal_cell,cellProps,links):
    if start_cell ==int(goal_cell): return [start_cell], goal_cell
    if str(start_cell) in cellProps: return -1
    parseMe = [start_cell]
    dctSeen = {}
    rewards_seen = []
    while parseMe:
        curr = parseMe.pop(0)
        for neighbor in links[curr]:
            if str(neighbor) in cellProps and neighbor!=int(goal_cell):
                rewards_seen.append(neighbor)
                continue
            if neighbor not in dctSeen and neighbor not in rewards_seen:
                parseMe.append(neighbor)
                dctSeen[neighbor] = curr
                if neighbor == int(goal_cell):
                    return reconstruct_path(start_cell,neighbor,dctSeen),goal_cell
            
        
    return -1
def main():
     if len(args) == 1:
        print('.'*int(args[0]))
     else:
        rev_symbols_dict = {'V': 'RU', 'W': 'RUD', 'S': 'RD', 'T': 'LRD', 'E': 'LD', 'F': 'LUD', 'M': 'LU', 'N': 'LRU', '|': 'UD', '-':'LR', '+':'LRUD','D':'D','U':'U','L':'L','R':'R','.':''}
        symbols_dict = {v: k for k, v in rev_symbols_dict.items()}
        size,width,height,links,cellProps,to_maximize = grfParse(args)
        result = ''
        if to_maximize == 0:
            rewards_sorted = sorted([(cellProps[key],key) for key in cellProps])[::-1]
            for cell in range(size):
                if str(cell) in cellProps:
                    result+='*'
                    continue
                possibles = []
                for neighbor in links[cell]:
                
                    goal_cell = -1
                    counter = 0
                    while counter<len(rewards_sorted):
                        '''
                        For each cell with highest reward, calculate the shortest path to the neighbor cell
                        '''
                        highest_reward= rewards_sorted[counter][0]
                        possible_paths = []
                        for reward in rewards_sorted[counter:]:
                            
                            if reward[0]==highest_reward:
                                if (b:=BFS(size,neighbor,reward[1],cellProps,links))!=-1:
                                    possible_paths.append((reward[0],len(b[0]),b[0]))
                                    goal_cell = reward[1]

                        if possible_paths != []:
                            break
                        counter+=1
                    if goal_cell == -1:
                        continue
                    else:
                        possibles.append((sorted(possible_paths)[0][0],neighbor,sorted(possible_paths)[0][2]))
                if possibles == []:
                    result += '.'
                else:
                    max_reward = max([possible[0] for possible in possibles])
                    min_length = min([len(possible[2]) for possible in possibles if possible[0]==max_reward])
                    min_paths = [possible[2] for possible in possibles if len(possible[2])==min_length and possible[0]==max_reward]
                    to_lookup = ''
                    for min_path in min_paths:
                        if min_path[0] == cell-1 and cell%width!=0:
                            to_lookup+='L'
                        elif min_path[0] == cell+1 and cell%width!=width-1:
                            to_lookup+='R'
                        elif min_path[0] == cell-width:
                            to_lookup+='U'
                        elif min_path[0] == cell+width:
                            to_lookup+='D'

                    to_actually_lookup = ''
                    if 'L' in to_lookup:
                        to_actually_lookup+='L'
                    if 'R' in to_lookup:
                        to_actually_lookup+='R'
                    if 'U' in to_lookup:
                        to_actually_lookup+='U'
                    if 'D' in to_lookup:
                        to_actually_lookup+='D'
                    result += symbols_dict[to_actually_lookup]
            print('\n'.join([result[i:i+width] for i in range(0,len(result),width)]))
        if to_maximize==1:
            '''
            For each cell
                find a path to each reward cell if possible
                add path to list + reward/len(path)
                find max reward/len(path
                give direction
                aadd to result
            
            '''
            rewards_sorted = sorted([(cellProps[key],key) for key in cellProps])[::-1]
            for cell in range(size):
                if str(cell) in cellProps:
                    result+='*'
                    continue
                possibles = []
                for neighbor in links[cell]:

                    for reward in rewards_sorted:

                        if (b:=BFS(size,neighbor,reward[1],cellProps,links))!=-1:
                            possibles.append((reward[0]/len(b[0]),b[0]))
                if possibles == []:
                    result += '.'
                else:
                    max_reward = max([possible[0] for possible in possibles])
                    to_lookup = ''
                    to_actually_lookup = ''

                    for possible in possibles:
                        if possible[0] == max_reward:
                            if possible[1][0] == cell-1 and cell%width!=0:
                                to_lookup+='L'
                            elif possible[1][0] == cell+1 and cell%width!=width-1:
                                to_lookup+='R'
                            elif possible[1][0] == cell-width:
                                to_lookup+='U'
                            elif possible[1][0] == cell+width:
                                to_lookup+='D'

                    if 'L' in to_lookup:
                                to_actually_lookup+='L'
                    if 'R' in to_lookup:
                                to_actually_lookup+='R'
                    if 'U' in to_lookup:
                                to_actually_lookup+='U'
                    if 'D' in to_lookup:
                                to_actually_lookup+='D'
                    result += symbols_dict[to_actually_lookup]
            print('\n'.join([result[i:i+width] for i in range(0,len(result),width)]))

                
        
if __name__ == '__main__':
    main()






















#Shaurya Jain, pd 3, 2023