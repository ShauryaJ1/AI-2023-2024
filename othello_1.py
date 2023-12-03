import sys; args = sys.argv[1:]
import math
import time 


def printBoard(boardString):
   print(*[boardString[i:i+8] for i in range(0,64,8)],sep="\n")
def print1DREP(boardString):
   print(boardString,str(boardString.lower().count('x'))+ '/'+str(boardString.lower().count('o')))
def makeMove(boardString):
   return ''

def determineMoves(boardString,tokenToPlay):
   opposite = 'x' if tokenToPlay == 'o' else 'x'
   board_list = list(boardString)
   possible_indices = [i for i,itm in enumerate(board_list) if itm=='.']
   moves= []
   for idx in possible_indices:
      directions_to_check = []
      for direction in directions:
            if direction[0] + idx + direction[1]*8<64 and board_list[direction[0] + idx + direction[1]*8]==opposite:
               directions_to_check.append(direction)
      for direction in directions_to_check:
         psblIdx = idx
         while psblIdx<64:
            psblIdx+=8
            if board_list[psblIdx] == opposite:
               continue
            elif(board_list[psblIdx]==tokenToPlay):
               moves.append(psblIdx)
               break
            else:
               break
               

   return moves,boardString

if __name__ == '__main__':
    if len(args)==0:
      board = '.'*27 + 'OX......XO' + '.'*27
      tokenToPlay = 'x'
    elif(len(args)==1):
      if args[0] in 'oxOX':
         tokenToPlay = args[0].lower()
         board = board = '.'*27 + 'OX......XO' + '.'*27
      else:
         board = args[0].lower()
         if((64-board.count('.'))%2==0):
            tokenToPlay = 'x'
         else:
            tokenToPlay = 'o'
    else:
       board = args[0].lower()
       tokenToPlay = args[1].lower()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    board = board.lower()
    moves,boardUpdated = determineMoves(board,tokenToPlay)
    printBoard(boardUpdated)
    print('\n')
    print1DREP(board)
    print(moves,'\n')

'''
testing boards:

'...................x.......xx......xo...........................'

'''
#Shaurya Jain, pd 3, 2025
