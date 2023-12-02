import sys; args = sys.argv[1:]
import time
import math
import re
letters_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
def neighbors_generator(word):
    neighbors=[]
    letters = list(word)
    for idx in range(len(letters)):
        letters = list(word)
        for i in range(26):
            neighbors.append(swap_letters(letters,idx,i))
    return neighbors
def swap_letters(letters,a,b):
  temp = letters
  letters[a] = letters_list[b]
  return ''.join(temp)
def file_to_lines():
    return open(args[0]).read().splitlines()
def num_words_vertices(lines_list):
    return len(lines_list)

def BFS(root):
    parseMe = [root] #queue with root
    dctSeen = {root:""}

    while parseMe:
        prnt = parseMe.pop(0)
        nbrs = neighbors_generator(prnt)
        for nbr in nbrs:
            if nbr not in dctSeen:
                print("appending neighbor....",nbr)
                parseMe.append(nbr)
                dctSeen[nbr]=prnt
    return dctSeen
def file_to_lines():
    return open(args[0]).read().splitlines()
def num_words_vertices(lines_list):
    return len(lines_list)
if __name__=='__main__':
    start_time=time.time()
    lines = file_to_lines()
      
    end_time=time.time()
    print(num_words_vertices(lines))
    # print(lines[:5])
    print("Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))

#Shaurya Jain, pd 3, 2025