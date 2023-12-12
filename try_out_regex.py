import re
import sys; args = sys.argv[1:]

if __name__ == '__main__':
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
    
    board = board.lower()
    print(board,tokenToPlay,moves_to_return)
#Shaurya Jain, pd 3, 2025