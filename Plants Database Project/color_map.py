from datetime import datetime
import pandas as pd
import numpy as np
import cv2

h = 22
path = '101w.jpg'

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
color = (0, 0, 255)
thickness = 1

img = cv2.imread(path)

## convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

## mask of green (36,25,25) ~ (86, 255,255)
# mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
mask = cv2.inRange(hsv, (30, 25, 25), (80, 255, 255))


## slice the green
imask = mask>0
green = np.zeros_like(img, np.uint8)
green[imask] = img[imask]

imgDenoised = cv2.fastNlMeansDenoisingColored(green, None, 10, 10, 7, 21)
blur = cv2.bilateralFilter(imgDenoised, 7, 11, 11)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dilated = cv2.dilate(blur, kernel)
eroded = cv2.erode(dilated, kernel)


imgGreenChannel = eroded[:, :, 1]
ret, th = cv2.threshold(imgGreenChannel, 0, 255,
                        cv2.THRESH_BINARY)


cv2.imwrite("green.png", th)

