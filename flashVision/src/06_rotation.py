from __future__ import print_function
import argparse
import numpy as np
import cv2
import imutils

__author__ = "@imflash217"
__copyright__ = "@flashAI, 2019"

"""

"""
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="path to the image")
args = vars(parser.parse_args())

image = cv2.imread(srga["image"])
cv2.imshow(winname="Original", mat=image)


# rotation module: manual
(height, width) = image.shape[:2]
rot_center = (width//2, height//2)                              # cv2 interprets coordinates as (x, y) i.e. (width, height)
rot_angle = 45
scale = 1
tfms_mat = cv2.getRotationMatrix2D(center=rot_center, angle=rot_angle, scale=scale)
rotated_image = cv2.warpAffine(src=image, M=tfms_mat, dsize=(width, height))
cv2.imshow(winname=f'Rotated by {rot_angle} @{tuple(rot_center)}', mat=rotated_image)
cv2.waitkey(0)

rot_center = (width//3, height//4)
rot_angle = -75
scale = 1.5
tfms_mat = cv2.getRotationMatrix2D(center=rot_center, angle=rot_angle, scale=scale)
rotated_image = cv2.warpAffine(src=image, M=tfms_mat, dsize=(width, height))
cv2.imshow(winname=f'Rotated by {rot_angle} @{tuple(rot_center)}', mat=rotated_image)
cv2.waitKey(0)

# rotation module: using imutils
rot_center = (np.random.randint(width), np.random.randint(height))
rot_angle = np.random.randint(-180, 180)
scale = 1.6
rotated_image = imutils.rotate(src=image, angle=rot_angle, scale=scale, center=rot_center)
cv2.imshow(winname=f"Rotated by {rot_angle} @{tuple(rot_center)}", mat=rotated_image)
cv2.waitKey(0)










