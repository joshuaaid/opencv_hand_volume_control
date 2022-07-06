import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

#############################
#pycaw paketinin pip install eledik ve proyekte daxil edirik
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#############################
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volumeRange=volume.GetVolumeRange() # -65-0
minVol=volumeRange[0]
maxVol=volumeRange[1]
#print(volumeRange)
vol=0
volForBar=400
volForPer=0
#volume.SetMasterVolumeLevel(0, None)

#############################
#Webcam caption width and height
vCam, hCam=640, 480
#############################

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
cap.set(3,vCam)
cap.set(4,hCam)
pTime=0

detector = htm.HandDetector(detectionCon=0.7)

while True:
    success, img =cap.read()
    img = detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
   
    

    if len(lmList) != 0:
        #print(lmList[4][1],lmList[8][1]) #8ci ve 4-cu barmaqin pozisiyasi lazimdir bize
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2 #tam bolme eledik cunki circle da yalniz int type deyer qebul edir
        length=math.hypot(x2 - x1,y2 - y1)
        #print(length)
        
        #Hand Range 50 - 300 0 we need to change this
        #Volume Range -65 -0  to this

        vol = np.interp(length, [50, 300],[minVol, maxVol]) #the function use interpolation formula
        volForBar = np.interp(length, [50, 300],[400, 100]) 
        volForPer = np.interp(length, [50, 300],[0, 100]) 
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

    


        

        cv2.circle(img, (x1,y1) ,15 ,(255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2) ,15 ,(255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255,0,255), 3)
        cv2.circle(img, (cx,cy) ,15 ,(255,0,255), cv2.FILLED)
        
        
        if(length<50):
            cv2.circle(img, (cx,cy) ,15 ,(0,255,0), cv2.FILLED)
        
    cv2.rectangle(img,(50,100),(85,400),(255, 0, 0),3)
    cv2.rectangle(img,(50,int(volForBar)),(85,400),(255, 0, 0),cv2.FILLED)
    cv2.putText(img,f'Percentage: {int(volForPer)} % ',(40,450), cv2.FONT_HERSHEY_COMPLEX,1, (255, 0, 0),3)



    cTime = time.time()
    fps =1/(pTime-cTime)
    pTime=cTime
    cv2.putText(img,f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX,1, (255,0,0),3)


    
    cv2.imshow("Img", img)
    cv2.waitKey(1)
