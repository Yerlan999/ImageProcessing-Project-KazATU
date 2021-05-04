from datetime import datetime
import pandas as pd
import numpy as np
import cv2


# FOR IMAGES WITH DIMETNSION 2048 x 1536 !!!
h = 30
path = '20.jpg'

#
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 3
color = (0, 255, 0)
thickness = 2


img = cv2.imread(path)

imgDenoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
imgGreenChannel = imgDenoised[:,:,1]
blur = cv2.bilateralFilter(imgGreenChannel,7,11,11)
ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

unique, counts = np.unique(th, return_counts=True)
result = dict(zip(unique, counts))

real_cm2 = round((result[255]/(14.695*(h**2) - 1148.5*h + 24123)),2)
corrected_real_cm2 = real_cm2 - real_cm2*0.10
img_height, img_width, _ = img.shape
org = (10, img_height-10)
current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")

cv2.putText(img, str(corrected_real_cm2) + ' cm2. ' + str(current_datetime), org, font,
                   fontScale, color, thickness, cv2.LINE_AA)


cv2.imwrite('test0001.jpg', img)
cv2.imwrite('test001.jpg', th)
print("Finished!")
