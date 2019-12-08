import cv2
import numpy as np



def getCircles(image):
    i = 80
    while(i<151):
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 2, 100.0,param1 = 30, param2= i, minRadius = 60, maxRadius = 110)
        if(len(circles) == 1):
            return circles
        i += 1
    return ([])

def getPupil(filename):
    global fg
    frame = cv2.imread(filename)
    iris = frame.copy()
    
    #Get pupil
    
    mask = np.full((iris.shape[0], iris.shape[1]), 0,np.uint8) 
    
    pupilImg = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint8)
    cv2.inRange(frame, (10,10,10), (80,80,80), pupilImg)
    contours, hierarchy = cv2.findContours(pupilImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    del pupilImg
    pupilImg = frame.copy()
    contourIdx = 0
    for c in contours:
        moments = cv2.moments(c)
        area = moments['m00']
        if (area > 50):
            pupilArea = area
            x = moments['m10']/area
            y = moments['m01']/area
            pupil = contours
            global centroid
            centroid = (int(x), int(y))
            cv2.drawContours(pupilImg, pupil, contourIdx ,color = (5,5,5), thickness =  1)
            rads = np.sqrt(4*pupilArea/np.pi)/2
            cv2.circle(mask,(int(x),int(y)),int(rads), (255, 255, 255), -1)
            break
        contourIdx += 1

    fg = cv2.bitwise_and(iris, iris, mask=mask)
    
    cv2.imwrite("temp/p.png",fg)
    return (pupilImg)


def isolate_pupil(filename):
    pupil = getPupil(filename)
    
    #Get iris
    iris = []
    copyImg = pupil.copy()
    resImg = pupil.copy()
    frame=pupil
    grayImg = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint8)
    mask = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint8)
    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, grayImg)
    cv2.Canny(grayImg, 5, 70, grayImg, 3)
    grayImg = cv2.GaussianBlur(grayImg,(7,7), 0, 0)
    circles = getCircles(grayImg)
    iris.append(resImg)
    
    for circle in circles:
        rad = int(circle[0][2])
        global radius
        radius = rad
        cv2.circle(mask, centroid, rad, (255,255,255), cv2.FILLED)
        cv2.circle(copyImg, centroid, rad, (0,0,0), 1)
        cv2.bitwise_not(mask, mask)
        cv2.subtract(frame,copyImg, resImg, mask)
        
        x = int(centroid[0] - rad)
        y = int(centroid[1] - rad)
        w = int(rad * 2)
        h = w
        roi = resImg[y:y+h , x:x+w]

        cv2.imwrite('temp/m.png', roi)

    


    #cv2.imshow("masked",fg)
    


    
    mask_ab = cv2.bitwise_xor(resImg,fg)
    cv2.imwrite("temp/final.png",mask_ab)

   

    
    
    cv2.waitKey(0)
    return centroid

  
	
  
