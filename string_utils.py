import numpy as np

def board_string_to_array(board, boardinfo = None):
	"""A board string is a python list of 8 strings of 8 characters
	"""
	return np.array( [[char_to_square(c, boardinfo) for c in line] 
		for line in board] )

def char_to_square(c):
	if ord(c) in range(ord('a'), ord('z') + 1):
		pass