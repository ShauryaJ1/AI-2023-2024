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
    #row1
    row= pzl[:5]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row2
    row= pzl[5:12]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row3
    row= pzl[12:19]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row4
    row= pzl[19:]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row5
    row= pzl[:2]+pzl[5:7]+pzl[12]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row6
    row= pzl[7:9]+pzl[13:15]+pzl[19]+pzl[2:4]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row7
    row= pzl[20:22]+pzl[15:17]+pzl[9:11]+pzl[4]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row8
    row= pzl[22:]+pzl[17:19]+pzl[9:11]+pzl[11]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row9
    row= pzl[3:5]+pzl[10:12]+pzl[18]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row10
    row= pzl[1:3]+pzl[8:10]+pzl[16:18]+pzl[23]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row11
    row= pzl[0]+pzl[6:8]+pzl[14:16]+pzl[21:23]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    #row12
    row= pzl[19:21]+pzl[12:14]+pzl[5]
    for tile in row:
            if row.count(tile)>1 and tile!=".":
                return True
            else:
                continue
    # for constraintSet in constraintSets:
    #      for tile in constraintSet:
    #           if constraintSet.count(tile)>1 and tile!="."
    #             return True
    #           else:
    #             continue
    return False
def isInvalid_constraintSets(pzl):
     for constraintSet in constraintSets:
         for tile in constraintSet:
              if constraintSet.count(tile)>1 and tile!=".":
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
    tiles = [1,2,3,4,5,6,7]
    empty_space = pzl.index(".")
    for tile in tiles:
        choices.append(replace_letters(pzl,empty_space,tile))
    return choices
def bruteForce(pzl):
    if isInvalid_constraintSets(pzl):
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
    global constraintSets
    constraintSets = [[0,1,2,6,7,8],[2,3,4,8,9,10],[5,6,7,12,13,14],[9,10,11,16,17,18],[7,8,9,14,15,16]
                      [13,14,15,19,20,21],[15,16,17,21,22,23],
                      [0,1,2,3,4],[5,6,7,8,9,10,11],[12,13,14,15,16,17,18],[19,20,21,22,23]
                      [0,1,5,6,12],[7,8,13,14,19,2,3],[20,21,15,16,9,10,4]]
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