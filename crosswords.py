import sys; args = sys.argv[1:]
import math
import time 
global h
global w
global num_squares
global symmetrical_lookup
global alphabetString

# args=[ '13x13', 32, 'Eckel.txt' ,'H1x4#Toe#', 'H9x2#' ,'V3x6#', 'H10x0Scintillating', 'V0x5stirrup' ,'H4x2##Ordained' ,'V0x1Ward' ,'V0x12Lis', 'V5x0orb']
# args = ['7x7',40,'Eckel.txt']
# args = ['13x13', 32,'Eckel.txt' ,'V2x4#', 'V1x9#', 'V3x2#', 'h8x2#moo#', 'v5x5#two#' ,'h6x4#ten#' ,'v3x7#own#' ,'h4x6#orb#','H12x4Send']
# args = ['6x6','36','Eckel.txt']
# args = ['6x6','20','Eckel.txt']
# args= ['10x13', '32', 'Eckel.txt', 'V6x0#', 'V9x3#','H3x9#', 'V0x8Obituaries']
# args = ['9x30', 50, 'Eckel.txt', 'h4x12d#', 'h3x9t#', 'h2x9#' ,'v2x0eye' ,'V5x1#w', 'V8x26l']
# args = ['8x8',50,'Eckel.txt']
def file_to_lines():
    return open(args[0]).read().splitlines()
alphabetString = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

dict_list = file_to_lines()
dict_dict = {}
for word in dict_list:
    if len(word) in dict_dict:
        dict_dict[len(word)] +=[word]
    else:
        dict_dict[len(word)] = [word]
# for key in dict_dict:
#     print(f"{key}: {dict_dict[key][:5]}")

args = args[1:]
h,w = int(args[0][:args[0].index('x')]) ,int(args[0][1+args[0].index('x'):])
num_squares = int(args[1])
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
def wordSearch(split):
    '''
    Given a word length and split, returns a word
    '''
    word_length = len(split)
    possibles = dict_dict[word_length]
    # print(possibles)
    letter_indices = [i for i in range(word_length) if split[i] in alphabetString]
    for possible in possibles:
        if all(possible[i]==split.lower()[i] for i in letter_indices):
            return(word)
    return ''

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
    if not xword_board:
        print('no puzzle')
    placed = list(xword_board)
    orientation = seedStringBreakdown[0]
    seedStringHeight = int(seedStringBreakdown[1])
    seedStringWidth = int(seedStringBreakdown[2])
    charactersToPlace = seedStringBreakdown[3]
    startIndex = seedStringHeight*w + seedStringWidth
    if orientation.lower() == 'h':
        indices_to_change = [startIndex+i for i in range(len(charactersToPlace))]
    else:
        indices_to_change = [startIndex + i * w for i in range(len(charactersToPlace))]
    for char_idx,board_idx in enumerate(indices_to_change):
        if charactersToPlace[char_idx] =='#':
            # print(placed)
            placed,ni,ad = placeBlockingSquaresSpacing(''.join(placed),num_squares,{},board_idx,True)
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
    if not placed:
        print('nothing placed')
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
def connectivity(puzzle):
    '''
    Accepts a puzzle
    Returns boolean representing connected or not
    '''

    '''
    Make adjacency list 
    '''
    adj_list = {}
    for i,c in enumerate(puzzle):
        if c!='#':
            val = []
            if 0<=i-w<h*w and puzzle[i-w]!='#':
                val.append(i-w)
            if 0<=i+w<h*w and puzzle[i+w]!='#':
                val.append(i+w)
            if i%w!=0 and 0<=i-1<h*w and puzzle[i-1]!='#':
                val.append(i-1)
            if i%w!=w-1 and 0<=i+1<h*w and puzzle[i+1]!='#':
                val.append(i+1)
            adj_list[i] = val
    not_blocks = [i for i in range(len(puzzle)) if puzzle[i]!='#']
    if not not_blocks:
        return True
    visited = {i:False for i in range(h*w)}
    stack = [not_blocks[0]]
    while stack:
        t = stack.pop()
        visited[t] = True
        for idx in adj_list[t]:
            if not visited[idx]:
                stack.append(idx)
    return sum([1 for i in visited if visited[i]]) == len(not_blocks)
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

