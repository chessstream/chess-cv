import numpy as np

def board_string_to_array_of_locations(board):
	"""A board string is a python list of 8 strings of 8 characters
	"""
	return np.array( [[char_to_location(board[line][c]) for c in line] 
		for line in board] )

def char_to_location(c):
	if ord(c) in range(ord('a'), ord('z') + 1):
		color = 'B'
	else:
		color = 'W'