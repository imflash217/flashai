from __future__ import print_function
import numpy as np
import cv2

__author__ = "@imflash217"
__copyright__ = "@flashAI, 2019"

"""
Image utility module
"""

def translate(src: np.ndarray, x: int, y: int) -> np.ndarray:
    """Translation Affine Transform"""

    tfms_mat = np.float32([[1,0,x], [0,1,y]])
    return cv2.warpAffine(src=src, M=tfms_mat, (src.shape[1], src.shape[0]))


def rotate(src: np.ndarray, angle: int, scale:float, center: tuple(int, int)=None) -> np.ndarray:
    """Rotation Affine Transform"""

    if center == None:
        center = tuple(src.shape[1]//2, src.shape[0]//2)

    tfms_mat = cv2.getRotationMatrix2D(center=center, angle=angle, scale=scale)
    return cv2.warpAffine(src=src, M=tfms_mat, dsize=tuple(src.shape[1], src.shape[0]))
