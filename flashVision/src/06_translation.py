
from __future__ import print_function
import argparse
import imutils
import numpy as np
import cv2

__author__ = "@imflash217"
__copyright__ = "@flashAI, 2019"

"""

"""

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True, help="path to the image")
args = vars(parser.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)
cv2.waitKey(0)

# translation module: manual
tfmsMatrix = np.float32([[1,0,50], [0,1,80]])
shiftedImage = cv2.warpAffine(src=image, M=tfmsMatrix, dsize=(image.shape[1], image.shape[0]))
cv2.imshow(winname="Shifted Down+Right", mat=shiftedImage)
cv2.waitKey(0)

# translation module: using imutils
shiftedImage = imutils.translate(src=image, x=10, y=-90)
cv2.imshow(winname="Shifted Up+Right", mat=shiftedImage)
cv2.waitKey(0)
