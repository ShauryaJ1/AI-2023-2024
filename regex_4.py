import sys; args = sys.argv[1:]
idx = int(args[0])-60
myRegexLst = [
  r"/^((?!010)[01])*$/",
  r"/^((?!010|101)[01])*$/",
  r"/^(0|1)([01]*\1)*$/",
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