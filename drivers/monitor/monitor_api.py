#basic CV2 based display API (for the driver)
import cv2
import numpy as np

#clear output file
f = open('monitor_out.png','wb')
f.close()


debug = False
white = (255,255,255)
black = (0,0,0)
ctx = ''

#inititialize image
img = cv2.imread('monitor.png')

if debug:
    cv2.imshow('monitorout', img)
    cv2.waitKey(0)
print('Monitor API imported')

height, width, channels = img.shape

def imgwrite(text):
    global ctx, debug, img, white, black
    ctx = ctx + text
    
    if text == '\n':
        ctx = ctx + ''
        return None


    items = ctx.split('\n')
    index = 20
    for i in items:
        img = cv2.putText(img, i, (0,index), cv2.FONT_HERSHEY_SIMPLEX, 0.5, white)
        index = index + 20

    if debug:
        cv2.imshow('monitorout', img)
        cv2.waitKey(0)

    cv2.imwrite('monitor_out.png', img)

def deimgwrite(text):
    global ctx, debug, img, white, black
    ctx = ctx + text
    
    if text == '\n':
        ctx = ctx + ''
        return None

    items = ctx.split('\n')
    index = 20
    for i in items:
        img = cv2.putText(img, i, (0,index), cv2.FONT_HERSHEY_SIMPLEX, 0.5, black)
        index = index + 20

    if debug:
        cv2.imshow('monitorout', img)
        cv2.waitKey(0)

    cv2.imwrite('monitor_out.png', img)

def pxwrite(right,down,thic=3):
    global debug, img, white, black
    img[down-thic:down+thic,right-thic:right+thic] = white

    if debug:
        cv2.imshow('monitorout', img)
        cv2.waitKey(0)

    cv2.imwrite('monitor_out.png', img)

def depxwrite(right,down,thic=3):
    global debug, img, white, black
    img[down-thic:down+thic,right-thic:right+thic] = black

    if debug:
        cv2.imshow('monitorout', img)
        cv2.waitKey(0)
        
def imageblank(color = black):
    global img, ctx, black, white
    img[0:height,0:width] = black
    ctx = ''
    

    cv2.imwrite('monitor_out.png', img)

imgwrite('cv2 Basic Display API 1: on-startup self test successful\n4inches-usbstick/impostorcpu/drivers/monitor/monitor_api.py')
