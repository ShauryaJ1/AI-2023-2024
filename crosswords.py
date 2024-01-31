import sys; args = sys.argv[1:]
import math
import time 
global h
global w
global num_squares
def file_to_lines():
    return open(args[2]).read().splitlines()
h,w = args[0][:args[0].index('x')] ,args[0][1+args[0].index('x'):]
num_squares = args[1]
dict_list = file_to_lines()
seedStrings = ""
if len(args)>3:
    seedStrings = args[3:]


'''
Place only symmetrically
Check 3s rule
Make a function to check symmetry



'''
def seedStringBreakdown(seedString):
    '''
    Accepts a seedString as an argument
    Returns a tuple of:
        orientation(H or V) - string
        seedstring height - string
        seedstring width - string
        characters - string
    '''
    orientation  = seedString[0]
    seedH, split = seedString[1:seedString.index('x')], seedString[seedString.index('x')+1:]
    # print(seedH,split)
    split_index = [c for c,i in enumerate(split) if ord(i) not in {48,49,50,51,52,53,54,55,56,57}] #not gonna work because if chars doesnt exist it will break
    # print(split_index)
    if split_index:
        seedW, chars= split[:split_index[0]],split[split_index[0]:]
    else:
        seedW, chars = split[:split_index] , split[split_index+1:]
    return orientation,seedH,seedW,chars
    
def printPuzzle(seedStringBreakdowns,h,w,num_squares):
    '''
    Accepts 
        a list of tuples of seedStringBreakdowns
        the height of the crossword h
        the width of the crossword w
        the number of blocking squares num_squares        

    Prints 
        the breakdowns in 2D cross word form
    '''
    len_xword = int(h)*int(w)
    print(len_xword)
    non_blocking_squares = len_xword - int(num_squares)

    xword_string = '#' * int(num_squares) + '_'*int(non_blocking_squares)
    
    print('\n'.join(xword_string[i*int(w):(i+1)*int(w)] for i in range(int(h))))
    
if __name__ == "__main__":
    # print(h,w,num_squares,seedStrings)
    breakdowns = []
    for seedString in seedStrings:
        breakdowns.append(seedStringBreakdown(seedString))

    printPuzzle(breakdowns,h,w,num_squares)
#Shaurya Jain, pd 3, 2025
