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
    seedH, split = seedString[:b:=(seedString.index('x'))], seedString[b+1:]
    split_index = [i for c,i in enumerate(split) if 48<=ord(c)<=57][-1] #not gonna work because if chars doesnt exist it will break
    seedW, chars = split[:split_index] , split[split_index+1:]
    
if __name__ == "__main__":
    print()