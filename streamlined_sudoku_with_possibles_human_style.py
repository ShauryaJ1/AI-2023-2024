import sys; args = sys.argv[1:]
import math
import time

def file_to_lines():
    return open(args[0]).read().splitlines()
def constraintSets():
    rows = [[i*puzzle_size+j for j in range(puzzle_size)] for i in range(puzzle_size)]
    cols = [[j*puzzle_size+i for j in range(puzzle_size)] for i in range(puzzle_size)]
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
    syms = set(list(pzl))
    if '.' in syms:
        syms.remove('.')
    if len(syms) == puzzle_size:
        symbol_set = syms
    else:
        all_symbol_set = set([str(digits[i]) if i<9 else letters[i-9] for i in range(puzzle_size)])
        left = list(all_symbol_set - syms)
        symbol_set = list(syms) + left[:puzzle_size-len(syms)]

    return puzzle_size,sub_block_width,sub_block_height,symbol_set
def neighbors(pzl):
    neighbors_list = []
    for idx in range(puzzle_size**2):   
        neighbors_list.append(set(c_sets[puzzle_size+idx//puzzle_size]+c_sets[puzzle_size*2+idx%puzzle_size]+block_dict[idx]))
    return neighbors_list
def possible_symbols(neighbors):
    possibles = {}
    for idx,nbr in enumerate(neighbors):
        if pzl[idx]=='.':
            possibles[idx] = set(symbol_set) - {pzl[i] for i in nbr}
            
    return possibles
def possible_periods(possible_symbols):
    possible_periods = {sym:set() for sym in symbol_set}
    for idx in possible_symbols:
        for sym in possible_symbols[idx]:
                possible_periods[sym].add(idx)
    return possible_periods
def isInvalid(pzl,last_pos):
    
    for idx in NBRS[last_pos]:
        if pzl[idx]==pzl[last_pos] and idx!=last_pos and pzl[idx]!='.' and pzl[last_pos]!='.':
            return True

    return False
def isSolved(pzl):
    return "." not in pzl
def updateStat(key_string,stats_counter):
    if key_string in stats_counter:
        stats_counter[key_string]+=1
    else:
        stats_counter[key_string]=1
def findBestSymbol(min_options,possible_dict):
        best_options_len = len(min_options)

        # possible_periods_dict = possible_periods(possible_dict)
        for sym in symbol_set:
            if pzl.count(sym)<puzzle_size:
                possiblePositions = {i for i in possible_dict if sym in possible_dict[i]}
                for cs in c_sets:
                # for sym in symbol_set:

                    temp = set(cs).intersection(possiblePositions)
                    if len(temp)==1:
                        return [(pos,sym) for pos in temp]
                    if len(temp)<best_options_len:
                        best_symbol = sym
                        best_empties = temp
                        best_options_len = len(temp)
def findBestSymbol2(min_options,possible_periods_dict):
        for sym in symbol_set:
            for cs in c_sets:
                temp = set(cs).intersection(possible_periods_dict[sym])
                if len(temp)<len(min_options) and len(temp)>0:
                    return [(pos,sym)for pos in temp]
def bruteForce_Best_Period_With_Options(pzl,space,possible_dict):
    # if isInvalid(pzl,space):
    #     return ''
    if isSolved(pzl):
        return pzl
    min = puzzle_size*3
    for idx,tile in enumerate(pzl):
        if tile == '.':
            options =possible_dict[idx]
            if len(options)==0:
                # updateStat(f"choice ct {len(options)}")
                return ""
            if len(options)==1:
                space_pzl = idx
                min_options = options
                lstOfChoices = [(space_pzl,option) for option in min_options]
                # updateStat(f"choice ct {len(options)}")
                break
            if len(options)<min:
                min = len(options)
                min_options = options
                space_pzl = idx
                # updateStat(f"choice ct {len(options)}")
    if len(min_options)!=1:
        new_lstOfChoices = findBestSymbol(min_options,possible_dict)
        if new_lstOfChoices:
            lstOfChoices = new_lstOfChoices
        else:
            lstOfChoices = [(space_pzl,option) for option in min_options]
    # updateStat(f"choice ct {len(lstOfChoices)}",stats_counter)
    # print(lstOfChoices)
    for pos,possibleChoice in lstOfChoices:
        
        subPzl = pzl[:pos] + possibleChoice + pzl[pos+1:]
        new_possibles_dict = {**possible_dict}
        del new_possibles_dict[pos]
        # for nbr in NBRS[pos].intersection(set(new_possibles_dict)):
        for nbr in NBRS[pos]:
            if nbr in new_possibles_dict:
                new_possibles_dict[nbr] = new_possibles_dict[nbr] - {possibleChoice}
        bF = bruteForce_Best_Period_With_Options(subPzl,space_pzl,new_possibles_dict)
        if bF:
            return bF
    # print("I sillied")
    return ""
def bruteForce(pzl,space,possible_symbols_dict,possible_periods_dict):
    # if isInvalid(pzl,space):
    #     return ''
    if isSolved(pzl):
        return pzl
    min = puzzle_size*3
    for idx,tile in enumerate(pzl):
        if tile == '.':
            options =possible_symbols_dict[idx]
            if len(options)==0:
                # updateStat(f"choice ct {len(options)}")
                return ""
            if len(options)==1:
                space_pzl = idx
                min_options = options
                lstOfChoices = [(space_pzl,option) for option in min_options]
                # updateStat(f"choice ct {len(options)}")
                break
            if len(options)<min:
                min = len(options)
                min_options = options
                space_pzl = idx
                # updateStat(f"choice ct {len(options)}")
    if len(min_options)!=1:
        new_lstOfChoices = findBestSymbol2(min_options,possible_periods_dict)
        if new_lstOfChoices:
            lstOfChoices = new_lstOfChoices
        else:
            lstOfChoices = [(space_pzl,option) for option in min_options]
    # updateStat(f"choice ct {len(lstOfChoices)}",stats_counter)
    print(lstOfChoices)
    for pos,possibleChoice in lstOfChoices:
        subPzl = pzl[:pos] + possibleChoice + pzl[pos+1:]
        new_possible_symbols_dict = {**possible_symbols_dict}
        new_possible_periods_dict = {**possible_periods_dict}
        del new_possible_symbols_dict[pos]
        # for nbr in NBRS[pos].intersection(set(new_possibles_dict)):
        for nbr in NBRS[pos]:
            if nbr in new_possible_symbols_dict:
                new_possible_symbols_dict[nbr] = new_possible_symbols_dict[nbr] - {possibleChoice}
        for sym in new_possible_periods_dict:
                new_possible_periods_dict[sym] = new_possible_periods_dict[sym] - {pos}
        bF = bruteForce(subPzl,space_pzl,new_possible_symbols_dict,new_possible_periods_dict)
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
        pzl = '145337812851887827872311586421115372512873356753216887268514259294727731731389764'

        puzzle_size,sub_block_width,sub_block_height,symbol_set = setGlobals(pzl)
        c_sets,block_dict = constraintSets()
        NBRS = neighbors(pzl)
        possible_symbols_dict = possible_symbols(NBRS)
        possible_periods_dict = possible_periods(possible_symbols_dict)
        printSudoku(pzl)
        for sym in possible_periods_dict:
            print(sym, " ",possible_periods_dict[sym])
        
        # for key in block_dict:
        #     print(key," ",block_dict[key])
        
    elif args[0].endswith("txt"):
        puzzles_list = file_to_lines()
        # stats_counter = {}
        for i, pzl in enumerate(puzzles_list):
            start_time = time.time()
            # times = []
            puzzle_size,sub_block_width,sub_block_height,symbol_set = setGlobals(pzl)
            c_sets,block_dict = constraintSets()
            NBRS = neighbors(pzl)
            possible_symbols_dict = possible_symbols(NBRS)
            # possible_periods_dict = possible_periods(possible_symbols_dict)
            solved = bruteForce_Best_Period_With_Options(pzl,0,possible_symbols_dict)
            # solved = bruteForce(pzl,0,possible_symbols_dict,possible_periods_dict)
            # solved = bruteForce(pzl,0)
            if solved:
                print(i+1,": ",pzl)
                # t_time = 
                print("   "+len(str(i+1))*" ", solved, checkSum(solved), f"{time.time()-start_time:.3g}s")
            else:
    
                print(i+1,": ",pzl)
                print("     ","No solution",f"{time.time()-start_time:.3g}s")
        # for stat in stats_counter:
        #     print(stat, " ", stats_counter[stat])
    else:
        pzl = args[0]
        start_time = time.time()
        puzzle_size,sub_block_width,sub_block_height,symbol_set = setGlobals(pzl)
        # space = 0
        c_sets,block_dict = constraintSets()
        NBRS = neighbors(pzl)
        possibles_dict = possible_symbols(NBRS)
        # for key in possibles_dict:
        #     print(key, " ", possibles_dict[key])
        solved = bruteForce_Best_Period_With_Options(pzl,0,possibles_dict)
        
        print(solved,f"{time.time()-start_time:.3g}s")
        # printSudoku(pzl)
        # printSudoku(solved)
        # given = set(list(pzl))
        # given.remove('.')
        # print(given,len(given))
        # print(checkSum(solved))
        # print(all(isInvalid(solved,pos) for pos in range(len(pzl))))
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
