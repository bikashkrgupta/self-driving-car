# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 03:14:06 2019

@author: Lenovo
"""
""" 
canny edge---

"""
import cv2
import matplotlib.pyplot as plt
import numpy as np


def make_cordinates(image,line_parameters):
    slope,intercept=line_parameters
    print(image.shape)
    
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])



# distinguish left and right lines
# draw a single line for each

def average_slope_intercept(image,lines):
    left_fit=[]
    right_fit=[]
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parameters=np.polyfit((x1,x2),(y1,y2),1)   # use it outside for understand
        slope,intercept=parameters[0],parameters[1]
        if slope<0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average=np.average(left_fit,axis=0)
    right_fit_average=np.average(right_fit,axis=0)
        # make cordinates out of slope and intercept
    left_line = make_cordinates(image,left_fit_average)
    right_line = make_cordinates(image,right_fit_average)
    return np.array([left_line,right_line])



def display_lines(image,lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
    return line_image
    

def canny(image):
    blur=cv2.GaussianBlur(image,(5,5),1,1)   
    edges=cv2.Canny(image,50,150)  # detect edeges    
    return edges

def region_of_interest(image):
    height=image.shape[0]
    polygon=np.array([[(200,height),(1000,height),(600,250)]])        #  3 tuple, 1 will be
    mask=np.zeros_like(image)
    cv2.fillPoly(mask,polygon,255)
    masked_image=cv2.bitwise_and(mask,image)
    return  masked_image

img=cv2.imread(r'\img\test_image.jpg')
lane_image=img.copy()
edge = canny(lane_image)
cropped_image=region_of_interest(edge)

lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=4)               # 2,np.pi/180 angle

averaged_lines=average_slope_intercept(lane_image,lines)

drawn_lines= display_lines(lane_image,averaged_lines)  

combo_image = cv2.addWeighted(lane_image,
                              0.8,
                              drawn_lines,1,1)    # opacity


""" what to crop dimension
plt.imshow(img)
plt.grid()
plt.show()  """



cv2.imshow('lane',combo_image)
cv2.waitKey(0)
cv2.destroyAllWindows()