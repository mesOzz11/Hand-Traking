import cv2
import mediapipe as mp
import time
import math
import csv


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLMS,self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand  = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx , cy = int(lm.x*w) , int(lm.y*h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])

        return lmList

    def getAngle(self,a, b, c):
        ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
        return ang + 360 if ang < 0 else ang
        #if ang < 0:
        #    ang = ang + 360
        #    ang = ang * (math.pi / 180)
        #else:
        #    ang = ang * (math.pi / 180)
        #return ang







def main():
    pTime=0   #previous time
    cTime=0   #current time
    #finger=int(input("enter finger no:(0-4)"))
    finger=0   #finger number from 0-4
    cap=cv2.VideoCapture(0)
    detector= handDetector()
    fing=[]
    ct = 1

    while True:
        success, img = cap.read()
        img=detector.findHands(img)
        lmlist=detector.findPosition(img)
        if len(lmlist) != 0:
            #print(lmlist[0][1:])
            if (finger == 0):
                ind=1
                name="finger0.csv"
            elif (finger == 1):
                ind=5
                name="finger1.csv"
            elif (finger == 2):
                ind=9
                name="finger2.csv"
            elif (finger == 3):
                ind=13
                name = "finger3.csv"
            elif (finger == 4):
                ind = 17
                name = "finger4.csv"

            angle1 = detector.getAngle(lmlist[0][1:],lmlist[ind][1:],lmlist[ind+1][1:])
            angle2 = detector.getAngle(lmlist[ind][1:],lmlist[ind+1][1:],lmlist[ind+2][1:])
            angle3 = detector.getAngle(lmlist[ind+1][1:], lmlist[ind+2][1:], lmlist[ind+3][1:])

            fing.append(angle1)
            fing.append(angle2)
            fing.append(angle3)
            if (len(fing)<=2000*3):
                try:
                    with open(name, "a", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow((angle1, angle2, angle3))
                except:
                    print("terminated")
                finally:
                    f.close()

            print(str(ct)+" angle1= " + str(angle1) + " angle2= " + str(angle2) + " angle3= " + str(angle3))
            ct= ct+1
            #print(len(res))




        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_DUPLEX,2,(255,10,55),3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__=="__main__":
    main()