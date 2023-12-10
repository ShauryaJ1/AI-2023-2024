import sys; args = sys.argv[1:]
import math
import time 
import re


def printBoard(boardString):
   print(*[boardString[i:i+8] for i in range(0,64,8)],sep="\n")
def print1DREP(boardString):
   boardString = removeAsterisk(boardString.lower())
   print(boardString,str(boardString.lower().count('x'))+ '/'+str(boardString.lower().count('o')))
def removeAsterisk(boardString):
    return boardString.replace('*','.')

def makeMove(boardString):
   return ''

def determineMoves(boardString,tokenToPlay):
   opposite = 'x' if tokenToPlay == 'o' else 'o'
#    print(opposite)
   board_list = list(boardString.lower())
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

def determineMovesAndPlay(boardString,tokenToPlay, opposite,move_idx):
      possible_moves = []
      board_list = list(boardString.lower())
      directions_to_check = []
      for direction in directions:
            
            if 0<=(direction[1] + move_idx + direction[0]*8)<64 and board_list[direction[1] + move_idx + direction[0]*8]==opposite:
            #    print(idx, direction[1] + idx + direction[0]*8)
               directions_to_check.append(direction)
    #   if directions_to_check:
    #      print(directions_to_check)
      flips = []
      for direction in directions_to_check:
         prevIdx = move_idx
         psblIdx = move_idx
        #  print(direction)
         p_flips = []
         while psblIdx<64:
            prevIdx = psblIdx
            psblIdx+=8*direction[0] + 1*direction[1]
            # print(psblIdx,prevIdx, abs(prevIdx%8-psblIdx%8))
            if psblIdx>=0 and psblIdx<64 and abs(prevIdx%8-psblIdx%8)<=1:
                # print('uo')
                   
                if board_list[psblIdx] == opposite:
                    #  print(psblIdx, 'continue')
                     p_flips.append(psblIdx)
                     continue
                elif(board_list[psblIdx]==tokenToPlay):
                    # print(psblIdx,'STOP')
                    flips+=p_flips
                    possible_moves.append(move_idx)
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
    #   for p_move in possible_moves:
    #     board_list[p_move] = '*'
      for flip in flips:
        board_list[flip] = tokenToPlay
      board_list[move_idx] = tokenToPlay.upper()
      return ''.join(board_list)



if __name__ == '__main__':
    start_time = time.time()
    a_moves = []
    board = ''
    tokenToPlay = ''
    args_joined = ' ' +' '.join(args) + ' '
    if(t:=re.search("\s[xoXO)]\s",args_joined)):
        tokenToPlay = t.group()[1]
    if (b:= re.search("[OXx.o]{64}",' '.join(args))):
       board = b.group().lower()
       
    if(m:= re.findall("([a-h][1-8])|([^a-z][0-9]{1,2})",' '.join(args))):
        a_moves = [(itm1 + itm2).replace(" ",'').lower() for itm1,itm2 in m]
        a_moves_all_nums = []
        for move in a_moves:
            if any(c.isalpha() for c in move):
                # print(ord(move[0])-97+8*(int(move[1]))-1)
                a_moves_all_nums.append(ord(move[0])-97+8*(int(move[1])-1))
            
            else:
                a_moves_all_nums.append(move)
        a_moves = [int(move) for move in a_moves_all_nums if int(move)>=0]
        
    
    
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
    # tokenToPlay = 'x'
    # tokenToPlay = 'o'
    # board = '.'*27 + 'OX......XO' + '.'*27
    # board = 'oooo.oooxooooooo.xooooooooxxooooooxxxoxxoooxoxx.oooooxx.ooooo...'
    # a_moves = [37, 45, 44, 43, 51, 21, 46, 59, 26, 42, 20, 19, 10, 18, 49, 56, 34, 29, 9, 2, 14, 7, 22, 15, 13, 6, 41, 48, 1, 0, 12, 5 ,58, 57, 11 ,3 ,33 ,40 ,25 ,50 ,52 ,60 ,23 ,31 ,32 ,24 ,53 ,38 ,54 ,17 ,39 ,30 ,8 ,16 ,4 ,63 ,55 ,47 ,61 ,62]
    # a_moves =[16]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    # print(board,a_moves,tokenToPlay)
    board = board.lower()
    f_moves,boardUpdated = determineMoves(board,tokenToPlay)
    printBoard(boardUpdated)
    print('\n')
    print1DREP(board)
    opposite = 'x' if tokenToPlay == 'o' else 'o'
    if f_moves:
            print(f"Possible moves for {tokenToPlay}:",*set(f_moves),'\n')
    else:
            print(f"No moves possible for {tokenToPlay}",'\n')
            tokenToPlay = opposite
            opposite = 'x' if tokenToPlay == 'o' else 'o'
    
    
    # for a_move in a_moves:
    #     board = determineMovesAndPlay(board.lower(),tokenToPlay,opposite,a_move)
    #     moves,board = determineMoves(board,opposite)
    #     print(f"{tokenToPlay} plays to {a_move}")
    #     printBoard(board)
    #     print('\n')
    #     print1DREP(board)
    #     if moves:
    #         print(f"Possible moves for {opposite}:",*set(moves),'\n')
    #         tokenToPlay = opposite
    #         opposite =  'x' if tokenToPlay == 'o' else 'o'
    #         board = removeAsterisk(board)
    #     else:
    #         print(f"No moves possible for {opposite}",'\n')
    #         moves,board = determineMoves(board,tokenToPlay)
    #         board = removeAsterisk(board)
    #         if moves:
    #             print(f"Possible moves for {tokenToPlay}:",*set(moves),'\n')
    #         else:
    #             print(f"No moves possible for {tokenToPlay}\nGame Over")
    print(a_moves)
    for a_move in a_moves:
        
        print(f"{tokenToPlay} plays to {a_move}")
        new_board = determineMovesAndPlay(board,tokenToPlay,opposite,a_move)
        opposite_moves, board_2 = determineMoves(new_board,tokenToPlay=opposite)
        printBoard(board_2)
        print('\n')
        print1DREP(board_2)
        if opposite_moves:
            print(f"Possible moves for {opposite}:",*set(opposite_moves),'\n')
            tokenToPlay = opposite
            opposite = 'x' if tokenToPlay == 'o' else 'o'
            board = removeAsterisk(board_2.lower())
        else:
            print(f"No moves possible for {opposite}")
            moves, board_2 = determineMoves(removeAsterisk(board_2.lower()),tokenToPlay)
            if moves:
                print(f"Possible moves for {tokenToPlay}:", *set(moves))
                board = removeAsterisk(board_2.lower())
            else:
                print(f"No moves possible for {tokenToPlay}\nGameOver")

    
        

        

#Shaurya Jain, pd 3, 2025

#Shaurya Jain, pd 3, 2025
