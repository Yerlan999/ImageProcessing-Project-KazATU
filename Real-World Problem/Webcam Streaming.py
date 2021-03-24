import cv2
import numpy as np


def draw_rectangle(event, x, y, flags, param):

    global pt1, pt2, topLeft_clicked, botRight_clicked

    if event == cv2.EVENT_LBUTTONDOWN:
        if topLeft_clicked and botRight_clicked:
            pt1 = (0, 0)
            pt2 = (0, 0)
            topLeft_clicked = False
            botRight_clicked = False
        if topLeft_clicked == False:
            pt1 = (x, y)
            topLeft_clicked = True
        elif botRight_clicked == False:
            pt2 = (x, y)
            botRight_clicked = True




pt1 = (0, 0)
pt2 = (0, 0)
topLeft_clicked = False
botRight_clicked = False


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # <--- IMPORTANT PART FOR WEBCAM STREAMING

cv2.namedWindow('Test')
cv2.setMouseCallback('Test', draw_rectangle)


width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))



# writer = cv2.VideoWriter('myfirstvideo.mp4v', cv2.VideoWriter_fourcc(*'DIVX'), 100, (width, height))


while True:
    ret, frame = cap.read()
    # writer.write(frame)

    if topLeft_clicked:
        cv2.circle(frame, center=pt1, radius=5, color=(0, 0, 255), thickness=-1)
    if topLeft_clicked and botRight_clicked:
        cv2.rectangle(frame, pt1, pt2, (0, 0, 255), 3)

    cv2.imshow('Test', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
# writer.release()
cv2.destroyAllWindows()
# heif
