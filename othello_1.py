import sys; args = sys.argv[1:]
import math
import time 

import time
def printBoard(boardString):
   print(*[boardString[i:i+8] for i in range(0,64,8)],sep="\n")
def print1DREP(boardString):
   print(boardString,str(boardString.lower().count('x'))+ '/'+str(boardString.lower().count('o')))
def makeMove(boardString):
   return ''

def determineMoves(boardString,tokenToPlay):
   opposite = 'x' if tokenToPlay == 'o' else 'o'
#    print(opposite)
   board_list = list(boardString)
   possible_indices = [i for i,itm in enumerate(board_list) if itm=='.']
#    print(len(possible_indices))
   moves= []
   for idx in possible_indices:
      directions_to_check = []
      for direction in directions:
            
            if 0<=(direction[1] + idx + direction[0]*8)<64 and board_list[direction[1] + idx + direction[0]*8]==opposite:
            #    print(idx, direction[1] + idx + direction[0]*8)
               directions_to_check.append(direction)
    #   if directions_to_check:
    #      print(directions_to_check)
      for direction in directions_to_check:
         prevIdx = idx
         psblIdx = idx
        #  print(direction)
         
         while psblIdx<64:
            prevIdx = psblIdx
            psblIdx+=8*direction[0] + 1*direction[1]
            # print(psblIdx,prevIdx, abs(prevIdx%8-psblIdx%8))
            if psblIdx>0 and psblIdx<64 and abs(prevIdx%8-psblIdx%8)<=1:
                # print('uo')
                   
                if board_list[psblIdx] == opposite:
                    #  print(psblIdx, 'continue')
                     continue
                elif(board_list[psblIdx]==tokenToPlay):
                    # print(psblIdx,'STOP')
                    moves.append(idx)
                    break
                # elif(psblIdx%8==0):
                #    break
                # elif(psblIdx%8==7):
                #    break
                else:
                    # print('STOP')
                    break

            else:
               break
   for move in moves:
      board_list[move] = '*'
        
   return moves,''.join(board_list)

if __name__ == '__main__':
    start_time = time.time()
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
    if moves:
        print(f"Possible moves for {tokenToPlay}:",*set(moves),'\n')
    else:
       print("No moves possible")
    print(f"Time: {time.time()-start_time:.3g}s")
'''
testing boards:

'...................x.......xx......xo...........................'


'''
#Shaurya Jain, pd 3, 2025
