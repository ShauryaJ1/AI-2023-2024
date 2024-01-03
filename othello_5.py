import sys; args = sys.argv[1:]
import math
import time 
import re
global directions
global board
global tokenToPlay
global corners
global next_to_corners
global edges
global edge_lists
corners = {0,7,63,56}
next_to_corners = {0:[1,8,9],7:[15,6,14],63:[62,55,54],56:[57,48,49]}
directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
edges = [[0,1,2,3,4,5,6,7],[56,57,58,59,60,61,62,63],[0,8,16,24,32,40,48,56],[7,15,23,31,39,47,55,63]]

edge_lists = {idx:edge for edge in edges for idx in edge if idx not in corners}

# print(edge_lists)
def checkEdge(brd,tkn,move):
    move_idx = edge_lists[move].index(move)
    # print(move_idx)
    slice_1 = ''.join(brd[idx] for idx in edge_lists[move][:move_idx])
    slice_2 = ''.join(brd[idx] for idx in edge_lists[move][move_idx+1:])
    if slice_1 == len(slice_1)*tkn or slice_2 ==len(slice_2)*tkn:
        return True
    return False
def mobility(brd,tkn,p_moves):
    opposite = 'x' if tkn == 'o' else 'o'
    lens = []
    for move in p_moves:
        p_brd = determineMovesAndPlay(brd,tkn,opposite,move)
        o_moves,_ = determineMoves(p_brd,opposite)
        lens.append((len(o_moves),move))
    return min(lens)[1]
# printBoard('...ooo.x..oxxxx.xxoxxoooxxoxxoooxoxxoxxoooooooxo..xxoxxx..x.ooxx')

def quickMove(brd,tkn):
    '''
    Implementing move to empty corners
    Implementing don't move around enemy or empty corners
    Implementing move to safe edges
    Implementing mobility
    '''
    p_moves,_ = determineMoves(brd,tkn)
    
    if p_moves:
        for move in p_moves:
            if move in corners:
                return move
        opposite = 'x' if tkn == 'o' else 'o'
        opps = []
        # yours = []
        for corner in corners:
            if brd[corner]==opposite or brd[corner]=='.':
                opps+=next_to_corners[corner]
            # else:
            #     yours+=next_to_corners[corner]
        if (s:=p_moves-p_moves.intersection(set(opps))):
            p_moves = s
        for move in p_moves:
            if move in edge_lists:
                if checkEdge(brd,tkn,move):
                    return move
            # if move in yours:
            #     return move
        
        return mobility(brd,tkn,p_moves)
    else: return ''
    # return [*p_moves][0]
def printBoard(boardString):
   print(*[boardString[i:i+8] for i in range(0,64,8)],sep="\n")

# printBoard('...ooo.x..oxxxx.xxoxxoooxxoxxoooxoxxoxxoooooooxo..xxoxxx..x.ooxx')

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
            if psblIdx>=0 and psblIdx<64 and abs(prevIdx%8-psblIdx%8)<=1:
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
        
   return set(moves),''.join(board_list)

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

def negamax(brd,tkn):
    eTkn = 'x' if tkn == 'o' else 'o'
    if brd.count('.')==0:
        return [brd.count(tkn)-brd.count(eTkn)]
    
    p_moves,_ = determineMoves(brd,tkn)
    if len(p_moves)==0:
        if len(determineMoves(brd,eTkn)[0])==0:
            return [brd.count(tkn)-brd.count(eTkn)]
        nm = negamax(brd,eTkn)
        bestSoFar = [-nm[0]] + nm[1:] + [-1]
        return bestSoFar
    bestSoFar = [-65]
    for mv in p_moves:
        newBrd = determineMovesAndPlay(brd,tkn,eTkn,mv).lower()
        nm = negamax(newBrd,eTkn)
        if -nm[0]>bestSoFar[0]:
            bestSoFar = [-nm[0]] + nm[1:] + [mv]
        
    return bestSoFar
def main():
    # args = ['442919102113_12618_237_0172416_81415_3_4_720_5_611222532_934123847304223333945404143504654495351564859526055316162']
    moves_to_return = []
    a_moves = []
    board = ''
    tokenToPlay = ''
    args_joined = ' ' +' '.join(args) + ' '
    if(t:=re.search("\s[xoXO)]\s",args_joined)):
        tokenToPlay = t.group()[1]
    if (b:= re.search("[OXx.o]{64}",' '.join(args))):
       board = b.group().lower()
       
    for arg in args:
        if 'x' not in arg.lower() and 'o' not in arg.lower():
            a_moves.append(arg)
    for a_move in a_moves:
        if len(a_move)<=2:
            if a_move[0] in ['A','B','C','D','E','F','G','H']:
                moves_to_return.append(ord(a_move[0])-65+8*(int(a_move[1])-1))
            elif a_move[0] == '_':
                moves_to_return.append(int(a_move[1]))
            elif(64>int(a_move)>=0):
                moves_to_return.append(int(a_move))
        else:
            splits = [a_move[i:i+2] for i in range(0,len(a_move),2)]
            for split in splits:
                
                if split[0] == '_':
                    moves_to_return.append(int(split[1]))
                elif(64>int(split)>=0):
                    moves_to_return.append(int(split))
    
    
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
    BRD = board
    TKN = tokenToPlay
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
            f_moves,boardUpdated  = determineMoves(board,opposite)
            print(f"Possible moves for {opposite}:",*set(f_moves),'\n')
            tokenToPlay = opposite
            opposite = 'x' if tokenToPlay == 'o' else 'o'

    
    
   
    # print(a_moves)
    for a_move in moves_to_return:
        
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
   
    if len(determineMoves(BRD,TKN)[0])<=10:
        neg = negamax(BRD,TKN)
        min_score,moves_seq = neg[0],neg[1:]
        print(f"My move is {moves_seq[-1]}")
        print(f"Min score: {min_score}; move sequence: {moves_seq}")
if __name__ == '__main__':
    main()
    # print(mobility('.'*27 + 'OX......XO' + '.'*27,'x',{26,19,44,37}))

        

#Shaurya Jain, pd 3, 2025
