from flask import Flask, render_template, url_for, request

app = Flask(__name__)

 

@app.route('/')
@app.route('/home')



def home():
    return render_template("index.html")



@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    print("Nandiiiiiiii")


    import cvzone
    import numpy as np
    import cv2
    #import mediapipe
    import math
    import random
    from cvzone.HandTrackingModule import HandDetector

    cap=cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

    detector=HandDetector(detectionCon=0.8,maxHands=1)

    class Snake:
        def __init__(self,pathFood):
            self.points=[]
            self.length=[]
            self.currentLen=0
            self.allowedLen=150
            self.previousHead=0,0

            self.imgFood=cv2.imread(pathFood,cv2.IMREAD_UNCHANGED)
            self.hfood,self.wfood,_=self.imgFood.shape
            self.foodPoint=0,0
            self.score=0
            self.gameOver=False
            self.ranFood()

        def ranFood(self):
            self.foodPoint=random.randint(100,1000),random.randint(100,600)

        def update(self,imgMain,currentHead):
            if self.gameOver:
                cvzone.putTextRect(imgMain,"Game Over",(300,400),scale=7,thickness=5,offset=20)
                cvzone.putTextRect(imgMain,f"Your Score:{self.score}",(300,550),scale=7,thickness=5,offset=20)
            else:
                px,py=self.previousHead
                cx,cy=currentHead

                self.points.append([cx,cy])
                distance=math.hypot(cx-px,cy-py)
                self.length.append(distance)
                self.currentLen+=distance
                self.previousHead=cx,cy

                #lenth rduction
                if self.currentLen>self.allowedLen:
                    for i,length in enumerate(self.length):
                        self.currentLen-=length
                        self.length.pop(i)
                        self.points.pop(i)

                        if self.currentLen<self.allowedLen:
                            break
                #snake eating food
                rx,ry=self.foodPoint
                if rx - self.wfood //2 <cx< rx + self.wfood //2 and ry-self.hfood //2  <cy< ry+self.hfood //2:
                    self.ranFood()
                    self.allowedLen+=50
                    self.score+=1
                    print(self.score)

                


                #drowing snake
                if self.points:
                    for i,point in enumerate(self.points):
                        if i!=0:
                            cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),20)
                    cv2.circle(imgMain,self.points[-1],17,(200,0,200),cv2.FILLED)

                #draw food
                #rx,ry=self.foodPoint
                imgMain=cvzone.overlayPNG(imgMain,self.imgFood,(rx - self.wfood// 2, ry - self.hfood//2)) #freaking out!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                #score
                cvzone.putTextRect(imgMain,f" Score ={self.score}",(50,80),scale=3,thickness=3,offset=10)



                #Collision
                pts=np.array(self.points[:-2],np.int32)
                pts=pts.reshape((-1,1,2))
                cv2.polylines(imgMain,[pts],False,(0,200,0),3)
                min_dist=cv2.pointPolygonTest(pts,(cx,cy),True)
                #print(min_dist)
                if -1<= min_dist<=1:
                    print("Game Over")
                    self.gameOver=True
                    self.points=[]
                    self.length=[]
                    self.currentLen=0
                    self.allowedLen=150
                    self.previousHead=0,0
                    self.ranFood()

            return imgMain

    game=Snake('donut.png')

    while True:

        succuess,img=cap.read()
        img=cv2.flip(img,1)
        hands,img=detector.findHands(img,flipType=False)

        if hands:
            lmList=hands[0]['lmList']
            pointIndex=lmList[8][0:2]
            img=game.update(img, pointIndex)
            #length,info,img = detector.findDistance(lmList[12][:2], lmList[10][:2],img) ##########3
            #print(lmList[8][2],lmList[6][2])
            if lmList[8][2]>lmList[6][2]:
                print("two fng")
            ##length= detector.findDistance(lmList[8], lmList[12])
        
        
        cv2.imshow("SNAKE GAME",img)
        if cv2.waitKey(1)==27:
            cv2.destroyAllWindows()
            cap.release()
        key=cv2.waitKey(1)
    ################################################################33
        #length,fuck, img = detector.findDistance(lmList[8], lmList[8], img)
        
    ##############################################################################
        if key == ord('r'):
            game.gameOver=False
            game.score=0


        '''thresh = (lst.landmark[9].y*100 - lst.landmark[12].y*100)/2

        if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:
            cnt += 1

        detector.'''

   


    name = output["name"]


    return render_template('index.html', name = name)


if __name__ == "__main__":
    app.run(debug=True)