from __future__ import print_function
import argparse
import numpy as np
import cv2
import imutils

__author__ = "@imflash217"
__copyright__ = "@flashAI, 2019"

"""
NOTE: in cv2, (x, y) == (width, height)
"""

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True, help="path to the image")
args = vars(parser.parse_args())

img = cv2.imread(args["image"])
(width, height) = (img.shape[1], img.shape[0])

cv2.imshow(winname="Original", mat=img)
cv2.waitKey(0)

# Resize module: manual
new_width = 100
new_dim = (new_width, new_width*height/width)
resized_img = cv2.resize(src=img, dsize=new_dim, interpolation=cv2.INTERP_AREA)
cv2.imshow(winname=f"Resized image with new width={new_width}", mat=resized_img)
cv2.waitKey(0)

new_height = 85
new_dim = (new_height*width/height, new_height)
resized_img = cv2.resize(src=img, dsize=new_dim, interpolation=cv2.INTERP_AREA)
cv2.imshow(winname=f"Resized image with new height={new_height}", mat=resized_img)
cv2.waitKey(0)

new_ratio = 0.17
new_dim = (width*new_ratio, height*new_ratio)
resized_img = cv2.resize(src=img, dsize=new_dim, interpolation=cv2.INTERP_AREA)
cv2.imshow(winname="Resized image by {new_ratio}\%", mat=resized_img)
cv2.waitKey(0)






