import sys; args = sys.argv[1:]
idx = int(args[0])-40
myRegexLst = [
  r"/^[x.o]{64}$/i",
  r"/^[xo]*\.[xo]*$/i",
  r"/\.o*x+$|^x+o*\.|^\.|\.$/i",#\.o*x+$|^x+o*\.|^\.|\.$
  r"/^.(..)*$/s",
  r"/^(0|1[10])([01]{2})*$/",#^(0([01]{2})*|1([01]{2})*[01])$
  r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aieu]|u[aioe])\w*/i",
  r"/^(1?0+|1+$)*$/",
  r"/^(a[bc]*|[bc]+a?[bc]*)$/",#^(a[bc]*|[bc]+|[bc]*a|[bc]*a[bc]*)$
  r"/^([bc]|(a[bc]*){2})+$/",#^(([bc]*a[bc]*){2})+$|^[bc]+$
  r"/^(2[02]*|(1[02]*){2})+$/"]#^(2(([20]*1){2})*[20]*|((1[20]*){2})+)$
#/^(2[02]*|((1[02]){2})+)$/
#/^([bc]|(a[bc]*){2})+$/
if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Shaurya Jain, pd 3, 2025
