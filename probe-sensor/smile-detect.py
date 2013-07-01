#!/usr/bin/env python
import cv
import time
import Image
#import mosquitto
import socket
import threading
import requests
import datetime
import json

cv.NamedWindow("camera", 1)
capture = cv.CreateCameraCapture(0)

width = int(320 * 1.5)
height = int(240 * 1.5)
#To Match MS Lifecam studio
#width = 640
#height = 360
smileness = 0
smilecount = 0

facecount = 0

smileList = []

smilecolor = cv.RGB(0, 255, 0)
lowercolor = cv.RGB(0, 0, 255)
facecolor = cv.RGB(255, 0, 0)
font = cv.InitFont(1, 1, 1, 1, 1, 1)
sFont = cv.InitFont(1, 0.7, 0.7, 1, 1, 1)

cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 
result = cv.CreateImage((width,height),cv.IPL_DEPTH_8U,3) 

class mqThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def run(self):
        print 'set up udp'


    def publishSmile(self):
        #self.mqttc.publish("smiles", "smile", 0)

        url = "http://127.0.0.1:8000/api/v1/smile/?api_key=cdf71d349bdc7b306211f4cb7bed2389931d7316&username=admin"

        data = {
            'probe': '/api/v1/probe/1/',
            'when': str(datetime.datetime.now())
        }
        headers = {'Content-type': 'application/json'}
        try:
            r = requests.post(url, data=json.dumps(data), headers=headers)
        except Exception as e:
            print e


    def publishFace(self):
        #self.mqttc.publish("faces", "face", 0)
        self.sock.sendto('face', (self.UDP_IP, self.UDP_PORT))
        global facecount
        facecount += 1

        if facecount > 40:
            facecount = 0

            url = "http://127.0.0.1:8000/api/v1/face/?api_key=cdf71d349bdc7b306211f4cb7bed2389931d7316&username=admin"
        
            data = {
                'probe': '/api/v1/probe/1/',
                'when': str(datetime.datetime.now())
            }
            headers = {'Content-type': 'application/json'}
            try:
                r = requests.post(url, data=json.dumps(data), headers=headers)
            except Exception as e:
                print e

            
mT = mqThread()
mT.start()
        



#openCV functions
def Load():

    return (faceCascade, smileCascade)

def Display(image):
    cv.NamedWindow("Smile Test")
    cv.ShowImage("Smile Test", image)
    cv.WaitKey(0)
    cv.DestroyWindow("Smile Test")

def DetectRedEyes(image, faceCascade, smileCascade):
    min_size = (20,20)
    image_scale = 2
    haar_scale = 1.2
    min_neighbors = 2
    haar_flags = 0
    
    global smileList

    # Allocate the temporary images
    gray = cv.CreateImage((image.width, image.height), 8, 1)
    smallImage = cv.CreateImage((cv.Round(image.width / image_scale),cv.Round (image.height / image_scale)), 8 ,1)

    # Convert color input image to grayscale
    cv.CvtColor(image, gray, cv.CV_BGR2GRAY)

    # Scale input image for faster processing
    cv.Resize(gray, smallImage, cv.CV_INTER_LINEAR)

    # Equalize the histogram
    cv.EqualizeHist(smallImage, smallImage)

    # Detect the faces
    faces = cv.HaarDetectObjects(smallImage, faceCascade, cv.CreateMemStorage(0),
    haar_scale, min_neighbors, haar_flags, min_size)

    # If faces are found
    if faces:
        
        #print faces

        for ((x, y, w, h), n) in faces:
        # the input to cv.HaarDetectObjects was resized, so scale the
        # bounding box of each face and convert it to two CvPoints
            #print "face"
            mT.publishFace()
            pt1 = (int(x * image_scale), int(y * image_scale))
            pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
            cv.Rectangle(image, pt1, pt2, facecolor, 1, 8, 0)
            cv.PutText(image, "face", pt1, font, facecolor)
            face_region = cv.GetSubRect(image,(x,int(y + (h/4)),w,int(h/2)))

            #split face
            cv.Rectangle(image, (pt1[0],(pt1[1] + (abs(pt1[1]-pt2[1]) / 2 ))), pt2, lowercolor, 1, 8, 0)
            cv.PutText(image, "lower", (pt1[0],(pt1[1] + (abs(pt1[1]-pt2[1]) / 2 ))), font, lowercolor)
            cv.SetImageROI(image, (pt1[0],
                               (pt1[1] + (abs(pt1[1]-pt2[1]) / 2 )),
                               pt2[0] - pt1[0],
                               int((pt2[1] - (pt1[1] + (abs(pt1[1]-pt2[1]) / 2 ))))))
            
            smiles = cv.HaarDetectObjects(image, smileCascade, cv.CreateMemStorage(0), 1.1, 5, 0, (15,15))
        
            if smiles:
                smileList.append(str(smiles)[0:25])
            
                for smile in smiles:
                    cv.Rectangle(image,
                    (smile[0][0],smile[0][1]),
                    (smile[0][0] + smile[0][2], smile[0][1] + smile[0][3]),
                    smilecolor, 1, 8, 0)

                    cv.PutText(image, "smile", (smile[0][0],smile[0][1]), font, smilecolor)

                    cv.PutText(image,str(smile[1]), (smile[0][0], smile[0][1] + smile[0][3]), font, smilecolor)
                    #print ((abs(smile[0][1] - smile[0][2]) / abs(pt1[0] - pt2[0])) * 100) 
                    
                    global smileness 
                    smileness = smile[1]
            cv.ResetImageROI(image)



    cv.ResetImageROI(image)
    
    
    if smileList.__len__() >= 10:
        smileList = smileList[-10:]
    #for smiles in smileList:
    #for idx, val in enumerate(smileList):
        #cv.PutText(image, val, (5,20 * idx), sFont, smilecolor)
        #print idx, val
        #print smiles
    return image

faceCascade = cv.Load("haarcascade_frontalface_alt.xml")
smileCascade = cv.Load("haarcascade_smile.xml")

while True:
    if smileness > 15:
        smilecount+= 1
    else:
        smilecount = 0
        
    if smilecount >=4:
        smilecount = 0
        mT.publishSmile()
        print "Got Smile!"
        smileList.append("Got Smile!")
        time.sleep(2)
    
    
    img = cv.QueryFrame(capture)
    
    smileness = 0
    image = DetectRedEyes(img, faceCascade, smileCascade)
    cv.ShowImage("camera", image)
    #print smileness
    
    k = cv.WaitKey(10);
    if k == 'f':
        break
