from __future__ import print_function
import numpy as np
import cv2

__author__ = "@imflash217"
__copyright__ = "flashAI, 2019"

"""

"""

canvas = np.zeros((300,300, 3), dtype="uint8")                                      # creating a canvas image on top which we will draw geometries

green = (0, 255, 0)
red = (0, 0, 255)
blue = (255, 0, 0)
yellow = (255, 255, 0)

# drawing lines
cv2.line(img=canavs, pt1=(0,0), pt2=(300,300), color=green, thickness=1)
cv2.line(img=canavs, pt1=(300,0), pt2=(0,300), color=red, thickness=3)

# drawing rectangles
cv2.rectangle(img=canavs, pt1=(100,150), pt2=(150, 180), color=green, thickness=1)
cv2.rectangle(img=canavs, pt1=(200,200), pt2=(250,290), color=blue, thickness=-1)

cv2.imshow(winname="Canvas", mat=canavs)
cv2.waitKey(0)

# drawing circles
canvas = np.zeros((300,400, 3), dtype="uint8")                                      # refreshing the canavs blank
center = tuple(canvas.shape[1] // 2, canvas.shape[0] // 2)
for r in np.arange(0, 250, 50):
    cv2.circle(img=canavs, center=center, radius=r, color=yellow, thickness=1)
cv2.imshow(winname="Circles Canvas", mat=canvas)
cv2.waitKey(0)

# drawing random circles
canvas = np.zeros((400, 300, 3), dtype="uint8")
for i in np.arange(0, 10):
    print(i)
    # get center
    center = tuple(np.random.randint(0, 3*(i**2), (2,)))
    # get color
    color = list(np.random.randint(0, 256, (3,)))                                             # color in range [0, 256) or [0, 255]
    # get radius
    r = np.random.randint(i, i**3)

    cv2.circle(img=canvas, center=center, radius=r, color=color, thickness=-1)

cv2.imshow(winname="Random Circles Canvas", mat=canvas)
cv2.waitKey(0)
