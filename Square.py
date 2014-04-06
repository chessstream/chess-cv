import cv2;

class Square():
	SOBEL_MIN = 10;

	def __init__(self, sobel_img, color_img, x, y, boardinfo=None):
		self.boardinfo = boardinfo
		self.sobel_img = sobel_img
		self.color_img = color_img
		self.x = x
		self.y = y
		
	@property
	def square_color(self):
		self.square_color = self.boardinfo['color'][(self.x + self.y) % 2]
		return self.square_color

	@property
	def has_piece(self):
		avg = self.sobel_img[10:-10, 10:-10].mean()
		self.has_piece = avg > Square.SOBEL_MIN
		return self.has_piece

	@property
	def piece_color(self):
		if not self.has_piece:
			return False
		if self.square_color == 'W':
			if self.w_w_diff < self.b_w_diff:
				# White piece on a white square
				self.piece_color = 'W'
			else:
				# Black piece on a white square
				self.piece_color = 'B'
		else:
			if self.w_b_diff < self.b_b_diff:
				# White_piece on a black square
				self.piece_color = 'W'
			else:
				# Black piece on a black square
				self.piece_color = 'B'
		return self.piece_color

	@property
	def color_average(self):
		self.color_average = \
				(self.color_img[:, :, 0].mean(), 
			 	 self.color_img[:, :, 1].mean(), 
				 self.color_img[:, :, 2].mean())
		return self.color_average

	@property
	def sobel_average(self):
		self.sobel_average = \
				(self.sobel_img[:, :, 0].mean(), 
			 	 self.sobel_img[:, :, 1].mean(), 
				 self.sobel_img[:, :, 2].mean())
		return self.sobel_average

	@property
	def w_w_diff(self):
		self.w_w_diff = color_diff(self.color_average, self.boardinfo['w_w'])
		return self.w_w_diff

	@property
	def b_w_diff(self):
		self.w_w_diff = color_diff(self.color_average, self.boardinfo['b_w'])
		return self.b_w_diff

	@property
	def w_b_diff(self):
		self.w_b_diff = color_diff(self.color_average, self.boardinfo['w_b'])
		return self.w_b_diff

	@property
	def b_b_diff(self):
		self.b_b_diff = color_diff(self.color_average, self.boardinfo['b_b'])
		return self.b_b_diff
	
	def __repr__(self):
		string = str((self.x, self.y)) + ": " + str(self.has_piece)
		if self.has_piece:
			string += ", " + str(self.piece_color)
		return string

def color_diff(tup1, tup2):
	total = 0
	for i in range(min(len(tup1), len(tup2))):
		total += abs(tup1[i] - tup2[i])

if __name__ == '__main__':
	s = Square( cv2.imread('img/chessboard.jpg'), 
				cv2.imread('img/chessboard.jpg'), 1, 2, {'color':['W', 'B']})