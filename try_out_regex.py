import re
import sys; args = sys.argv[1:]

if __name__ == '__main__':
    # args_joined = ' ' +' '.join(args) + ' '
    # # print(args_joined)
    # if(t:=re.search("\s[xo]\s",args_joined,re.I)):
    #     print(t.group()[1])
    
    # if (b:= re.search("[x.o]{64}",' '.join(args))):
    #    board = b.group().lower()
    #    print(board)
    # if(m:= re.findall("([a-h][1-8])|([^a-z][0-9]{1,2})",' '.join(args))):
    #     moves = [(itm1 + itm2).replace(" ",'') for itm1,itm2 in m] 
    #     print(moves)
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

#Shaurya Jain, pd 3, 2025