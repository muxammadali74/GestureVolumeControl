import math
import time

import cv2
import numpy as np
from comtypes import CLSCTX, CLSCTX_ALL
from kivy import level
from pycaw.api.audioclient import IAudioClient
from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.utils import AudioUtilities
from ctypes import cast, POINTER

from handDetector import handDetector

device = AudioUtilities.GetSpeakers()
interface = device.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_Range = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0,None)
minVol = vol_Range[0]
maxVol = vol_Range[1]
vol = 0

def main():
    pTime = 0
    cTime = 0
    volBar = 400
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        ret ,frame = cap.read()
        img = detector.findHands(frame)
        lmlist =detector.findPosition(img, draw=False)
        if len(lmlist) !=0:
            x1,y1 = lmlist[4][1], lmlist[4][2]
            x2,y2 = lmlist[8][1], lmlist[8][2]

            cx,cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1,y1), 15,(255,0,255), -1)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), -1)
            cv2.line(img, (x1,y1), (x2,y2),(255,0,255) ,3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), -1)

            lengh = math.hypot(x2-x1,y2-y1)


            vol = np.interp(lengh, [50,300], [minVol,maxVol])
            volBar = np.interp(lengh,[50,300], [400,150])
            volume.SetMasterVolumeLevel(vol, None)

            if lengh < 50:
                cv2.circle(img, (cx,cy), 15, (0, 255, 0), -1)

        cv2.rectangle(img, (50,150), (85,400), (0, 255, 0 ), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), -1)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)  # ФреймРейт

        cv2.imshow('python', img)
        if cv2.waitKey(20) == 27:  # exit on ESC
            break

    cap.release()


if __name__ == "__main__":
    main()

