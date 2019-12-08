import numpy as np
import cv2

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result


def polar2linear(center):
	image = cv2.imread('temp/final.png')
	image_polar = cv2.logPolar(image,(center[0],center[1]),50,cv2.INTER_LINEAR+cv2.WARP_FILL_OUTLIERS)
	image_polar_rotate = rotateImage(image_polar,90)
	cv2.imwrite("temp/polar.png",image_polar_rotate)
	cv2.waitKey(0)

	
