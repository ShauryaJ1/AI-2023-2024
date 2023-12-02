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
    vd = abs((pzl.index(c)//width)-(goal.index(c)//width))
    hd = abs((pzl.index(c)%width)-(goal.index(c)%width))
    return hd+vd
def h(pzl,goal,width):
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
def astar(root,goal,width):
   if not possible(root,goal,width):
      return []
   openSet = [(h(root,goal,width),root,"",0)]
   # print(h(root,goal,width))
   closedSet = {}
   while True:
      openSet.sort()
      pzl = openSet.pop(0)
      if pzl[1] in closedSet:
         continue
      closedSet[pzl[1]]=pzl[2]
      if pzl[1]==goal:
         return path_to_goal(goal,closedSet)[::-1]
      for nbr in nbrs(pzl[1],width):
         newF = h(nbr,goal,width) + pzl[3] + 1
         # print(newF)
         openSet.append((newF,nbr,pzl[1],pzl[3]+1))

def astar_modified(root,goal,width):
   if not possible(root,goal,width):
      return []
   currentF = h(root,goal,width)
   openSet = [[] for i in range(80)]
   openSet[currentF].append((h(root,goal,width),root,"",0))
   closedSet = {}
   while True:
      if not openSet[currentF]:
         currentF+=2
      pzl = openSet[currentF][0]
      openSet[currentF] = openSet[currentF][1:]
      if pzl[1] not in closedSet:
         closedSet[pzl[1]]=pzl[2]
      if pzl[1]==goal:
         return path_to_goal(goal,closedSet)[::-1]
      for nbr in nbrs(pzl[1],width):
         newF = h(nbr,goal,width) + pzl[3] + 1
         # print(newF)
         openSet[currentF].append((newF,nbr,pzl[1],pzl[3]+1))
      

if __name__ == "__main__":
   if len(args)==1:
      start_time = time.time()
      puzzles_list = file_to_lines()
      goal = puzzles_list[0]
      _,width = find_h_w(goal)
      # for i,pzl in enumerate(puzzles_list):
      # c=1
      for pzl in puzzles_list:
         # print(i+1," ", pzl," ",condensed_path(astar(root=pzl,goal=goal,width=width),width=width))
         print(pzl," ",condensed_path(astar_modified(root=pzl,goal=goal,width=width),width=width))
         # c+=1
      end_time = time.time()
      print("Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))
   else:
      start_time = time.time()
      pzl=args[0]
      goal = args[1]
      _,width = find_h_w(goal)
      print(pzl," ",condensed_path(astar(root=pzl,goal=goal,width=width),width=width))
      end_time = time.time()
      print("Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))
    # print(h("ABCDEFGHIJKLMNO_","BECDAFHKI_NLMGJO","E",width=4))
#Shaurya Jain, pd 3, 2025
