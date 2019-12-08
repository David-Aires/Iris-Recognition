import numpy as np
import cv2
from matplotlib import pyplot as plt

def features():
    img = cv2.imread('temp/polar.png')
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)     
    alg = cv2.AKAZE_create()
    (kp, desc) = alg.detectAndCompute(gray, None)
    return (kp, desc)
    




