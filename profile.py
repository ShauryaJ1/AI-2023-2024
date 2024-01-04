import pprofile
from othello_5 import main
with pprofile.Profile() as prof:
    main()

prof.dump_stats('othello_5.txt')