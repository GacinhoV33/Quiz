#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np
from settings import detectionCon
from cvzone.HandTrackingModule import HandDetector
from DragRect import DragFigure


def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background


Detector = HandDetector(detectionCon=detectionCon, maxHands=2)

# Rect_list = list()
Circle_list = list()
#
# for i in range(5):
#     Rect_list.append(DragFigure())

Rect_list = [DragFigure([50, 130], [100, 200])]
Circle_list.append(DragFigure([250, 250], [80, 80]))
Circle_list.append(DragFigure([500, 250], [80, 80]))
BallImage = cv.imread('images/ball2.png', cv.IMREAD_UNCHANGED)
# BallImage = cv.imread('images/ball.png')
print(BallImage.shape)
Elipse = DragFigure([450, 500], [75, 75])
BallRect = DragFigure([320, 320], [320, 320])