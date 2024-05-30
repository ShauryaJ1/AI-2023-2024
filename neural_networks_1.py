import sys;args=sys.argv[1:]
import math
def file_to_lines():
    return open(args[0]).read().splitlines()
def dot_product(v1,v2):
    return sum([v1[i]*v2[i] for i in range(len(v1))])
def transfer_function(x,transferFunction):
    if transferFunction=='T1':
        return x
    elif transferFunction=='T2':
        return x*(x>0)
    elif transferFunction=='T3':
        return 1/(1+math.exp(-x))
    else:
        return (2*1/(1+math.exp(-x)))-1
def hadamard(v1,v2):
    return [v1[i]*v2[i] for i in range(len(v1))]
if __name__ == '__main__':
    lines = file_to_lines()
    transferFunction = args[1]
    inputs = [float(i) for i in args[2:]]
    lines = [[float(l) for l in line.split(' ')] for line in lines]
    for line in lines[:-1]:
        split_num = len(inputs)
        inputs = [transfer_function(dot_product(line[i:i+split_num],inputs),transferFunction) for i in range(0,len(line),split_num)]
    print(' '.join([str(i) for i in [i for i in hadamard(inputs,lines[-1])]]))

#Shaurya Jain, pd 3, 2025