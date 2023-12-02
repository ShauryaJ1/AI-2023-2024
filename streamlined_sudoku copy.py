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
    # given = set(list(pzl))
    # given.remove('.')
    # if len(given)==puzzle_size:
    #     symbol_set = given
    # else:
    #     symbols_left = list(set(digits) + set(list(letters)) - given)
    #     symbol_set = given+ set([symbols_left[i] for i in range(puzzle_size-len(given))])
    symbol_set = [str(digits[i]) if i<9 else letters[i-9] for i in range(puzzle_size)]
    return puzzle_size,sub_block_width,sub_block_height,symbol_set
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
def bruteForce_Best_Period_With_Options(pzl,space):
    # if isInvalid(pzl,space):
    #     return ""
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
            if len(options)==0:
                min_options = set()
                break
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
    if args[0].endswith("txt"):
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
        printSudoku(pzl)
        printSudoku(solved)
        given = set(list(pzl))
        given.remove('.')
        print(given,len(given))
        print(checkSum(solved))
        print(all(isInvalid(solved,pos) for pos in range(len(pzl))))
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
