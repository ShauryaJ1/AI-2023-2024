import re
import sys; args = sys.argv[1:]

if __name__ == '__main__':
    args_joined = ' ' +' '.join(args) + ' '
    # print(args_joined)
    if(t:=re.search("\s[xo]\s",args_joined,re.I)):
        print(t.group()[1])
    
    if (b:= re.search("[x.o]{64}",' '.join(args))):
       board = b.group().lower()
       print(board)
    if(m:= re.findall("([a-h][1-8])|([^a-z][0-9]{1,2})",' '.join(args))):
        moves = [(itm1 + itm2).replace(" ",'') for itm1,itm2 in m] 
        print(moves)

#Shaurya Jain, pd 3, 2025