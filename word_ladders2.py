import sys; args = sys.argv[1:]
import time
import math
import re
import random


def neighbors_generator(word):
    neighbors=[]
    for letter_pos in range(26):
        for word_pos in range(6):
            new_word = replace_letters(word,word_pos,letter_pos)
            if new_word in words_set and new_word!=word:
                neighbors.append(new_word)
    return list(set(neighbors))
def replace_letters(word,word_pos,letters_pos):
  temp = list(word)
  temp[word_pos] = letters_list[letters_pos]
  return ''.join(temp)
def file_to_lines():
    return open(args[0]).read().splitlines()


def BFS(root):
    parseMe = [root] #queue with root
    dctSeen = {root:""}
    while parseMe:
        prnt=parseMe.pop(0)
        neighbors = neighbors_generator(prnt)
        for nbr in neighbors:
            if nbr not in dctSeen:
                parseMe.append(nbr)
                dctSeen[nbr] = prnt          
    return dctSeen
def path_func(start,goal,dctSeen):
   path_list = [goal]
   temp=goal
   while temp!=start:
     if dctSeen[temp]:
        temp=dctSeen[temp]
        path_list.append(temp)
     else:
        return -1
        
   return path_list
def degree_counter(word,dctSeen):
    return sum([1 for key in dctSeen if dctSeen[key]==word]) + 1
def check_one_letter_different(word1,word2):
    return [True if c1==c2 else False for c1,c2 in zip(word1,word2)].count(False)==1
def edge_counting(lines):
    count=0
    for li,word1 in enumerate(lines):
        for word2 in lines[li+1:]:
            if check_one_letter_different(word1=word1,word2=word2):
                count+=1 
    return count
    
def degree_distribution():
    degrees = {word:neighbors_generator(word) for word in lines}
    degrees_list=[]
    edge_count=0
    for word in lines:
        nbrs_len = len(degrees[word])
        degrees_list.append(nbrs_len)
        edge_count+=nbrs_len
    return [edge_count//2,[degrees_list.count(i) for i in set(degrees_list)]]

def second_highest_degree_word():
    
    degrees = {word:neighbors_generator(word) for word in lines}
    degrees_list=[]
    for word in lines:
        degrees_list.append(len(degrees[word]))
    second_highest_degree = list(set(degrees_list))[-2]
    for word in degrees:
        if len(degrees[word])==second_highest_degree:
            return word
def farthest_path(start,dctSeen):
    paths = []
    max_node=''
    max_path=0
    for node in dctSeen:
        if max_path<(b:=len(path_func(start,node,dctSeen))):
            max_node=node
            max_path=b
    return max_node
    # return max([len(path_func(start,node,dctSeen)) for node in dctSeen])
def connected_component_sizes():
    temp_set = set(lines)
    cluster_dict={}
    while temp_set:
        node = temp_set.pop()
        dct = BFS(node)
        cluster_set = set(dct)
        cluster_dict[node]=cluster_set
        for item in cluster_set:
            temp_set.discard(item)
    return cluster_dict
def k_counter(ccs,k):
    count=0
    for key in ccs:
        if len(ccs[key])==k:
            count+=all([len(neighbors_generator(word))==k-1 for word in ccs[key]])
    return count
    

if __name__=='__main__':
    
    
    if len(args)==1:
        start_time = time.time()
        letters_list = ['a','b','c','d','e',
                    'f','g','h','i','j',
                    'k','l','m','n','o',
                    'p','q','r','s','t',
                    'u','v','w','x','y',
                    'z']
        lines = file_to_lines()
        words_set = set(lines)
        len_lines = len(lines)
        
        
        node_count = len_lines
        edges_and_degree_distribution = degree_distribution()
        # edge_count = edge_counting(lines)

        print("Word count: ",node_count)
        print("Edge count: ", edges_and_degree_distribution[0])
        print("Degree List: ", edges_and_degree_distribution[1])
        
        # print("Degree list: ", degree_distribution())
        # print(part_1_combined())
        end_time=time.time()
        # print(dctSeen)
        print("Construction Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))
    if len(args)>1:
        start_time=time.time()
        letters_list = ['a','b','c','d','e',
                    'f','g','h','i','j',
                    'k','l','m','n','o',
                    'p','q','r','s','t',
                    'u','v','w','x','y',
                    'z']
        lines = file_to_lines()
        words_set = set(lines)
        len_lines = len(lines)
        
        print("Second Degree Word: ", second_highest_degree_word())
        # print("Connected Component Size: ", connected_component_sizes())
        print("Neighbors: ", neighbors_generator(args[1]))
        
        start = args[1]
        goal = args[2]
        dctSeen = BFS(start)
        path=path_func(start,goal,dctSeen)
        ccs = connected_component_sizes()
        
        intermediate = [len(ccs[key]) for key in ccs]
        
        distinct_sizes=len(set(intermediate))

        k2s = intermediate.count(2)
        k3s = k_counter(ccs,3)
        k4s = k_counter(ccs,4)
        print("Connected Component Size Count: ", distinct_sizes)
        print("Largest Component Size: ", max(intermediate))
        print("K2 Count: ", k2s)
        print("K3 Count: ", k3s)
        print("K4 Count: ", k4s)
        print("Farthest: ", farthest_path(start,dctSeen))
        print("Path: ", path[::-1])
        end_time=time.time()
        print("Construction Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))
#Shaurya Jain, pd 3, 2025