import cv2
import numpy as np

img = cv2.imread('img/phone2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,175,apertureSize = 3)

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
          horizontal_lines.append({'rho': rho, 'theta': theta, 'p1': (x1, y1), 'p2': (x2, y2)})
        if y1 > 900 and y2 < -900:
          vertical_lines.append({'rho': rho, 'theta': theta, 'p1': (x1, y1), 'p2': (x2, y2)})
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

MAGNITUDE_DIFF = 100

# more lines than necessary, so merge
if (len(vertical_lines) * len(horizontal_lines) > 49):
    for i in range(len(vertical_lines)):
        for j in range(len(vertical_lines)):
            pass
            # if lines have same angle
            #if i != j and vertical_lines[i]['theta'] == vertical_lines[i][theta] and abs(vertical_lines[i]['rho'] - vertical_lines[i]['rho']) < MAGNITUDE_DIFF:
                #vertical_lines[j]['theta'])

print(len(vertical_lines))
        


def findIntersection(line1, line2):
    pass

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
dst = cv2.cornerHarris(gray,3,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[255,0,0]

cv2.imwrite('houghlines3.jpg',img)