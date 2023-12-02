import sys; args = sys.argv[1:]
import time
import math
import re
import random
width,height=3,3
def find_goal(start_puzzle):
   list_str = list(start_puzzle)
   list_str.remove("_")
   return "".join(sorted(list_str)) + "_"

def inversion_count(puzzle):
   puz = ''.join(puzzle.split("_"))
   count=0
   for id,p in enumerate(puz):
      for s in puz[id:]:
         if p>s:
            count+=1
   return count
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
def generate_random_3x3_puzzles(n_puzzles):
    puzzles=[]
    for i in range(n_puzzles):
        temp_puzzle=[0]*9
        temp_puzzle[random.randint(0,8)] = "_"
        while temp_puzzle.count(0)>0:
            rand_n1=random.randint(1,8)
            rand_n2=random.randint(0,8)
            if temp_puzzle[rand_n2]==0 and temp_puzzle.count(str(rand_n1))==0:
                temp_puzzle[rand_n2]=str(rand_n1)
        temp_puzzle="".join(temp_puzzle)
        puzzles.append(temp_puzzle)

    return puzzles

puzzles= generate_random_3x3_puzzles(1000)

def loop(puzzles):
    times=[]
    path_lengths=[]
    for p in puzzles:
        goal=find_goal(p)
        steps=0
        start_time=time.time()
        if inversion_count(p)%2!=inversion_count(goal)%2 and width%2==1:
           steps=-1
        else:
           seen = BFS(p,goal)
           if seen!=-1:
                path=path_func(p,goal,seen)
                if path!=-1:
                    steps=len(path)-1
           else:   
                steps=-1  
        end_time=time.time()
        times.append(end_time-start_time)
        path_lengths.append(steps)
    return sum(times)/len(times), sum(path_lengths)/len(path_lengths), sum(times), sum(path_lengths)

print(loop(puzzles))
