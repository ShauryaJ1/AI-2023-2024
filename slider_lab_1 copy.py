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

seen = BFS(puzzle,goal)
path=path_func(puzzle,goal,seen)
if path!=-1:
   print_bands_of_puzzles(path[::-1],height,width,k_puzzles=6)
   print(path[::-1])
end_time=time.time()
print("Steps: ", len(path)-1)
print("Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))
#Shaurya Jain, pd 3, 2023