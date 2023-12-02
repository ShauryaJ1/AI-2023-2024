import sys; args = sys.argv[1:]
# import time
# import math
# import re
# import random
# start_time=time.time()
# r"/^.{2,4}$/is"
idx = int(args[0])-30
# r"/^100$|^101$|^0$/"
# r"/^10[01]$|^0$/"
#"/^.*?\b\w*d\w*\b/mi"
#"/^.*?\w*d\w*?\b/mi"
myRegexLst = [
  r"/^10[01]$|^0$/",
  r"/^[01]*$/",
  r"/0$/",
  r"/\w*[aeiou]\w*[aeiou]\w*/i",
  r"/^1[01]*0$|^0$/",
  r"/^[01]*110[01]*$/",
  r"/^.{2,4}$/s",
  r"/^\d{3} *-? *\d\d *-? *\d{4}$/",
  r"/^.*?d\w*/mi",
  r"/^1[01]*1$|^0[01]*0$|^[10]?$/"]
char_count = sum([len(exp)-exp.count("/") for exp in myRegexLst])
print(char_count)
if idx < len(myRegexLst):
  print(myRegexLst[idx])


# end_time=time.time()
#Shaurya Jain, pd 3, 2025
