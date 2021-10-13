
import cv2
import numpy as np
import colorgram

img = cv2.imread('picture.jpg')

print("1) \t Color Recognizer")
print("2) \t View Text of Picture")
print("3) \t Quit from program")
cho = int ( input("please enter your choice <1-3> : ") )
print(" ")

if cho == 3 :
    cv2.destroyAllWindows()
        
if cho == 2 :
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,threshold = cv2.threshold(gray,12,125,cv2.THRESH_BINARY)
    th = cv2.adaptiveThreshold(gray,125,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1)
        
    cv2.imshow('page',img)
    cv2.imshow('paget',threshold)
    cv2.imshow('threshAdaptive',th)

if cho == 1 :
    colors = colorgram.extract('picture.jpg', 4)

    # colorgram.extract returns Color objects, which let you access..
    # RGB, HSL, and what proportion of the image was that color.
    first_color = colors[0]
    rgb = first_color.rgb # e.g. (255, 151, 210)
    hsl = first_color.hsl # e.g. (230, 255, 203)
    proportion  = first_color.proportion # e.g. 0.34

    # RGB and HSL are named tuples, so values can be accessed as properties.
    # These all work just as well:
    red = rgb[0]
    red = rgb.r
    saturation = hsl[1]
    saturation = hsl.s
        
    i=0;
    while(i<4):
        print(colors[i])
        i = i+1
    print(" ")
