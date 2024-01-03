import sys
sys.setrecursionlimit(100000)
cache = {}
def change(n,coinLst):
    
    
    if n==0:
            return 1

    if(n<0):
        return 0
    if not coinLst:
        return 0
    key = (n,*coinLst)
    if key in cache:
        return cache[key]
    
            
    cache[(n,*coinLst)] = change(n-coinLst[0],coinLst)+change(n,coinLst[1:])
    return cache[key]
if __name__=="__main__":
    print(change(10000,[100,50,25,10,5,1]))

