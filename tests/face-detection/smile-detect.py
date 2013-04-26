import cv
import time
import Image

cv.NamedWindow("camera", 1)
capture = cv.CreateCameraCapture(0)

#font = cv.CvFont
font = cv.InitFont(1, 1, 1, 1, 1, 1)

width = None
height = None
width = 320
height = 240

if width is None:
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    

if height is None:
    height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

result = cv.CreateImage((width,height),cv.IPL_DEPTH_8U,3) 

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
            pt1 = (int(x * image_scale), int(y * image_scale))
            pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
            print pt1
            print pt2
            cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 1, 8, 0)
            cv.PutText(image, "face", pt1, font, cv.RGB(255, 0, 0))
            face_region = cv.GetSubRect(image,(x,int(y + (h/4)),w,int(h/2)))

        #split face
        cv.Rectangle(image, (pt1[0],(pt1[1] + (abs(pt1[1]-pt2[1]) / 2 ))), pt2, cv.RGB(0,255,0), 1, 8, 0)
        cv.SetImageROI(image, (pt1[0],
                               (pt1[1] + (abs(pt1[1]-pt2[1]) / 2 )),
                               pt2[0] - pt1[0],
                               int((pt2[1] - (pt1[1] + (abs(pt1[1]-pt2[1]) / 2 ))))))
            
        smiles = cv.HaarDetectObjects(image, smileCascade, cv.CreateMemStorage(0), 1.1, 5, 0, (15,15))
        
        if smiles:
            #print smiles
            
            for smile in smiles:
                cv.Rectangle(image,
                (smile[0][0],
                smile[0][1]),
                (smile[0][0] + smile[0][2],
                smile[0][1] + smile[0][3]),
                cv.RGB(255, 0, 0), 1, 8, 0)
        
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
while True:
    img = cv.QueryFrame(capture)

    image = DetectRedEyes(img, faceCascade, smileCascade)
    cv.ShowImage("camera", image)
    k = cv.WaitKey(10);
    if k == 'f':
        break
