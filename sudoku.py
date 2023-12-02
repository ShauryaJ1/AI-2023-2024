import sys; args = sys.argv[1:]
import math
import time

def file_to_lines():
    return open(args[0]).read().splitlines()
def constraintSets():
    rows = [[i*puzzle_size+j for j in range(puzzle_size)] for i in range(puzzle_size)]
    cols = [[j*puzzle_size+i for j in range(puzzle_size)] for i in range(puzzle_size)]
    # rows_cols = [[[i*puzzle_size+j,j*puzzle_size+i] for j in range(puzzle_size)] for i in range(puzzle_size)]
    # rows = [[pair[0] for pair in row_col] for row_col in rows_cols]
    # cols = [[pair[1] for pair in row_col] for row_col in rows_cols]
    all_blocks = []
    p = 0
    for k in range(puzzle_size):
        blocks = [j+puzzle_size*i+p for i in range(sub_block_height) for j in range(sub_block_width)] 
        all_blocks.append(blocks)
        p+=sub_block_width
        if p%puzzle_size==0:
            p+=(puzzle_size-sub_block_width)*sub_block_height
    block_dict= {}
    for block in all_blocks:
        for i in block:
            block_dict[i] = block
    return all_blocks+rows+cols,block_dict  
      

def setGlobals(pzl):
    puzzle_size = int(math.sqrt(len(pzl)))
    pzl_sqrt = math.sqrt(puzzle_size)
    if  pzl_sqrt - int(pzl_sqrt) == 0.0:
        sub_block_height,sub_block_width = int(pzl_sqrt),int(pzl_sqrt)
    else:
        sub_block_height = 1
        for i in range(1,int(pzl_sqrt)+1):
            if puzzle_size%i==0 and i>sub_block_height:
                sub_block_height = i
        sub_block_width = puzzle_size//sub_block_height
    
    symbol_set = [str(digits[i]) if i<9 else letters[i-9] for i in range(puzzle_size)]
    return puzzle_size,sub_block_width,sub_block_height,symbol_set
def isInvalid(pzl):
    # sets_to_check = [c_sets[puzzle_size+space//puzzle_size]]+[c_sets[puzzle_size*2+space%puzzle_size]]+[block_dict[space]]
    # for constraintSet in sets_to_check:
    for constraintSet in c_sets:
        seen = ""
        for idx in constraintSet:
            if pzl[idx] in seen:
                return True
            if pzl[idx]!=".":
                seen+=pzl[idx]

    return False

