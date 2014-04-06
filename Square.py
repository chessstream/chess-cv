import cv2;

class Square():
	SOBEL_MIN = 10;

	def __init__(self, sobel_img, color_img, x, y):
		self.sobel_img = sobel_img
		self.color_img = color_img
		self.x = x
		self.y = y

		self.color = None;
		self.exists = self.sobel_detect()
		if self.exists:
		  	self.color = color_detect()

	def sobel_detect(self):
		avg = self.sobel_img[10:-10, 10:-10].mean()
		self.exists = avg > Square.SOBEL_MIN
		# self.color_avg

	def color_detect(self, infopacket):
		color_average()
		self.infopacket = infopacket
		color = infopacket['color'][(self.x + self.y) % 2]
		if color == "W":
			diffW = infopacket['']
			diffB = infopacket['']
			#YO, FIX THIS

	@property
	def color_average(self):
		self.
		return (self.color_img[:,:,0].mean(), 
			 	self.color_img[:,:,1].mean(), 
				self.color_img[:,:,2].mean())


if __name__ == '__main__':
	s = Square(cv2.imread('test.jpg'), cv2.imread('test.jpg'), 1, 2)