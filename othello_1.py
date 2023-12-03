import sys; args = sys.argv[1:]
import math
import time 


def printBoard(boardString):
   print(*[boardString[i:i+8] for i in range(0,64,8)],sep="\n")

def makeMove(boardString):
   return ''

def determineMoves(boardString):
   return ''


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
       board = args[0]
       tokenToPlay = args[1]
    printBoard(board)

#Shaurya Jain, pd 3, 2025