def neighbors(pzl):
    neighbors_list = []
    for idx in range(puzzle_size**2):   
        neighbors_list.append(set(c_sets[puzzle_size+idx//puzzle_size]+c_sets[puzzle_size*2+idx%puzzle_size]+block_dict[idx]))
    return neighbors_list
def isInvalid(pzl,last_pos):
    
    for idx in NBRS[last_pos]:
        if pzl[idx]==pzl[last_pos] and idx!=last_pos and pzl[idx]!='.' and pzl[last_pos]!='.':
            return True

    return False
def isSolved(pzl):
    return "." not in pzl
def replace_letters(word,empty_space,c2):
  temp = list(word)
  temp[empty_space] = c2
  return ''.join(temp)
def setOfChoices(pzl):
    space = pzl.index(".")
    set_of_choices = []
    for s in symbol_set:
        set_of_choices.append(replace_letters(pzl,space,s))
    return set_of_choices

def periods(pzl):
    periods = {}
    for i in range(puzzle_size**2):
        if pzl[i] == '.':
            periods[i] = len(set(symbol_set)-set([pzl[idx] for idx in NBRS[i]]))
    return periods
def findBestPeriod(pzl):
    min = puzzle_size*3
    min_space = 0
    # for space in periods:
    #     if periods[space]==1:
    #         return space
    #     if periods[space]<min:
    #         min = periods[space]
    #         min_space = space
    # return min_space
    for idx,space in enumerate(pzl):
        if space == '.':
            options = len(set(symbol_set)-set([pzl[i] for i in NBRS[idx]]))
            if options==1:
                return idx
            if options<min:
                min = options
                min_space = idx
    return min_space

def bruteForce(pzl,space):
    if isInvalid(pzl,space):
        return ""
    if isSolved(pzl):
        return pzl
    # set_of_choices = setOfChoices(pzl)
    # for possibleChoice in set_of_choices:
    space_pzl = pzl.index(".")
    for possibleChoice in symbol_set:
    #     subPzl = possibleChoice
        subPzl = pzl[:space_pzl] + possibleChoice + pzl[space_pzl+1:]
        bF = bruteForce(subPzl,space_pzl)
        if bF:
            return bF
    return ""
def bruteForce_Best_Period(pzl,space):
    if isInvalid(pzl,space):
        return ""
    if isSolved(pzl):
        return pzl
    # set_of_choices = setOfChoices(pzl)
    # for possibleChoice in set_of_choices:
    # space_pzl = pzl.index(".")
    space_pzl = findBestPeriod(pzl)
    # new_periods = dict(periods)
    # del new_periods[space_pzl]
    # for idx in NBRS[space_pzl]:
    #     if idx in new_periods:
    #         new_periods[idx]+=1
    for possibleChoice in symbol_set:
    #     subPzl = possibleChoice
        subPzl = pzl[:space_pzl] + possibleChoice + pzl[space_pzl+1:]
        bF = bruteForce_Best_Period(subPzl,space_pzl)
        if bF:
            return bF
    return ""

def bruteForce_Best_Period_With_Options(pzl,space):
    if isInvalid(pzl,space):
        return ""
    if isSolved(pzl):
        return pzl
    # set_of_choices = setOfChoices(pzl)
    # for possibleChoice in set_of_choices:
    # space_pzl = pzl.index(".")
    min = puzzle_size*3
    # options = set()
    # new_periods = dict(periods)
    # del new_periods[space_pzl]
    # for idx in NBRS[space_pzl]:
    #     if idx in new_periods:
    #         new_periods[idx]+=1
    for idx,tile in enumerate(pzl):
        if tile == '.':
            # len_options = len(set(symbol_set)-set([pzl[i] for i in NBRS[idx]]))
            options = set(symbol_set)-set([pzl[i] for i in NBRS[idx]])
            if len(options)==1:
                space_pzl = idx
                # min_options = set(symbol_set)-set([pzl[i] for i in NBRS[idx]])
                min_options = options
                break
            if len(options)<min:
                min = len(options)
                min_options = options
                space_pzl = idx
    for possibleChoice in min_options:
    #     subPzl = possibleChoice
        subPzl = pzl[:space_pzl] + possibleChoice + pzl[space_pzl+1:]
        bF = bruteForce_Best_Period_With_Options(subPzl,space_pzl)
        if bF:
            return bF
    return ""
def printSudoku(pzl):
    temp_print=""
    for row in range(puzzle_size):
        for col in range(puzzle_size):
            temp_print+=pzl[row*puzzle_size+col] +" "
            # temp_print+=str(row*puzzle_size+col)+" "
            if (col+1)%sub_block_width==0 and col<puzzle_size-1:
                temp_print+=" "
        temp_print+="\n"
        if (row+1)%sub_block_height == 0:
            temp_print+="\n"
    print(temp_print)
        
def checkSum(pzl):
    min_ascii = min([ord(c) for c in pzl])
    return sum(ord(c)-min_ascii for c in pzl)
if __name__ == "__main__":
    global letters,digits
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = [i for i in range(1,10)]
    
    if len(args)==0:
        pzl = '.43.8.25.6.............1.949....4.7....6.8....1.2....382.5.............5.34.9.71.'
        puzzle_size,sub_block_width,sub_block_height,symbol_set = setGlobals(pzl)
        c_sets,block_dict = constraintSets()
        # for key in block_dict:
        #     print(key, block_dict[key])
        printSudoku(pzl)
        NBRS = neighbors(pzl)
        space = 72
        print(len(set(symbol_set)-set([pzl[i] for i in NBRS[space]])))
        print(findBestPeriod(pzl))
    elif args[0].endswith("txt"):
        puzzles_list = file_to_lines()
        for i, pzl in enumerate(puzzles_list):
            start_time = time.time()
            puzzle_size,sub_block_width,sub_block_height,symbol_set = setGlobals(pzl)
            c_sets,block_dict = constraintSets()
            NBRS = neighbors(pzl)
            
            solved = bruteForce_Best_Period_With_Options(pzl,0)
            # solved = bruteForce(pzl,0)
            if solved:
                print(i+1,": ",pzl)
                print("   "+len(str(i+1))*" ", solved, checkSum(solved), f"{time.time()-start_time:.3g}s")
            else:
                
                print(i+1,": ",pzl)
                print("     ","No solution",f"{time.time()-start_time:.3g}s")
    else:
        pzl = args[0]
        start_time = time.time()
        puzzle_size,sub_block_width,sub_block_height,symbol_set = setGlobals(pzl)
        # space = 0
        c_sets,block_dict = constraintSets()
        NBRS = neighbors(pzl)
            
        solved = bruteForce_Best_Period_With_Options(pzl,0)

        print(solved,f"{time.time()-start_time:.3g}s")
        
    
    # puzzle_size,sub_block_width,sub_block_height,symbol_set = setGlobals("123456789111"*12)
    # printSudoku("123456789111"*12)
    # for constraintSet in constraintSets():
    #     print(constraintSet)
    # print(isInvalid("123456789111"*12))
    # print(isSolved("123456789111"*12))

#  0  1  2  3  4  5  6  7  8  
#  9 10 11 12 13 14 15 16 17 
# 18 19 20 21 22 23 24 25 26
# 27 28 29 30 31 32 33 34 35
# 36 37 38 39 40 41 42 43 44
# 45 46 47 48 49 50 51 52 53 
# 54 55 56 57 58 59 60 61 62 
# 63 64 65 66 67 68 69 70 71 
# 72 73 74 75 76 77 78 79 80 
#Shaurya Jain, pd 3, 2025


