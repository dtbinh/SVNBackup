'''
Created on 2014-9-17

@author: Walter
'''

import cv2
import numpy as np

img_filename = 'simplecircles.ppm'
img_filename = 'circles.ppm'
img_filename = 'coins.jpg'

img = cv2.imread(img_filename,0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,10,param1=200,param2=100,minRadius=0,maxRadius=0)

print circles

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()