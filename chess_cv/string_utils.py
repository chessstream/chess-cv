import numpy as np
from game import Location

def board_string_to_location_array(board):
	"""A board string is a python list of 8 strings of 8 characters
	"""
	return np.array([[char_to_location(board[line][c], c, line) 
		for c in range(len(board[line]))] 
		for line in range(len(board))] )

def char_to_location(c, x, y):
	if ord(c) in range(ord('a'), ord('z') + 1):
		color = 'B'
	else:
		color = 'W'
	if c == '_':
		c = None
	return Location(x, y, c, color)

def compare_square_array_to_location_array(squares, locations):
	pass

def location_array_to_fen(locations):
	pass