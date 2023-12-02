import sys; args = sys.argv[1:]
import math
import time
def isInvalid(pzl):
    #hex1
    hex = pzl[:3] + pzl[6:9]
    for tile in hex:
            if hex.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #hex2
    hex = pzl[2:5] + pzl[8:11]
    for tile in hex:
            if hex.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #hex3
    hex = pzl[5:8] + pzl[12:15]
    for tile in hex:
            if hex.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #hex4
    hex = pzl[9:12] + pzl[16:19]
    for tile in hex:
            if hex.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #hex5
    hex = pzl[7:10] + pzl[14:17]
    for tile in hex:
            if hex.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #hex6
    hex = pzl[13:16] + pzl[19:22]
    for tile in hex:
            if hex.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #hex7
    hex = pzl[15:18] + pzl[21:]
    for tile in hex:
            if hex.count(tile)>1 and tile!=".":
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
    tiles = [1,2,3,4,5,6]
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

def hexPrint(pzl):
    prints = []
    prints.append(" "+pzl[:5])
    prints.append(pzl[5:12])
    prints.append(pzl[12:19])
    prints.append(" "+pzl[19:])
    return prints



if __name__ == "__main__":
    if len(args) == 0:
        pzl = "."*24
    else:
        pzl = args[0]
    start_time = time.time()
    solved = bruteForce(pzl)
    if solved:
        for li in hexPrint(solved):
            print(li)
    else:
        print("No solution possible")
    end_time = time.time()
    # for li in hexPrint("ABCDEFGHIJKLMNOPQRSTUVWX"):
    #      print(li)
    # print(setOfChoices('1.......................'))
    # print(isInvalid('11......................'))
    print("Total Time: {}s".format(round(end_time-start_time, 3 - len(str(end_time-start_time).split('.')[0]))))


#Shaurya Jain, pd 3, 2025
#"........................"