def placeBlockingSquaresSpacing(puzzle,num_blocks,availables,space,inSS):
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
            return '',0,0
        # print(newly_added)
        toCheck = newly_added.pop(0)

        # print(toCheck)
        # print(toCheck)
        add_count+=1
        # print(len(new_puzzle))
        if new_puzzle[toCheck] in alphabetString:
            return '',0,0
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
                        return '',0,0
                    if new_puzzle[pos] != '#' and pos not in new_indices:
                        newly_added.append(pos)
                        new_indices.append(pos)
                break
            if new_puzzle[u] in alphabetString and not all(True for a in up if new_puzzle[a] in alphabetString or a=='-'):
                # print('nothing')
                return '',0,0
            if new_puzzle[u] == '#':
                for j in up[:i]:
                    if new_puzzle[j]!='#' and j not in new_indices:
                        newly_added.append(j)
                        new_indices.append(j)
            
            
        for i,d in enumerate(down):
            if len(down)<3:
                for pos in down:
                    if new_puzzle[pos] in alphabetString:
                        # print('nothing')
                        return '',0,0
                    if new_puzzle[pos] != '#' and pos not in new_indices:
                        newly_added.append(pos)
                        new_indices.append(pos)
                break
            if new_puzzle[d] in alphabetString  and not all(True for a in down if new_puzzle[a] in alphabetString or a=='-'):
                # print('nothing')
                return '',0,0
            if new_puzzle[d] == '#':
                for j in down[:i]:
                    if new_puzzle[j]!='#' and j not in new_indices:
                        
                        newly_added.append(j)
                        new_indices.append(j)
        for i,l in enumerate(left):
            if len(left)<3:
                for pos in left:
                    if new_puzzle[pos] in alphabetString:
                        # print('nothing')
                        return '',0,0
                    if new_puzzle[pos] != '#' and pos not in new_indices:
                        newly_added.append(pos)
                        new_indices.append(pos)
                break
            if new_puzzle[l] in alphabetString  and not all(True for a in left if new_puzzle[a] in alphabetString or a=='-'):
                # print('nothing')
                return '',0,0
            if new_puzzle[l] == '#':
                for j in left[:i]:
                    if new_puzzle[j]!='#' and j not in new_indices:
                        newly_added.append(j)
                        new_indices.append(j)
            
        for i,r in enumerate(right):
            if len(right)<3:
                for pos in right:
                    if new_puzzle[pos] in alphabetString:
                        # print('nothing')
                        return '',0,0
                    if new_puzzle[pos] != '#' and pos not in new_indices:
                        newly_added.append(pos)
                        new_indices.append(pos)
                break
            if new_puzzle[r] in alphabetString and not all(True for a in right if new_puzzle[a] in alphabetString or a=='-'):
                # print('nothing')
                return '',0,0
            if new_puzzle[r] == '#':
                for j in right[:i]:
                    if new_puzzle[j]!='#' and j not in new_indices:
                        newly_added.append(j)
                        new_indices.append(j)
            
    for idx in new_indices:
            if new_puzzle[symmetrical_lookup[idx]]!='-':
                break
            # new_puzzle[symmetrical_lookup[idx]] = '#'
            new_puzzle,_,_ = placeBlockingSquaresSpacing(''.join(new_puzzle),num_blocks,availables,symmetrical_lookup[idx],inSS)
            if not new_puzzle:
                return '',0,0
            new_puzzle = list(new_puzzle)
            add_count+=1
            new_indices.append(symmetrical_lookup[idx])
    
    if not inSS:
        if connectivity(b:=''.join(new_puzzle)):
            return b,new_indices,add_count
        return '',0,0
    else:
        return ''.join(new_puzzle),new_indices,add_count
    #     for i,u in enumerate(up):
    #             if len(up)<3:
    #                 for pos in up:
    #                     if new_puzzle[pos] in alphabetString:
    #                         return '',0,0
    #                     if new_puzzle[pos] != '#' and pos not in new_indices:
    #                         newly_added.append(pos)
    #                         new_indices.append(pos)
    #                 break
    #             if new_puzzle[u] in alphabetString and not all([new_puzzle[a] in alphabetString or new_puzzle[a]=='-' for a in up]):
    #                 # print('nothing')
    #                 return '',0,0
    #             if new_puzzle[u] == '#':
    #                 for j in up[:i]:
    #                     if new_puzzle[j]!='#' and j not in new_indices:
    #                         newly_added.append(j)
    #                         new_indices.append(j)
            
            
    #     for i,d in enumerate(down):
    #         if len(down)<3:
    #             for pos in down:
    #                 if new_puzzle[pos] in alphabetString:
    #                     # print('nothing')
    #                     return '',0,0
    #                 if new_puzzle[pos] != '#' and pos not in new_indices:
    #                     newly_added.append(pos)
    #                     new_indices.append(pos)
    #             break
    #         if new_puzzle[d] in alphabetString  and not all([new_puzzle[a] in alphabetString or new_puzzle[a]=='-' for a in down]):
    #             # print('nothing')
    #             return '',0,0
    #         if new_puzzle[d] == '#':
    #             for j in down[:i]:
    #                 if new_puzzle[j]!='#' and j not in new_indices:
                        
    #                     newly_added.append(j)
    #                     new_indices.append(j)
    #     for i,l in enumerate(left):
    #         if len(left)<3:
    #             for pos in left:
    #                 if new_puzzle[pos] in alphabetString:
    #                     # print('nothing')
    #                     return '',0,0
    #                 if new_puzzle[pos] != '#' and pos not in new_indices:
    #                     newly_added.append(pos)
    #                     new_indices.append(pos)
    #             break
    #         if new_puzzle[l] in alphabetString  and not all([new_puzzle[a] in alphabetString or new_puzzle[a]=='-' for a in left]):
    #             # print('nothing')
    #             return '',0,0
    #         if new_puzzle[l] == '#':
    #             for j in left[:i]:
    #                 if new_puzzle[j]!='#' and j not in new_indices:
    #                     newly_added.append(j)
    #                     new_indices.append(j)
            
    #     for i,r in enumerate(right):
    #         if len(right)<3:
    #             for pos in right:
    #                 if new_puzzle[pos] in alphabetString:
    #                     # print('nothing')
    #                     return '',0,0
    #                 if new_puzzle[pos] != '#' and pos not in new_indices:
    #                     newly_added.append(pos)
    #                     new_indices.append(pos)
    #             break
    #         if new_puzzle[r] in alphabetString and not all([new_puzzle[a] in alphabetString or new_puzzle[a]=='-' for a in right]):
    #             # print('nothing')
    #             return '',0,0
    #         if new_puzzle[r] == '#':
    #             for j in right[:i]:
    #                 if new_puzzle[j]!='#' and j not in new_indices:
    #                     newly_added.append(j)
    #                     new_indices.append(j)
            
    # for idx in new_indices:
    #         if new_puzzle[symmetrical_lookup[idx]]!='-':
    #             break
    #         # new_puzzle[symmetrical_lookup[idx]] = '#'
    #         new_puzzle,_,_ = placeBlockingSquaresSpacing(''.join(new_puzzle),num_blocks,availables,symmetrical_lookup[idx],inSS)
    #         if not new_puzzle:
    #             return '',0,0
    #         new_puzzle = list(new_puzzle)
    #         add_count+=1
    #         new_indices.append(symmetrical_lookup[idx])
    
    # if not inSS:
    #     if connectivity(b:=''.join(new_puzzle)):
    #         return b,new_indices,add_count
    #     return '',0,0
    # else:
    #     return ''.join(new_puzzle),new_indices,add_count
