import cv2
import numpy as np

cap = cv2.VideoCapture(0)
j = 0

while True:
    ###Changes
    width  = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("Width, Height: ", width, height)
    ###
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #red color
    low_red=np.array([161,130,84])
    high_red=np.array([179,255,255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    _, contours, _= cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    for i in contours:
        (x, y, w, h) = cv2.boundingRect(i) 
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        x_mid = int((x+x+w)/2)
        y_mid = int((y+y+h)/2)
        cv2.line(frame, (x_mid, 0), (x_mid, 480), (0, 255, 0), 2)
        cv2.line(frame, (0, y_mid), (640, y_mid), (0, 255, 0), 2)
        #break
        area = int(w*h)
        #print(area)
        #break
        
        distance = int(9132.7 * (area**-0.47))
        l = 'distance in cm =', distance
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,str(l),(15,40), font, .5,(255,255,255),2,cv2.LINE_AA)
        j+=10
        if l == ord('q'):
            break
    
        deltax = int(abs(320-(x+h/2)))
        k = "delta x =", deltax
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,str(k),(15,65), font, .5,(255,255,255),2,cv2.LINE_AA)
        j+=10
        if k == ord('q'):
            break
        
        deltay = int(abs(190-(y+w/2)))
        n = "delta y =", deltay
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,str(n),(15,90), font, .5,(255,255,255),2,cv2.LINE_AA)
        j+=10
        if n == ord('q'):
            break
        
        m = "pixel area =", area
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,str(m),(15,15), font, .5,(255,255,255),2,cv2.LINE_AA)
        j+=10
        if m == ord('q'):
            break
        
        if int(320-(x+h/2))>0:
            cv2.putText(frame,str('Turn left'),(550, 15), font, .5,(255,255,255),2,cv2.LINE_AA)
        if int(320-(x+h/2))<0:
            cv2.putText(frame,str('Turn right'),(550, 15), font, .5,(255,255,255),2,cv2.LINE_AA)
        if int(190-(y+w/2))>0:
            cv2.putText(frame,str('Go up'),(550, 40), font, .5,(255,255,255),2,cv2.LINE_AA)
        if int(190-(y+w/2))<0:
            cv2.putText(frame,str('Go down'),(550, 40), font, .5,(255,255,255),2,cv2.LINE_AA)
        
        break
    ###
    print("Width, Height: ", width, height)
    ###
    cv2.circle(frame, (320,190), 2, (255,255,255), 1)
    cv2.imshow("Frame", frame)
    #cv2.imshow("mask", red_mask)
    
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()


