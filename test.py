#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np


img1 = cv.imread("images/intro.png")
img2 = cv.imread("images/intro.jpg")

img1 = cv.resize(img1, [1000, 500])
cv.imshow("FirstWindow", img1)
# cv.imshow("FirstWindow", img2)
cv.waitKey(0)