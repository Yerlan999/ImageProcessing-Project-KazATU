from datetime import datetime
import pandas as pd
import numpy as np
import cv2


h = 22
path = '86w.jpg'

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
color = (0, 0, 255)
thickness = 1

img = cv2.imread(path)

imgDenoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
imgGreenChannel = imgDenoised[:, :, 1]
edges = cv2.Canny(imgGreenChannel, 100, 200)
blur = cv2.bilateralFilter(imgGreenChannel, 7, 11, 11)
ret, th = cv2.threshold(blur, 130, 255,
                        cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dilated = cv2.dilate(edges, kernel)
eroded = cv2.erode(dilated, kernel)


contours, hierarchy = cv2.findContours(
    eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (255, 0, 0), 1)


total_area = 0
biggest_area = {
    "area": 0,
    "contour": None,
}

for cnt in contours:

    area = cv2.contourArea(cnt)
    if area > biggest_area["area"]:
        biggest_area["area"] = area
        biggest_area["contour"] = cnt
    total_area += area
    M = cv2.moments(cnt)

    try:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    except ZeroDivisionError:
        continue

    cv2.putText(img, str(area), (cx, cy), font,
                fontScale, color, thickness, cv2.LINE_AA)


cv2.putText(img, str(total_area), (50, 50), font,
            fontScale, (255, 255, 0), 3, cv2.LINE_AA)


hull = cv2.convexHull(biggest_area["contour"])
# rect = cv2.minAreaRect(biggest_area["contour"])
# box = cv2.boxPoints(rect)
# box = np.int0(box)
cv2.drawContours(img,[hull],0,(0,0,255),2)


inverted_thresh = 255 - th

stencil = np.zeros(inverted_thresh.shape).astype(img.dtype)
color = [255, 255, 255]
cv2.fillPoly(stencil, [hull], color)
result = cv2.bitwise_and(inverted_thresh, stencil)


cv2.imwrite("result.jpg", result)
cv2.imwrite("thres.jpg", inverted_thresh)
cv2.imwrite('test.jpg', img)

print(hull)
print("Done!")
