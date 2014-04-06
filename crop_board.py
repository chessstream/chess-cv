import cv2
import numpy as np

#img = cv2.imread('img/phone2.jpg')

def get_crop_pts(img):
    #Make it grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
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

    return biggest
    '''
    Sample debugging output:
    print biggest
    print type(biggest)
    print biggest.shape

    [[[ 46 245]]

    [[ 40 683]]

    [[478 680]]

    [[475 252]]]
    <type 'numpy.ndarray'>
    (4, 1, 2)
    '''
'''
Misc debug code
biggest = get_crop_pts(img)
cv2.drawContours(img,biggest,-1,(0,255,0),3)
cv2.imwrite('cropout.jpg', img)
'''

