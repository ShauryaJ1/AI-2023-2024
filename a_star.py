import sys; args = sys.argv[1:]
import math
import time 

def find_h_w(puzzle):
    height,width=0,0
    for i in range(1,int(math.sqrt(len(puzzle))+1)):
        if len(puzzle)%i==0:
            height=i
            width=len(puzzle)//i
    return height,width
def file_to_lines():
    return open(args[0]).read().splitlines()
def inversion_count(puzzle):
   puz = ''.join(puzzle.split("_"))
   count=0
   for id,p in enumerate(puz):
      for s in puz[id:]:
         if p>s:
            count+=1
   return count
def condensed_path(puzzles_list,width):
    if len(puzzles_list)==0: return "X"
    if len(puzzles_list)==1: return "G"
    dct = {-1:"R",1:"L",width:"U",-width:"D"}
    moves_string=""
    for i in range(len(puzzles_list)-1):
        idx_1 = (puzzles_list[i]).index("_")
        idx_2 = (puzzles_list[i+1]).index("_")
        moves_string+=dct[idx_1-idx_2]
    return moves_string
# def args_to_list(arg_str):
#     return arg_str[1:-1].split(",")
def h_tile(pzl,goal,c,width):
    puzzle_space = pzl.index(c)
    goal_space = goal.index(c)
    difference_space_vd = goal_space//width-puzzle_space//width
    difference_space_hd = goal_space%width-puzzle_space%width
    return abs(difference_space_hd)+abs(difference_space_vd)
   #  diff = abs(pzl.index(c)-goal.index(c))
   #  return diff//width + diff%width
def h(pzl,goal,width):
   # goal_space = goal.index("_")
   # goal_mod_width = goal_space%width
   # goal_div_width = goal_space//width
   # total_md=0
   # for c in pzl:
   #    if c!="_":
   #       puzzle_space = pzl.index(c)
   #       total_md+=abs(goal_mod_width-puzzle_space%width)+abs(goal_div_width-puzzle_space//width)
   # return total_md
   return sum([h_tile(pzl,goal,c,width) for c in pzl if c!="_"])
   
def possible(pzl,goal,width):
    pzl_inv = inversion_count(pzl)
    goal_inv = inversion_count(goal)
    if pzl_inv%2==goal_inv%2 and width%2==1:
       return True
    if width%2==0 and (pzl_inv+(pzl.index("_"))//width)%2==(goal_inv+(goal.index("_"))//width)%2:
       return True
    return False
def swap(l,a,b):
  n=list(l)
  temp = n[a]
  n[a] = n[b]
  n[b] = temp
  return ''.join(n)

def nbrs(puzzle,width):
    
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

def path_to_goal(goal,dctSeen):
   path_list = [goal]
   temp=goal
   while dctSeen[temp]!="": #temp!=startpzl
     if dctSeen[temp]:
        temp=dctSeen[temp]
        path_list.append(temp)
     else:
        return -1
        
   return path_list
def solve(pzl,goal,width):
    if not possible(pzl,goal,width): return []
    if pzl==goal: return [goal]
    parseMe = [(h(pzl,goal,width),pzl)]
    dctSeen = {pzl:""}
    while parseMe:
        parseMe.sort()
        node = parseMe.pop(0)[1]
        for nbr in nbrs(node,width):
            if nbr in dctSeen:continue
            dctSeen[nbr] = node
            parseMe.append((h(nbr,goal,width),nbr))
            if nbr==goal:
                return path_to_goal(goal,dctSeen)[::-1]
    # parseMe = [pzl]
    # dctSeen = {pzl:""}
    # while parseMe:
    #     node = parseMe.pop(0)
    #     for nbr in nbrs(node,width):
    #         if nbr not in dctSeen:
    #             if nbr == goal:
    #                 dctSeen[nbr] = node
    #                 return path_to_goal(goal,dctSeen)[::-1]
    #             dctSeen[nbr] = node
    #             parseMe.append(nbr)
def astar(root,goal,width):
   if not possible(root,goal,width):
      return []
   openSet = [(h(root,goal,width),root,"",0)]
   closedSet = {}
   while True:
      openSet.sort(reverse=True)
      pzl = openSet.pop()
      if pzl[1] in closedSet:
         continue
      closedSet[pzl[1]]=pzl[2]
      if pzl[1]==goal:
         return path_to_goal(goal,closedSet)[::-1]
      for nbr in nbrs(pzl[1],width):
         newF = h(nbr,goal,width) + pzl[3] + 1
         openSet.append((newF,nbr,pzl[1],pzl[3]+1))
   
def astar_buckets(root,goal,width):
   if not possible(root,goal,width):
      return []

   buckets = [[] for i in range(80)]
   currentF = h(root,goal,width)
   ptr = currentF
   openSet = [(currentF,root,"",0)]
   buckets[currentF].append(openSet[0])
   closedSet = {}
   while True:
      for bucket in buckets:
         if bucket:
            pzl = bucket.pop()
            break
      # openSet.sort(reverse=True)
      # pzl = openSet.pop()
      if pzl[1] in closedSet:
         continue
      closedSet[pzl[1]]=pzl[2]
      if pzl[1]==goal:
         return path_to_goal(goal,closedSet)[::-1]
      for nbr in nbrs(pzl[1],width):
         newF = h(nbr,goal,width) + pzl[3] + 1
         buckets[newF].append((newF,nbr,pzl[1],pzl[3]+1))

if __name__ == "__main__":
   start_time = time.time()
   puzzles_list = file_to_lines()
   goal = puzzles_list[0]
   _,width = find_h_w(goal)
   # for i,pzl in enumerate(puzzles_list):
   # c=1
   for pzl in puzzles_list:
         # print(i+1," ", pzl," ",condensed_path(astar(root=pzl,goal=goal,width=width),width=width))
         #temp_start_time = time.time() 
         path_to_return = condensed_path(astar_buckets(root=pzl,goal=goal,width=width),width=width)
         print(pzl," ",path_to_return)
         # temp_end_time = time.time() 
         # print(pzl," ",path_to_return,"{}s".format(round(temp_end_time-temp_start_time, 3 - len(str(temp_end_time-temp_start_time).split('.')[0]))))
         # c+=1
   end_time = time.time()
   

   print("Total Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))

#Shaurya Jain, pd 3, 2025
