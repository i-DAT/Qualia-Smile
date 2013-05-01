#!/usr/bin/env python
import cv
import time
import Image
import mosquitto
import threading

cv.NamedWindow("camera", 1)
capture = cv.CreateCameraCapture(1)

width = 320
height = 240
smileness = 0
smilecount = 0

smilecolor = cv.RGB(0, 255, 0)
lowercolor = cv.RGB(0, 0, 255)
facecolor = cv.RGB(255, 0, 0)
font = cv.InitFont(1, 1, 1, 1, 1, 1)

cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 
result = cv.CreateImage((width,height),cv.IPL_DEPTH_8U,3) 

class mqThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mqttc = mosquitto.Mosquitto()
    def run(self):
        self.mqttc.connect("127.0.0.1", 1883, 60)
        print "connected"
        
        while True:
            self.mqttc.loop()
    def publish(self):
        self.mqttc.publish("smiles", "smile", 0)
            
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
                print smiles
            
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
    return image

faceCascade = cv.Load("haarcascade_frontalface_alt.xml")
smileCascade = cv.Load("haarcascade_smile.xml")

while True:
    if smileness > 70:
        smilecount+= 1
    else:
        smilecount = 0
        
    if smilecount >=40:
        smilecount = 0
        mT.publish()
        print "Got Smile!"
        time.sleep(5)
    
    
    img = cv.QueryFrame(capture)
    
    smileness = 0
    image = DetectRedEyes(img, faceCascade, smileCascade)
    cv.ShowImage("camera", image)
    #print smileness
    
    k = cv.WaitKey(10);
    if k == 'f':
        break
