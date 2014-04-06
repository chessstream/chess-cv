#!/usr/bin/python

import sys
import chess_cv

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
print sys.argv[0]

if len(sys.argv) == 3:
    chess_cv.start_game(sys.argv[1], sys.argv[2])

elif len(sys.argv) == 4:
    chess_cv.start_game(sys.argv[1], sys.argv[2], sys.argv[3])

else:
    print 'This command requires 2 or 3 arguments'
