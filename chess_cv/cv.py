import cv2
import numpy as np
from new_game import initialize_game
from Square import Square

def crop_img(orig_img, sobel_img):
    #Make it grayscale
    gray = cv2.cvtColor(sobel_img,cv2.COLOR_BGR2GRAY)
    #Compute thresholds, don't need to use adaptive cause it's black and white
    ret,thresh = cv2.threshold(gray,127,255,0)
    #Calculate contours from thresh, no idea what ret is even for.
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Search for the biggest contour
    biggest = None
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 100:
            peri = cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i,0.02*peri,True)
            if area > max_area and len(approx)==4:
                biggest = approx
                max_area = area

    print biggest
    x_max = 0;
    x_min = 100000;
    y_max = 0
    y_min = 100000;
    for d in biggest:
       x = d[0][0] 
       y = d[0][1]
       if x > x_max:
           x_max = x
       if x < x_min:
           x_min = x
       if y > y_max:
           y_max = y
       if y < y_min:
           y_min = y
    
    x_start = x_min + 10
    x_end = x_max - 10
    y_start = y_min + 10
    y_end = y_max + 10
    new_original = orig_img[y_start:y_end, x_start:x_end]
    new_sobel = sobel_img[y_start:y_end, x_start:x_end]
    return new_original, new_sobel





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


def find_intersection(line1, line2, sobel_img):
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
    cv2.circle(sobel_img, (x, y), 3, (255, 0, 0), 2)
    return (x,y)


def find_squares(horizontal_lines, vertical_lines, orig_img, sobel_img):
    hori_ind = 1
    vert_ind = 1
    squares = np.empty(shape=(8,8), dtype=object)

    while hori_ind < len(horizontal_lines):
        top_line = horizontal_lines[hori_ind - 1]
        bottom_line = horizontal_lines[hori_ind]
        left_line = vertical_lines[vert_ind - 1]
        right_line = vertical_lines[vert_ind]

        # corners of square
        top_left = find_intersection(top_line, left_line, sobel_img)
        bottom_right = find_intersection(bottom_line, right_line, sobel_img)

        # crop squares
        orig_square = orig_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        sobel_square = sobel_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        squares[hori_ind - 1][vert_ind - 1] = Square(sobel_square, orig_img, hori_ind - 1, vert_ind - 1, board_state)

        vert_ind += 1
        if vert_ind == len(vertical_lines):
            vert_ind = 1
            hori_ind += 1

    initialize_game(squares)
    return squares

def find_everything(orig_img_path, sobel_img_path, board_state=None):
    orig_img_in = cv2.imread(orig_img_path)
    sobel_img_in = cv2.imread(sobel_img_path)
    orig_img, sobel_img = crop_img(orig_img_in, sobel_img_in)
    horizontal_lines, vertical_lines = hough_lines(sobel_img)

    cv2.imwrite('recentoutput.jpg',sobel_img)
    # more lines than necessary, so merge
    print(len(vertical_lines))
    print(len(horizontal_lines))
    
    if (len(vertical_lines) * len(horizontal_lines) > 49):
        merge_lines(vertical_lines)
        merge_lines(horizontal_lines)
    vertical_lines = sort_lines(vertical_lines, 'vertical')
    horizontal_lines = sort_lines(horizontal_lines, 'horizontal')

    # add edges to sobel_img
    for vert_line in vertical_lines:
        cv2.line(sobel_img,vert_line['p1'],vert_line['p2'],(0,0,255),2)
    for hori_line in horizontal_lines:
        cv2.line(sobel_img,hori_line['p1'],hori_line['p2'],(0,0,255),2)

    return find_squares(horizontal_lines, vertical_lines, orig_img, sobel_img, board_state)

