import sys;args= sys.argv[1:]

import sys; args = sys.argv[1:]
import time

global board
board = ""

global width
global height


global finSet 

finSet = set()

import math
width = 0
height = 0
for arg in args:
    if len(arg) >1:
        board = arg
        finSet.add(board)
    else:
        width = int(arg)

if not width:
    steps=0
    height,width=0,0
    for i in range(1,int(math.sqrt(len(board))+1)):
        if len(board)%i==0:
            height=i
            width=len(board)//i




def q1display(pzl):
   startIndeces = [q for q in range(0,len(pzl),width) ]
   listed = []
   for q in startIndeces:
       listPuzzle = list(pzl)
       theThing  = listPuzzle[q: q+width]
       listed.append(''.join(theThing))
  


   if len(listed) ==0:
       print("No solution found")
   else:
       for i in listed:
           print (i)


def clockwise(brd,height,width):
    brd_list= list(brd)
    new_brd_list = [0]*len(brd)
    for i in range(len(brd)):
        col = i%8
        row = i//8
        print(col*int(height)+int(height)-col-1)
        new_brd_list[col*int(height)+ col*(width-row-1)] = brd_list[i]
    return ''.join(new_brd_list)
# q1display(clockwise(board,height,width))
print(clockwise(board,height,width))


