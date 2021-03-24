import cv2
import numpy as np


# ФУНКЦИЯ ДЛЯ ВЫВОДА ИЗОБРАЖЕНИИ В МАТРИЦЕ
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


# ФУНКЦИЯ ДЛЯ ОБОЗНАЧЕНИЯ КОНТУРА
def getContours(img):
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area>300:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, 0.001*peri, True) # ТОЧНОСТЬ КРИВИЗНЫ КОНТУРА !!!!
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)


            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2) # ЗАКЛЮЧЕНИЕ В ПРЯМОУГОЛЬНИКИ
            cv2.putText(imgContour,str(area),
                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (0,0,0),2)


cv2.imshow("Stack", imgContour)
cv2.imwrite('43.5cm_result.jpg', imgCanny)
cv2.waitKey(0)




## LOOP FOR SHOWING IMAGE
while True:
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == 27: # or ord('q')
        break

cv2.destroyAllWindows()



## MORE CANVAS SPACE FOR WORK ON !!!
fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111)
ax.imshow(gray_img, cmap='gray')


    cont_list.sort()
    max_cont = cont_list.pop()
    real_area = max_cont - sum(cont_list)
    print("Real Area: ", real_area)


## convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
## mask of green (36,25,25) ~ (86, 255,255)
mask = cv2.inRange(hsv, (0, 0, 0), (255, 255, 255))
# mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))
## slice the green
imask = mask>0
green = np.zeros_like(img, np.uint8)
green[imask] = img[imask]
## save
cv2.imwrite("green.jpg", green)
