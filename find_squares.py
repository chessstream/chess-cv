import cv2
import numpy as np

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
            j+=1
        i+=1

def sort_lines(lines, orientation):
    if orientation == 'horizontal':
        ind = 1
    elif orientation == 'vertical':
        ind = 0
    # sort by average of points
    return sorted(lines, key=lambda line: (line['p1'][ind] + line['p1'][ind])/2)


def find_intersection(line1, line2, img):
    # diff in x-coordinates for both lines
    diffx1 = line1['p1'][0] - line1['p2'][0]
    diffx2 = line2['p1'][0] - line2['p2'][0]
    # slopes
    m1 = None if (diffx1 == 0) else (line1['p1'][1] - line1['p2'][1]) / diffx1
    m2 = None if (diffx2 == 0) else (line2['p1'][1] - line2['p2'][1]) / diffx2
    # y-intercepts
    b1 = None if (diffx1 == 0) else line1['p1'][1] - m1 * line1['p1'][0]
    b2 = None if (diffx2 == 0) else line2['p1'][1] - m2 * line2['p1'][0]

    # assume we only have 1 vertical line
    if m1 == None:
        x = line1['p1'][0]
    elif m2 == None:
        x = line2['p1'][0]
    else:
        x = ((b2-b1) / (m1-m2))

    # TODO: parallel lines

    y = m1 * x + b1
    cv2.circle(img, (x, y), 3, (255, 0, 0), 2)
    return (x,y)


def find_squares(horizontal_lines, vertical_lines, img):
    hori_ind = 1
    vert_ind = 1
    while hori_ind < len(horizontal_lines):
        top_line = horizontal_lines[hori_ind - 1]
        bottom_line = horizontal_lines[hori_ind]
        left_line = vertical_lines[vert_ind - 1]
        right_line = vertical_lines[vert_ind]

        # corners of square
        top_left = find_intersection(top_line, left_line, img)
        bottom_right = find_intersection(bottom_line, right_line, img)
        square = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        cv2.imwrite('square.jpg', square)

        vert_ind += 1
        if vert_ind == len(vertical_lines):
            vert_ind = 1
            hori_ind += 1

if __name__ == '__main__':
    img = cv2.imread('img/sobelcropped.png')
    horizontal_lines, vertical_lines = hough_lines(img)

    # more lines than necessary, so merge
    if (len(vertical_lines) * len(horizontal_lines) > 49):
        merge_lines(vertical_lines)
        merge_lines(horizontal_lines)
    vertical_lines = sort_lines(vertical_lines, 'vertical')
    horizontal_lines = sort_lines(horizontal_lines, 'horizontal')
    print(len(horizontal_lines), len(vertical_lines))

    # display lines
    for vert_line in vertical_lines:
        cv2.line(img,vert_line['p1'],vert_line['p2'],(0,0,255),2)

    for hori_line in horizontal_lines:
        cv2.line(img,hori_line['p1'],hori_line['p2'],(0,0,255),2)

    find_squares(horizontal_lines, vertical_lines, img)

    cv2.imwrite('houghlines3.jpg',img)
