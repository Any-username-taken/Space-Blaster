import pygame
import time
import random


class Sprite:
    def __init(self, img_src, angle, pos, type_, other=''):
        # Path, angle, [x, y]
        self.img_src = pygame.image.load(img_src)
        self.hitBox = self.img_src.get_rect()
        self.angle = angle
        self.pos = pos

        # Type is for the children of this class
        self.type = type_

        # Other is all other sprites in animation (if there is one)
        self.other = other

        self.current_img = self.img_src

        self.velX = 0
        self.velY = 0

    def update(self):
        self.pos[0] += self.velX
        self.pos[1] += self.velY

