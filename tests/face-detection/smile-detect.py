#!/usr/bin/env python
import cv
import time
import Image
#import SocketServer
import mosquitto
import threading

cv.NamedWindow("camera", 1)
capture = cv.CreateCameraCapture(0)

#font = cv.CvFont
font = cv.InitFont(1, 1, 1, 1, 1, 1)

width = None
height = None
width = 320
height = 240
smileness = 0
smilecount = 0

if width is None:
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    

if height is None:
    height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

result = cv.CreateImage((width,height),cv.IPL_DEPTH_8U,3) 

#mqtt functions
#mqttc = mosquitto.Mosquitto()
#mqttc.connect("127.0.0.1", 1883, 60)
#mqttc.subscribe("$SYS/#", 0)

mqLoop = 0

class mqThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mqttc = mosquitto.Mosquitto()
    #    mqttc.connect("127.0.0.1", 1883, 60)
    #    print "connected"
    def run(self):
        self.mqttc.connect("127.0.0.1", 1883, 60)
        print "connected"
        
        while True:
            self.mqttc.loop()
    def publish(self):
        self.mqttc.publish("smiles", "smile", 0)
            
mT = mqThread()
mT.start()
        

#HOST, PORT = "localhost", 9999
#print "Starting Server"
#server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
#server.serve_forever()



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
        
        print faces

        for ((x, y, w, h), n) in faces:
        # the input to cv.HaarDetectObjects was resized, so scale the
        # bounding box of each face and convert it to two CvPoints
            print "face"
            pt1 = (int(x * image_scale), int(y * image_scale))
            pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
            # print pt1
            # print pt2
            cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 1, 8, 0)
            cv.PutText(image, "face", pt1, font, cv.RGB(255, 0, 0))
            face_region = cv.GetSubRect(image,(x,int(y + (h/4)),w,int(h/2)))

            #split face
            cv.Rectangle(image, (pt1[0],(pt1[1] + (abs(pt1[1]-pt2[1]) / 2 ))), pt2, cv.RGB(0,255,0), 1, 8, 0)
            cv.PutText(image, "lower", (pt1[0],(pt1[1] + (abs(pt1[1]-pt2[1]) / 2 ))), font, cv.RGB(0, 255, 0))
            cv.SetImageROI(image, (pt1[0],
                               (pt1[1] + (abs(pt1[1]-pt2[1]) / 2 )),
                               pt2[0] - pt1[0],
                               int((pt2[1] - (pt1[1] + (abs(pt1[1]-pt2[1]) / 2 ))))))
            
            smiles = cv.HaarDetectObjects(image, smileCascade, cv.CreateMemStorage(0), 1.1, 5, 0, (15,15))
        
            if smiles:
                #print smiles
            
                for smile in smiles:
                    cv.Rectangle(image,
                    (smile[0][0],smile[0][1]),
                    (smile[0][0] + smile[0][2], smile[0][1] + smile[0][3]),
                    cv.RGB(0, 0, 255), 1, 8, 0)

                    cv.PutText(image, "smile", (smile[0][0],smile[0][1]), font, cv.RGB(0, 0, 255))

                    cv.PutText(image,str(smile[1]), (smile[0][0], smile[0][1] + smile[0][3]), font, cv.RGB(0, 0, 255))
                    #print ((abs(smile[0][1] - smile[0][2]) / abs(pt1[0] - pt2[0])) * 100) 
                    
                    global smileness 
                    smileness = smile[1]
            cv.ResetImageROI(image)
                    #if smile[1] > 90:
                    #    mqttc.publish("smiles", "got smile", 1)
                    #    time.sleep(5)
                    
        
        #eyes = cv.HaarDetectObjects(image, eyeCascade,
        #cv.CreateMemStorage(0),
        #haar_scale, min_neighbors,
        #haar_flags, (15,15))
            

        #if eyes:
            # For each eye found
            
            #print eyes
            
            #for eye in eyes:
                # Draw a rectangle around the eye
            #	cv.Rectangle(image,
            #	(eye[0][0],
            #	eye[0][1]),
            #	(eye[0][0] + eye[0][2],
            #	eye[0][1] + eye[0][3]),
            #	cv.RGB(255, 0, 0), 1, 8, 0)

    cv.ResetImageROI(image)
    return image

faceCascade = cv.Load("haarcascade_frontalface_alt.xml")
#eyeCascade = cv.Load("haarcascade_eye.xml")
#smileCascade = cv.Load("smileD/smiled_04.xml")
smileCascade = cv.Load("haarcascade_smile.xml")
#mqttc.loop()

while True:
    if smileness > 70:
        smilecount+= 1
    else:
        smilecount = 0
        
    if smilecount >=40:
        smilecount = 0
        #mqttc.publish("smiles", "smile", 0)
        mT.publish()
        time.sleep(5)
    
    if mqLoop >= 100:
        #mqttc.loop()
        mqLoop = 0
    else:
        mqLoop+= 1
    
    
    img = cv.QueryFrame(capture)
    
    smileness = 0
    image = DetectRedEyes(img, faceCascade, smileCascade)
    cv.ShowImage("camera", image)
    #print smileness
    
    k = cv.WaitKey(10);
    if k == 'f':
        break
