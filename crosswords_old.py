import sys; args = sys.argv[1:]
import math
import time 
global h
global w
global num_squares
global symmetrical_lookup
global alphabetString

# args=[ '13x13', 32, 'Eckel.txt' ,'H1x4#Toe#', 'H9x2#' ,'V3x6#', 'H10x0Scintillating', 'V0x5stirrup' ,'H4x2##Ordained' ,'V0x1Ward' ,'V0x12Lis', 'V5x0orb']
def file_to_lines():
    return open(args[2]).read().splitlines()
alphabetString = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
h,w = int(args[0][:args[0].index('x')]) ,int(args[0][1+args[0].index('x'):])
num_squares = int(args[1])
dict_list = file_to_lines()
seedStrings = ""
if len(args)>3:
    seedStrings = args[3:]

positions = [i for i in range(h*w)]
p1 = 0
p2 = h-1
splits = [positions[i:i+w][::-1] for i in range(0,h*w,w)]
while p1<=p2:
        temp = splits[p1]
        splits[p1] = splits[p2]
        splits[p2] = temp
        p1+=1
        p2-=1
reversed = []
for s in splits:
    reversed+=s
symmetrical_lookup = {i:v for i,v in enumerate(reversed)}

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
    minus_count = 0
    '''
    Accepts
        a crossword puzzle - string
        a seedStringBreakdown - tuple
    Returns
        a new crossword puzzle with the string having been placed - string
        a minusCount which is how many blocks need to be subtracted given the number of them submitted via grader input
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
        if charactersToPlace[char_idx] =='#':
            # print(placed)
            placed,ni,ad = placeBlockingSquaresSpacing(''.join(placed),num_squares,{},board_idx)
            placed = list(placed)
        else:
            placed[board_idx] = charactersToPlace[char_idx]

    # if '#' in charactersToPlace:
    #     block_indices = [i for i in range(len(charactersToPlace)) if charactersToPlace[i]=='#']
    #     for i in block_indices:
    #         placed,_,_ = placeBlockingSquaresSpacing(''.join(placed),num_blocks,{},i)
    #         placed = list(placed)
    #         if symmetrical_lookup[indices_to_change[i]] != indices_to_change[i]:
    #             minus_count+=1
    #         placed[symmetrical_lookup[indices_to_change[i]]] = '#'
    # print(printPuzzle(''.join(placed),h,w,0))
    return ''.join(placed),minus_count
def placeBlockingSquaresBasic(puzzle,num_squares):
    '''
    Doesnt do anything special...just puts the blocks down
    '''
    availables = [i for i in range(len(puzzle))if puzzle[i]=='-']
    puzzle_list= list(puzzle)
    for i in range(num_squares):
        puzzle_list[availables[i]] = '#'
    return ''.join(puzzle_list) 
def rotation(puzzle):
    '''
    Finds the rotation of the puzzle
    '''
    p1 = 0
    p2 = h-1
    splits = [puzzle[i:i+w][::-1] for i in range(0,h*w,w)]
    while p1<=p2:
        temp = splits[p1]
        splits[p1] = splits[p2]
        splits[p2] = temp
        p1+=1
        p2-=1
    return ''.join(splits)
def onlyBlocks(puzzle):
    '''
    Removes all characters that are not blocks
    '''
    puzzle_list = list(puzzle)
    for i in range(len(puzzle_list)):
        if puzzle_list[i]!='#':
            puzzle_list[i] = '-'
    return ''.join(puzzle_list)
def isInvalid(puzzle):
    '''
    Only checks if the rotation of the onlyBlocks form of the puzzle is the same as the original puzzle
    '''
    return onlyBlocks(puzzle) != onlyBlocks(rotation(puzzle))
def placeBlockingSquares(puzzle,num_blocks,availables):  
    if isInvalid(puzzle):
        return ''  
    if num_blocks == 0:
        return puzzle
    if num_blocks==1:
        for i in symmetrical_lookup:
            if symmetrical_lookup[i] == i:
                new_puzzle = list(puzzle)
                new_puzzle[i] = '#'
                return ''.join(new_puzzle)
    for choice in availables:
        sub_pzl = list(puzzle)
        sub_pzl[choice] = '#'
        sub_pzl[symmetrical_lookup[choice]] = '#'
        bF = placeBlockingSquares(''.join(sub_pzl),num_blocks-2,availables-{choice,symmetrical_lookup[choice]})
        if bF:
            return bF
    

    return ''
def placeBlockingSquaresSpacing(puzzle,num_blocks,availables,space):
    '''
    Accepts:
        Puzzle, Blocks, Available Spaces, Chosen Space to place
    Returns:
        a semi-complete or complete puzzle
    '''
    # if symmetrical_lookup[space] != '-':
    #     return ''
    width = w
    height = h
    new_puzzle = list(puzzle)
    add_count = 0
    newly_added = [space]
    new_indices = [space]
    # print(new_puzzle)
    while newly_added:
        if puzzle.count('#')>num_blocks:
            return ''
        # print(newly_added)
        toCheck = newly_added.pop(0)
        # print(toCheck)
        add_count+=1
        new_puzzle[toCheck] = '#'
        #up
        up = [toCheck-(i*width) for i in range(1,4) if 0<=toCheck-(i*width)<height*width]
        down = [toCheck+(j*width) for j in range(1,4) if 0<=toCheck+(j*width)<height*width]
        left = []
        right = []
        temp = toCheck
        count = 3
        while temp%width > 0 and count > 0:
            temp-=1
            count-=1
            if toCheck%width == 0 and count>0:
                break
            left.append(temp)
        temp = toCheck
        count = 3
        while temp%width < width-1 and count > 0:
            temp+=1
            count-=1
            if toCheck%width == width-1 and count>0:
                break
            right.append(temp)
        # print(up,down,left,right)
        for i,u in enumerate(up):
            if len(up)<3:
                for pos in up:
                    if new_puzzle[pos] in alphabetString:
                        return ''
                    newly_added.append(pos)
                    new_indices.append(pos)
                break
            if new_puzzle[u] in alphabetString and not all(True for a in up if new_puzzle[a] in alphabetString or a=='-'):
                return ''
            if new_puzzle[u] == '#':
                for j in up[:i]:
                    if new_puzzle[j]!='#':
                        newly_added.append(j)
                        new_indices.append(j)
            
            
        for i,d in enumerate(down):
            if len(down)<3:
                for pos in down:
                    if new_puzzle[pos] in alphabetString:
                        return ''
                    newly_added.append(pos)
                    new_indices.append(pos)
                break
            if new_puzzle[d] in alphabetString  and not all(True for a in down if new_puzzle[a] in alphabetString or a=='-'):
                return ''
            if new_puzzle[d] == '#':
                for j in down[:i]:
                    if new_puzzle[j]!='#':
                        newly_added.append(j)
                        new_indices.append(j)
        for i,l in enumerate(left):
            if len(left)<3:
                for pos in left:
                    if new_puzzle[pos] in alphabetString:
                        return ''
                    newly_added.append(pos)
                    new_indices.append(pos)
                break
            if new_puzzle[l] in alphabetString  and not all(True for a in left if new_puzzle[a] in alphabetString or a=='-'):
                return ''
            if new_puzzle[l] == '#':
                for j in left[:i]:
                    if new_puzzle[j]!='#':
                        newly_added.append(j)
                        new_indices.append(j)
            
        for i,r in enumerate(right):
            if len(right)<3:
                for pos in right:
                    if new_puzzle[pos] in alphabetString:
                        return ''
                    newly_added.append(pos)
                    new_indices.append(pos)
                break
            if new_puzzle[r] in alphabetString and not all(True for a in right if new_puzzle[a] in alphabetString or a=='-'):
                return ''
            if new_puzzle[r] == '#':
                for j in right[:i]:
                    if new_puzzle[j]!='#':
                        newly_added.append(j)
                        new_indices.append(j)
            
    for idx in new_indices:
            if new_puzzle[symmetrical_lookup[idx]]!='-':
                break
            new_puzzle[symmetrical_lookup[idx]] = '#'
            add_count+=1
            new_indices.append(symmetrical_lookup[idx])
    # print(new_indices)
    return ''.join(new_puzzle),new_indices,add_count
    

def bruteForce(puzzle,num_blocks,availables):
    '''
    If it is good, do it
    Otherwise just dont
    '''
    if puzzle.count('#')==num_blocks:
        return puzzle
    for choice in availables:
        if puzzle[symmetrical_lookup[choice]] != '-':
            continue
        plc,ni,ad = placeBlockingSquaresSpacing(puzzle,num_blocks,availables,choice)
        if not plc:
            continue
        if plc.count('#')>num_blocks:
            continue
        return bruteForce(plc,num_blocks,availables-set(ni))
    return ''
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
    print(breakdowns)
    num_blocks = num_squares - sum(b[3].count('#') for b in breakdowns)
    for breakdown in breakdowns:
        puzzle,mc = placeWord(puzzle,breakdown)
        num_blocks-=mc
    print(printPuzzle(puzzle,h,w,0))
    print(num_squares)
    availables={i for i in range(len(puzzle)) if puzzle[i]=='-' and puzzle[symmetrical_lookup[i]]=='-'}
    print(availables)
    bF = bruteForce(puzzle,num_squares,availables)   
    # availables = {i for i in range(h*w) if puzzle[i]=='-' and puzzle[symmetrical_lookup[i]]=='-'}
    # final_puzzle = placeBlockingSquares(puzzle,num_blocks,availables)
    print(printPuzzle(bF,h,w,0))
    # print('\n'*5, printPuzzle('-------------------------',5,5,0))
    # tp,ni,ad = placeBlockingSquaresSpacing('-------------------------',5,{},5)
    # print(printPuzzle(tp,5,5,0))
    # print(ni)
    # print(ad)
    
#Shaurya Jain, pd 3, 2025
