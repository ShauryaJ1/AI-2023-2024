import sys; args = sys.argv[1:]
import math
import time 
global h
global w
global num_squares
def file_to_lines():
    return open(args[2]).read().splitlines()
h,w = int(args[0][:args[0].index('x')]) ,int(args[0][1+args[0].index('x'):])
num_squares = int(args[1])
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
    if split_index:
        seedW, chars= split[:split_index[0]],split[split_index[0]:]
    else:
        seedW, chars = split , '#'
    return orientation,seedH,seedW,chars
def placeWord(xword_board,seedStringBreakdown):
    '''
    Accepts
        a crossword puzzle - string
        a seedStringBreakdown - tuple
    Returns
        a new crossword puzzle with the string having been placed - string
    '''
    placed = list(xword_board)
    orientation = seedStringBreakdown[0]
    seedStringHeight = int(seedStringBreakdown[1])
    seedStringWidth = int(seedStringBreakdown[2])
    charactersToPlace = seedStringBreakdown[3]
    startIndex = seedStringHeight*w + seedStringWidth
    if orientation == 'H':
        indices_to_change = [startIndex+i for i in range(len(charactersToPlace))]
    else:
        indices_to_change = [startIndex + i * w for i in range(len(charactersToPlace))]
    for char_idx,board_idx in enumerate(indices_to_change):
        placed[board_idx] = charactersToPlace[char_idx]
    return ''.join(placed)
def placeBlockingSquares(puzzle,num_squares):
    availables = [i for i in range(len(puzzle))if puzzle[i]=='-']
    puzzle_list= list(puzzle)
    for i in range(num_squares):
        puzzle_list[availables[i]] = '#'
    return ''.join(puzzle_list)

    

def printPuzzle(puzzle,h,w,num_squares):
    '''
    Accepts 
        a list of tuples of seedStringBreakdowns
        the height of the crossword h
        the width of the crossword w
        the number of blocking squares num_squares        

    Returns 
        the breakdowns in 2D cross word form
    '''
    # len_xword = int(h)*int(w)
    # non_blocking_squares = len_xword - int(num_squares)

    # xword_string = '#' * int(num_squares) + '-'*int(non_blocking_squares)
    
    return '\n'.join(puzzle[i*int(w):(i+1)*int(w)] for i in range(int(h)))
    
if __name__ == "__main__":
    # print(h,w,num_squares,seedStrings)
    puzzle = '-'*(h*w)
    breakdowns = []
    for seedString in seedStrings:
        breakdowns.append(seedStringBreakdown(seedString))

    for breakdown in breakdowns:
        puzzle = placeWord(puzzle,breakdown)
    print(placeBlockingSquares(printPuzzle(puzzle,h,w,int(num_squares)),num_squares))
#Shaurya Jain, pd 3, 2025
