import cv2
import numpy as np

img = cv2.imread('img/sobelcropped.png')
horizontal_lines, vertical_lines = hough_lines(img)

# more lines than necessary, so merge
if (len(vertical_lines) * len(horizontal_lines) > 49):
    merge_lines(vertical_lines)
    merge_lines(horizontal_lines)

# only use horizontal/vertical lines
def valid_line(theta):
    DIFFERENCE = np.pi/70
    ninety = np.pi/2;
    num = theta / ninety - np.floor(theta / ninety)
    return num * (np.pi/2) < DIFFERENCE

def hough_lines(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,175,apertureSize = 3)
    lines = cv2.HoughLines(edges,1,np.pi/180,180)
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
            #cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    return (horizontal_lines, vertical_lines)

THETA_DIFF = np.pi/1
MAGNITUDE_DIFF = 25

def merge_lines(lines):
    """
    Merge similar lines
    lines: Array of dictionarys with rho and theta attributes
    """
    i = 0
    while i in range(len(lines)):
        j = 0
        while j in range(len(lines)):
            # if lines have same angle
            if (i != j and 
                abs(lines[i]['theta'] - lines[j]['theta']) < THETA_DIFF and 
                abs(lines[i]['rho'] - lines[j]['rho']) < MAGNITUDE_DIFF):
                del lines[j]
                print('similar')
            j+=1
        i+=1

# display lines
for vert_line in vertical_lines:
    cv2.line(img,vert_line['p1'],vert_line['p2'],(0,0,255),2)

for hori_line in horizontal_lines:
    cv2.line(img,hori_line['p1'],hori_line['p2'],(0,0,255),2)

def findIntersection(line1, line2):
    pass