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
	disappeared, appeared = None, None
	for row in range(len(locations)):
		for col in range(len(locations[row])):
			if locations[row][col].piece and not squares[row][col].has_piece:
				disappeared = (col, row)
			elif squares[row][col].has_piece and not locations[row][col].piece:
				appeared = (col, row)

	return disappeared, appeared

def update_location_array(locations, squares, disappeared, appeared):
	if not appeared:
		# A piece was taken
		pass
	else:
		# Generic move
		pass

def location_array_to_fen(locations):
	pass