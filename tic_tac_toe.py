tknToPlay = 'x'
startingBoard = '.'*9
board = startingBoard
constraintSets = [[0,1,2],[3,4,5],[6,7,8],[1,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]
def gameOver(brd):
    if brd.count('.') == 0:
        return True
    for cSet in constraintSets:
        temp = ''.join([brd[idx] for idx in cSet])
        if temp == 'xxx' or temp=='ooo':
            # print(cSet,temp)
            return True
    
    return False
def play(brd,tkn,mv):
    return brd[:mv] + tkn + brd[mv+1:], 'x' if tkn =='o' else 'o'
# print(play(startingBoard,'x',8))
# while not gameOver(startingBoard):
#     for i in range(9):
brds = []
move_sets = []
def bruteForce(brd,tknToPlay):
    
    if gameOver(brd):
        brds.append(brd)

        # print(brd)
    else:
        empty_spaces = {idx for idx,c in enumerate(brd) if c=='.'}
        for empty_space in empty_spaces:
            new_brd,tknToPlay = play(board,tknToPlay,empty_space)
            bruteForce(new_brd,tknToPlay)
for i in range(9):
    while not gameOver(board):
        empty_spaces = {idx for idx,c in enumerate(board) if c=='.'}
        if empty_spaces:
            new_brd,tknToPlay = play(board,tknToPlay,[*empty_spaces][0])
            board = new_brd
        else:
            break

def print2D(brd):
    print(brd[:3]+'\n'+brd[3:6]+'\n'+brd[6:])
bruteForce(startingBoard,'x')
print(len(set(brds)))