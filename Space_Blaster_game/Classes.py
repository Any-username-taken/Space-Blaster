import pygame
import time
import random


class Sprite:
    def __init(self, img_src, angle, pos, type_, other=''):
        # Path, angle, [x, y]
        self.img_src = img_src
        self.angle = angle
        self.pos = pos

        # Type is for the children of this class
        self.type = type_

        # Other is all other sprites in animation (if there is one)
        self.other = other

        self.current_img = self.img_src

    def draw(self):
        return self.current_img, self.angle, self.pos
