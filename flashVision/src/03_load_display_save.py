from __future__ import print_function
import argparse
import cv2

__author__ = "@imflash217"
__copyright__ = "@flashAI, 2019"

"""

"""

parser = argparse.ArgumentParser()                                              # ArgumentParser object
parser.add_argument("-i", "--image", required=True, help="Path to the image")   # adding a new argument that can be passed in BASH while executing this src code
args = vars(parser.parse_args())                                                # save the args in a dict

image = cv2.imread(args["image"])                                               # reading the image off the dict as a Numpy array
print(f'height   = {image.shape[0]}')
print(f'width    = {image.shape[1]}')
print(f'channels = {image.shape[2]}')

cv2.imshow("Image", image)                                                      # displaying the Numpy array image
cv2.waitKey(0)                                                                  # necessary to hold the display window, else the image window is displayed and closes

cv2.imwrite("../images/newimage.jpg", image)                                    # writes the image Numpy array as a new image-file (.jpg, .png etc)
