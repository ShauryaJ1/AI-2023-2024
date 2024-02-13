import sys; args = sys.argv[1:]
idx = int(args[0])-60
myRegexLst = [
  r"//",
  r"//",
  r"//",
  r"//",
  r"//",
  r"//",
  r"//",
  r"//",
  r"//",
  r"//"
]
if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Shaurya Jain, pd 3, 2025