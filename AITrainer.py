import cv2 
import numpy as np
import time 
import poseEstimationModule as pm

cap=cv2.VideoCapture("1.mp4")

detector=pm.poseDetector()
count=0
dir=0

pTime=0
while True:
    success,img=cap.read()
    img=detector.findPose(img,False)
    lmList=detector.findPosition(img,False)
    if len(lmList)!=0:
        angle=detector.findAngle(img,11,13,15)
        per = np.interp(angle,(185,290),(0,100))
        
        #check for the dumbell curls
        color=(255,0,255)
        if per==100:
            color=(0,255,0)
            if dir==0:
                count+=0.5
                dir=1 
        if per==0:
            color=(0,255,0)
            if dir==1:
                count+=0.5
                dir=0
                
        cv2.rectangle(img,(850,150),(800,400),color,3)
        cv2.rectangle(img,(850,150+250-int(per*2.5)),(800,400),color,cv2.FILLED)
        cv2.putText(img,f'{int(per)}',(800,130),cv2.FONT_HERSHEY_PLAIN,2,color,2)
        
        cv2.rectangle(img,(0,230),(250,480),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'{int(count)}',(40,400),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)