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
				disappeared = (row, col)
			elif squares[row][col].has_piece and not locations[row][col].piece:
				appeared = (row, col)

	return disappeared, appeared

def update_location_array(locations, squares, disappeared, appeared):
	"""Destructive: changes locations in place.
	appeared and disappeared are (row, col), not (x, y)"""
	if not appeared:
		# A piece was taken
		pass
	else:
		# Generic move
		piece = locations[disappeared[0]][disappeared[1]].piece
		color = locations[disappeared[0]][disappeared[1]].color
		locations[disappeared[0]][disappeared[1]].piece = None
		locations[disappeared[0]][disappeared[1]].color = None
		locations[appeared[0]][appeared[1]].piece = piece
		locations[appeared[0]][appeared[1]].color = color
		

def location_array_to_board_string(locations):
	pass

def location_array_to_fen(locations, rotation):
	pass