import sys; args = sys.argv[1:]
import time
import math
import re
start_time=time.time()
puzzle=args[0]

def find_goal(start_puzzle):
   list_str = list(start_puzzle)
   list_str.remove("_")
   return "".join(sorted(list_str)) + "_"

if len(args)>1:
   goal = args[1]
else:
   goal=find_goal(puzzle)
goal=find_goal(puzzle)
steps=0
height,width=0,0
for i in range(1,int(math.sqrt(len(puzzle))+1)):
  if len(puzzle)%i==0:
    height=i
    width=len(puzzle)//i

def swap(l,a,b):
  n=list(l)
  temp = n[a]
  n[a] = n[b]
  n[b] = temp
  return ''.join(n)

def neighbors(puzzle):
    
    neighbors_list=[]
    space = puzzle.index("_")
    if space+width<len(puzzle):
       neighbors_list.append(swap(puzzle,space,space+width))
    if space-width>=0:
       neighbors_list.append(swap(puzzle,space,space-width))
    if space%width!=width-1:
      neighbors_list.append(swap(puzzle,space,space+1))
    if space%width!=0:
      neighbors_list.append(swap(puzzle,space,space-1))
    return neighbors_list

def print_bands_of_puzzles(puzzle_strings,height,width,k_puzzles=6):
    k_puzzle_strings=[]
    for k in range(0,len(puzzle_strings),6):
      k_puzzle_strings = puzzle_strings[k:k+6]

      band = ""
      for i in range(0,height*width,width):
            for puzzle in k_puzzle_strings:
               band+=puzzle[i:i+width] + ' '  
            print(band)
            band=""
      print()

def BFS(start,goal):
   
   if start==goal:
      return [start]
   parseMe = [start]
   dctSeen = {}
   while parseMe:
      node = parseMe.pop(0)
      for nbr in neighbors(node):
        if nbr not in dctSeen:
            if nbr == goal:
                dctSeen[nbr] = node
                return dctSeen
            dctSeen[nbr] = node
            parseMe.append(nbr)
   
   return -1
def BFS_no_goal(start):
   
   if start==goal:
      return [start]
   parseMe = [start]
   dctSeen = {start:0}
   levels = [1]
   families = [[0,0,0],[0,0,0,0],[0,0,0,0,0]]
   while parseMe:
      node = parseMe.pop(0)
      levelChildren = dctSeen[node]+1
      nbrs = [nbr for nbr in neighbors(node) if nbr not in dctSeen]
      if levelChildren < len(levels):
         levels[levelChildren] += len(nbrs)
      else:
         levels.append(len(nbrs))
      nbrs_len = len(nbrs)
      for nbr in nbrs:
        dctSeen[nbr] = levelChildren                 
        parseMe.append(nbr)
   return dctSeen,levels

def find_patterns(dctSeen):
   patterns = {"02":0,"03":0,"04":0,"20":0,"30":0,"40":0,"11":0,"13":0,"12":0,"22":0,"21":0,"31":0}
   for node in dctSeen:
      nbrs = neighbors(node)
      
      parentCount = 0
      childCount=0
      for nbr in nbrs:
         if dctSeen[nbr]<dctSeen[node]:
            parentCount+=1
         else:
            childCount+=1
    #   if((str(parentCount)+str(childCount)) in patterns):
      patterns[str(parentCount)+str(childCount)]+=1
   return patterns, sum([patterns[pattern] for pattern in patterns])
      
      

def BFS_Families(start):
   
   if start==goal:
      return [start]
   parseMe = [start]
   dctSeen = {start:0}
   families = [[0,0,0],[0,0,0,0],[0,0,0,0,0]]
   while parseMe:
      node = parseMe.pop(0)
      
      nbrs = neighbors(node)
      numParents = len([nbr for nbr in nbrs if dctSeen[nbr]==dctSeen[node]-1])
      families[len(nbrs)-2][numParents] += 1
      for nbr in nbrs:
        dctSeen[nbr] = dctSeen[node]+1
        parseMe.append(nbr)
   return families
    # if start==goal:
    #     return [start]
    # parseMe = [start]
    # dctSeen = {start:0}
    # levels = [1]
    # while parseMe:
    #     node = parseMe.pop(0)
    #     levelChildren = dctSeen[node]+1
    #     nbrs = [nbr for nbr in neighbors(node) if nbr not in dctSeen]
    #     if levelChildren < len(levels):
    #         levels[levelChildren] += len(nbrs)
    #     else:
    #         levels.append(len(nbrs))
    #     for nbr in nbrs:
    #         dctSeen[nbr] = levelChildren
    #         parseMe.append(nbr)
    # return levels

def path_func(startpzl,goal,dctSeen):
   path_list = [goal]
   temp=goal
   while temp!=startpzl:
     if dctSeen[temp]:
        temp=dctSeen[temp]
        path_list.append(temp)
     else:
        return -1
        
   return path_list

seen = BFS_no_goal(puzzle)
print(find_patterns(seen[0]))
print(sum(seen[1]))


   
  
end_time=time.time()
print("Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))
#Shaurya Jain, pd 3, 2023