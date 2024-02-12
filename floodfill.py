puzzle = '--#----###-----'

def runRoute(brd, row, col):
    width = 5
    height = 3
    if 0 <= col < width and 0 <=  row < height and brd[row*width+col] != "#" and brd[row*width+col] != ".":
        brd = brd[:row*width+col] + "." + brd[row*width+col+1:]
        brd = runRoute(brd, row-1, col)
        brd = runRoute(brd, row+1, col)
        brd = runRoute(brd, row, col-1)
        brd = runRoute(brd, row, col+1)
    return brd

def printPuzzle(puzzle,height,width):
    print('\n'.join(puzzle[i*int(width):(i+1)*int(width)] for i in range(int(height))))

printPuzzle(puzzle,3,5)
print()
printPuzzle(runRoute(puzzle,0,3),3,5)