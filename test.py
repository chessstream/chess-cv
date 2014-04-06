import cv2
import numpy as np

img = cv2.imread('img/sobelcropped.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,100,100,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,180)

# only use horizontal/vertical lines
def valid_line(theta):
    DIFFERENCE = np.pi/70
    ninety = np.pi/2;
    num = theta / ninety - np.floor(theta / ninety)
    return num * (np.pi/2) < DIFFERENCE

horizontal_lines = []
vertical_lines = []
for rho,theta in lines[0]:
    if (valid_line(theta)):
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        if x1 < -900 and x2 > 900:
          horizontal_lines.append([(x1, y1), (x2, y2)])
        if y1 > 900 and y2 < -900:
          vertical_lines.append([(x1, y1), (x2, y2)])
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)



gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
dst = cv2.cornerHarris(gray,3,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[255,0,0]

cv2.imwrite('houghlines3.jpg',img)