import sys; args = sys.argv[1:]
import math
import time 
global h
global w
global num_squares
def file_to_lines():
    return open(args[2]).read().splitlines()
h,w = args[0][:b:=(args[0].index('x'))] + args[0][1+b:]
num_squares = args[1]

seedStrings = args[3]

def seedStringBreakdown(seedString):
    orientation  = seedString[0]

if __name__ == "__main__":
    print()