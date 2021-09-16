#!/usr/bin/python
# -*- coding: utf-8 -*-
import screeninfo


Resolution = (1280, 720)
X_S, Y_S = Resolution[0], Resolution[1]
monitor_resolution = (screeninfo.get_monitors()[1].width, screeninfo.get_monitors()[1].height)
Res_center = (int(monitor_resolution[0]/2 - Resolution[0]/2), int(monitor_resolution[1]/2 - Resolution[1]/2))

DetectRectColor = (0, 0, 255)
detectionCon = 0.8
ColorRect = (255, 0, 255)