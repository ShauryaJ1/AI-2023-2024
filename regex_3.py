import sys; args = sys.argv[1:]
idx = int(args[0])-50
myRegexLst = [
  r"/(\w)*\w*\1\w*/i", #/\b(\w)(?!\1)\w*\b/
  r"/(\w)*(\w*\1){3}\w*/i",
  r"/^(0|1)([01]*\1)*$/",
  r"/\b(?=\w*cat)\w{6}\b/i",
  r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
  r"/\b(?!\w*cat)\w{6}\b/i",
  r"/\b((\w)(?!\w*\2))+\b/i",
  r"/^((?!10011)[01])*$/",
  r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",
  r"/^((?!1[01]1)[01])*$/"]
if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Shaurya Jain, pd 3, 2025