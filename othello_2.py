import sys; args = sys.argv[1:]
import math
import time 
import re

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
def makeMove(board,tokenToPlay,choice):
    board_list = list(board)
    flips = []
    opposite = 'x' if tokenToPlay == 'o' else 'o'
    r_moves = []
    directions_to_check = []
    for direction in directions:
            
            if 0<=(direction[1] + choice + direction[0]*8)<64 and board_list[direction[1] + choice + direction[0]*8]==opposite:
            #    print(idx, direction[1] + idx + direction[0]*8)
               directions_to_check.append(direction)
    
    for direction in directions_to_check:
         prevIdx = choice
         psblIdx = choice
        #  print(move)
         p_flips = []
         while psblIdx<64:
            prevIdx = psblIdx
            psblIdx+=8*direction[0] + 1*direction[1]
            
            # print(psblIdx,prevIdx, abs(prevIdx%8-psblIdx%8))
            if psblIdx>0 and psblIdx<64 and abs(prevIdx%8-psblIdx%8)<=1:
                # print('uo')
                   
                if board_list[psblIdx] == opposite:
                    #  print(psblIdx, 'continue')
                    p_flips.append(psblIdx)
                    continue
                elif(board_list[psblIdx]==tokenToPlay):
                    # print(psblIdx,'STOP')
                    r_moves.append(choice)
                    print(r_moves)
                    print(p_flips)
                    flips += p_flips
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
    for r_move in r_moves:
            board_list[r_move] = '*'
    if flips:
        print(flips)
        for flip in flips:
                board_list[flip] = tokenToPlay

    return ''.join(board_list), tokenToPlay
    
if __name__ == '__main__':
    moves = []
    board = ''
    tokenToPlay = ''
    args_joined = ' ' +' '.join(args) + ' '
    if(t:=re.search("\s[xo]\s",args_joined,re.I)):
        tokenToPlay = t.group()[1]
    if (b:= re.search("[x.o]{64}",' '.join(args))):
       board = b.group().lower()
       
    if(m:= re.findall("([a-h][1-8])|([^a-z][0-9]{1,2})",' '.join(args))):
        moves = [(itm1 + itm2).replace(" ",'').lower() for itm1,itm2 in m]
        moves_all_nums = []
        for move in moves:
            if any(c.isalpha() for c in move):
                moves_all_nums.append((ord(move[0])-97)*8+int(move[1])-1)
            
            else:
                moves_all_nums.append(move)
        moves = [abs(int(move)) for move in moves_all_nums]
        
    
    
    if not tokenToPlay:
        if not board:

            tokenToPlay = 'x'
            board = '.'*27 + 'OX......XO' + '.'*27
        else:
            if((64-board.count('.'))%2==0):
                tokenToPlay = 'x'
            else:
                tokenToPlay = 'o'

    if not board:
        board = '.'*27 + 'OX......XO' + '.'*27


    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    # if (m:= re.search("[x.o]{64}",' '.join(args))):
    #    board = m.group().lower()
    # board = re.search("[x.o]{64}",' '.join(args)).group().lower()
    print(moves,board, tokenToPlay)
    if moves:
        out_moves,boardUpdated = determineMoves(board,tokenToPlay)
        printBoard(boardUpdated)
        print('\n')
        print1DREP(board)
        if out_moves: 
            print(f"Possible moves for {tokenToPlay}:",*set(out_moves),'\n')
        else:
            print("No moves possible")
        opposite = 'x' if tokenToPlay == 'o' else 'o'

        opposite,boardUpdated = makeMove(board,opposite,moves[0])
        printBoard(opposite)
        
    else:
        out_moves,boardUpdated = determineMoves(board,tokenToPlay)
        
        printBoard(boardUpdated)
        print('\n')
        print1DREP(board)
        if out_moves: 
            print(f"Possible moves for {tokenToPlay}:",*set(out_moves),'\n')
        else:
            print("No moves possible")

        
    
'''
testing boards:

'...................x.......xx......xo...........................'


'''
#Shaurya Jain, pd 3, 2025
