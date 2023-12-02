import sys; args = sys.argv[1:]
import math
import time
def isInvalid(pzl):
    width = int(math.sqrt(len(pzl)))
    for row in range(width):
        pzl_row = pzl[row*width:width*(row+1)]
        for tile in pzl_row:
            if pzl_row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    for col in range(width):
        pzl_col = ''.join([pzl[col+i*width]for i in range(width)])
        for tile in pzl_col:
            if pzl_col.count(tile)>1 and tile!=".":
                return True
                
            else:
                continue
    pzl_diag_1 = ''.join([pzl[i*(width+1)]for i in range(width)])
    pzl_diag_2 = ''.join([pzl[(i+1)*(width-1)]for i in range(width)])
    for tile in pzl_diag_1:
        if pzl_diag_1.count(tile)>1 and tile!=".":
            return True
        else:
            continue
    for tile in pzl_diag_2:
        if pzl_diag_2.count(tile)>1 and tile!=".":
            return True
        else:
            continue
    return False
def isSolved(pzl):
    return True if pzl.count(".")==0 else False
def replace_letters(word,empty_space,c2):
  temp = list(word)
  temp[empty_space] = str(c2)
  return ''.join(temp)
def setOfChoices(pzl):
    choices = []
    width = int(math.sqrt(len(pzl)))
    tiles = [i for i in range(1,width+1)]
    empty_space = pzl.index(".")
    for tile in tiles:
        choices.append(replace_letters(pzl,empty_space,tile))
    
    return choices
def bruteForce(pzl):
    if isInvalid(pzl):
        return ""
    if isSolved(pzl):
        return pzl
    set_of_choices = setOfChoices(pzl)
    for possibleChoice in set_of_choices:
        subPzl = possibleChoice
        bF = bruteForce(subPzl)
        if bF:
            return bF
    return ""

def squarePrint(pzl):
    width = int(math.sqrt(len(pzl)))
    split_pzls = [pzl[i*width:width*(i+1)] for i in range(width)]
    return split_pzls


if __name__ == "__main__":
    if len(args) == 0:
        pzl = "."*49
    else:
        pzl = "."*(int(args[0])**2)
    start_time = time.time()
    solved = bruteForce(pzl)
    if solved:
        for li in squarePrint(solved):
            print(li)
    else:
        print("No solution possible")
    end_time = time.time()
    print("Total Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))
#Shaurya Jain, pd 3, 2025
# *=+/
# /+=*
# =*/+
# +/*=
# "*=+//+=*=*/++/*="
# .................................................