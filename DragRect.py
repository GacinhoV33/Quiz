#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from settings import Resolution


class DragFigure:

    def __init__(self, posCenter=None, size=[130, 130]):
        self.size = size
        if posCenter:
            self.posCenter = posCenter
        else:
            self.posCenter = self.get_random_pos(self.size[0], self.size[1])

    def update(self, cursor):
        centerx, centery = self.posCenter
        w, h = self.size
        if centerx - w//2 < cursor[0] < centerx + w//2 and centery - h//2 < cursor[1] < centery + h//2:
            self.posCenter = cursor
        return True

    @classmethod
    def get_random_pos(cls, minx: int, miny: int):
        return [random.randint(int(minx//2+1), int(Resolution[0] - minx//2 - 1)), random.randint(int(miny//2+1),
                                            int(Resolution[1] - miny//2 - 1))]