def calculateSpaces(puzzle,space):
    '''
    receives puzzle and space and returns value for word spaces
    '''
    
    row= puzzle[(space//w)*(w):(space//w)*(w+1)]
    col = puzzle[space%w:h*w:w]
    
    row_sections = row.split('#')
    col_sections = col.split('#')

    max_row_section = max([split.count('-') for split in row_sections])
    max_col_section = max([split.count('-') for split in col_sections])

    return (max_col_section + max_row_section, row_sections, col_sections,space)




    # return sum(len(i) for i in puzzle[space%w:space:w].split('#')) + sum(len(i) for i in puzzle[space%w + w * (space//w)::w].split('#')) + sum(len(i) for i in puzzle[(space//w)*w:(space//w + 1)*(w)].split('#'))
    
    # print([(len(i),i) for i in puzzle[space%w::w].split('#')])
    # print(space//w)
    # print(puzzle[(space//w)*w:(space//w + 1)*(w)])
def place_words_with_bruteforce(puzzle, possibles):
    if puzzle.count('-') == 0:
        return puzzle
    sorted_possibles = []
    for possible in possibles:
        sorted_possibles.append(calculateSpaces(puzzle, possible))
    sorted_possibles = sorted(sorted_possibles)
    return sorted_possibles
    # for choice in availables:
    #     if puzzle[symmetrical_lookup[choice]] != '-':
    #         continue
    #     plc,ni,ad = placeBlockingSquaresSpacing(puzzle,num_blocks,availables,choice,False)
    #     if isInvalid(plc):
    #         continue
    #     if not plc:
    #         continue
    #     if plc.count('#')>num_blocks:
    #         continue
    #     return bruteForce(plc,num_blocks,availables-set(ni))
def bruteForce(puzzle,num_blocks,availables):
    '''
    If it is good, do it
    Otherwise just dont
    '''
    if puzzle.count('#')==num_blocks:
        return puzzle
    # sorted_availables = [()]
    for choice in availables:
        if puzzle[symmetrical_lookup[choice]] != '-':
            continue
        plc,ni,ad = placeBlockingSquaresSpacing(puzzle,num_blocks,availables,choice,False)
        if isInvalid(plc):
            continue
        if not plc:
            continue
        if plc.count('#')>num_blocks:
            continue
        return bruteForce(plc,num_blocks,availables-set(ni))
    # print(availables)
    # print('nothing')
    return puzzle
def fillInWordsHorizontally(puzzle):
    puzzle_list = list(puzzle)
    availables = {i for i in range(h*w) if puzzle[i]=='-'}
    horizontal_lines = [[j for j in range(i*w,i*w+w)] for i in range(h)]
    horizontal_lines_of_puzzle = [''.join([puzzle[j] for j in range(i*w,i*w+w)]) for i in range(h)]
    # print(horizontal_lines)
    # print(horizontal_lines_of_puzzle)
    new_h_lines = []
    for i,v in enumerate(horizontal_lines_of_puzzle):
        c_hline = v
        splits = v.split('#')
        for split in splits:
            # print(split)
            if any(char in alphabetString for char in split):
                # continue
                letter_indices = [i for i in range(len(split)) if split[i] in alphabetString]
                if len(split) in dict_dict:
                    for word in dict_dict[len(split)]:
                        if all(word[i]==split.lower()[i] for i in letter_indices):
                            word_to_be_placed = word
                            dict_dict[len(split)].remove(word)
                            c_hline = c_hline[:c_hline.index(split)] + word_to_be_placed + c_hline[c_hline.index(split)+len(split):]
                            break

            elif(split and len(split) in dict_dict):
                word_to_be_placed = dict_dict[len(split)][0]
                dict_dict[len(split)] = dict_dict[len(split)][1:]
                c_hline = c_hline[:c_hline.index(split)] + word_to_be_placed + c_hline[c_hline.index(split)+len(split):]
    
        new_h_lines.append(c_hline)
                

    print(printPuzzle(''.join(new_h_lines),h,w,0))
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
    # oddPos = -1
    # print(args)
    alphabetString = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    h,w = int(args[0][:args[0].index('x')]) ,int(args[0][1+args[0].index('x'):])
    num_squares = int(args[1])
    # dict_list = file_to_lines()
    seedStrings = ""
    if len(args)>2:
        seedStrings = args[2:]

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

    puzzle = '-'*(h*w)
    breakdowns = []
    for seedString in seedStrings:
        breakdowns.append(seedStringBreakdown(seedString))
    
    # print(breakdowns)
    if num_squares%2==1:
        # print('ODD')
        for key in symmetrical_lookup:
            if symmetrical_lookup[key] == key:
                temp_puzzle = list(puzzle)
                temp_puzzle[key] = '#'
                puzzle = ''.join(temp_puzzle)
    num_blocks = num_squares - sum(b[3].count('#') for b in breakdowns)
    
    for breakdown in breakdowns:
        # print(breakdown)
        if not puzzle:
            print('NO PUZZLE')
        puzzle,mc = placeWord(puzzle,breakdown)
        num_blocks-=mc
    # print(printPuzzle(puzzle,h,w,0))
    # print(printPuzzle(puzzle,h,w,0))
    # print(num_squares)
    
        
    # print(availables)
    
    availables={i for i in range(len(puzzle)) if puzzle[i]=='-' and puzzle[symmetrical_lookup[i]]=='-'}
    bF = bruteForce(puzzle,num_squares,availables)   
    print(calculateSpaces(bF,6))
    # print(bF.count('#'))
    # availables = {i for i in range(h*w) if puzzle[i]=='-' and puzzle[symmetrical_lookup[i]]=='-'}
    # final_puzzle = placeBlockingSquares(puzzle,num_blocks,availables)
    print(bF.count('#'))
    print(printPuzzle(bF,h,w,0))
    print()
    fillInWordsHorizontally(bF)

    print(place_words_with_bruteforce(puzzle,availables))
    
    # print(wordSearch('-A-'))
    # print(printPuzzle(runRoute(''.join(['-', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#', '#', '#', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-']),3,9),10,13,0))
    # print(seedStringBreakdown('h6x0'))
    # print(connectivity(bF))

    # print('\n'*5, printPuzzle('-------------------------',5,5,0))
    # tp,ni,ad = placeBlockingSquaresSpacing('-------------------------',5,{},5)
    # print(printPuzzle(tp,5,5,0))
    # print(ni)
    # print(ad)
    
#Shaurya Jain, pd 3, 2025