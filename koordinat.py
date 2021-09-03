import cv2
import numpy as np

camera = cv2.VideoCapture(0)
def nothing():
    pass
while True :
    _,frame = camera.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernal = np.ones((5,5), "uint8")

    low_red = np.array([0,174,0])
    high_red = np.array([5,255,255])

    red_mask = cv2.inRange(hsv, low_red, high_red)
    dilated_redmask = cv2.dilate(red_mask, kernal)
    blured_redmask = cv2.GaussianBlur(dilated_redmask, (5,5), 4/6)

    contours_red, hierarchy = cv2.findContours(blured_redmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i=0

    for pic, contour in enumerate(contours_red):
        area = cv2.contourArea(contour)
        if area > 3000 :
            x, y, w, h = cv2.boundingRect(contour)
            i+=1
            if i == 2:
                break

            merkezX = x+(w/2)
            merkezY = y+(h/2)

            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

            if y < 10 and x <= 360 :
                frame = cv2.putText(frame, f"x={merkezX} y={merkezY}", (350, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            elif y > 10 and x <= 360 :
                frame = cv2.putText(frame, f"x={merkezX} y={merkezY}", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
            elif y > 10 and x > 360 :
                frame = cv2.putText(frame, f"x={merkezX} y={merkezY}", (350, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)



    cv2.imshow("Frame", frame)
    if cv2.waitKey(1)==ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
