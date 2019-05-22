from __future__ import print_function
import argparse
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

(b, g, r) = image[0, 0]                                     # cv2 stores color channels in BGR format not RGB
print(f'Pixel at [0, 0]: Red={r}, Green={g}, Blue={b}')

image[0, 0] = (0, 0 255)                                    # cv2 stores color channels in BGR format not RGB, so (0, 0, 255) == {B=0, G=0, R=255}
(b, g, r) = image[0, 0]
print(f'Updated pixel at [0, 0]: Red={r}, Green={g, Blue={b}')

corner = image[0:100, 0:100]
cv2.imshow("Corner", corner)

image[0:100, 0:100] = (0, 255, 0)                           # (B, G, R)
cv2.imshow("Modified", image)

cv2.waitKey(0)
