import pygame
import time
import random
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, img_src, anim_srcs, pos, type_, mSpeed, fireRate, damage, bull_lifetime, bull_speed, controllable, screen_par, scale=0.4):
        super().__init__()

        self.scale = scale

        self.image = pygame.transform.rotozoom(pygame.image.load(img_src), 0, self.scale)
        self.current_image = self.image
        self.holder_image = self.image

        self.anim = anim_srcs
        self.anim_speed = 0.5

        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.velX = 0
        self.velY = 0
        self.angle = 0

        self.hitBox = self.image.get_rect(center=self.pos)
        self.imOutline = self.hitBox.copy()

        self.type = type_

        self.mSpeed = mSpeed

        self.fireRate = fireRate
        self.coolDown = 0
        self.damage = damage
        self.bull_life = bull_lifetime
        self.bull_speed = bull_speed

        self.keys = [False, False, False, False]  # [W, A, S, D]
        self.mouse = [pygame.mouse.get_pos(), False, [0, 0]]

        self.controllable = controllable

        self.screen_par = screen_par

    def refresh(self):
        self.user_input()
        self.rotation()
        self.change_vel()
        self.movement()
        fire_check = self.fire_control()
        self.cool()
        self.update_animation()

        if fire_check:
            return self.damage, self.bull_speed, self.bull_life, "1", "Sprites/Projectiles/costume1.svg"

    def rotation(self):
        if not self.controllable == False and not self.type == 2:
            self.mouse[0] = pygame.mouse.get_pos()

            self.mouse[2][0] = (self.mouse[0][0] - self.hitBox.centerx)
            self.mouse[2][1] = (self.mouse[0][1] - self.hitBox.centery)

            self.angle = math.degrees(math.atan2(self.mouse[2][1], self.mouse[2][0]))
            self.current_image = pygame.transform.rotate(self.holder_image, -self.angle)
            self.imOutline = self.current_image.get_rect(center=self.hitBox.center)

    def movement(self):
        if self.controllable:
            self.pos += pygame.math.Vector2(self.velX, self.velY)
            self.hitBox.center = self.pos
            self.imOutline.center = self.hitBox.center

        # Screen wrap top - bottom

        if self.pos[1] > self.screen_par[1] + self.image.get_height() / 2:
            self.pos[1] = -100

        if self.pos[1] < -100:
            self.pos[1] = self.screen_par[1] + self.image.get_height() / 2

        # Screen wrap left - right

        if self.pos[0] > self.screen_par[0] + self.image.get_width() / 2:
            self.pos[0] = -100

        if self.pos[0] < -100:
            self.pos[0] = self.screen_par[0] + self.image.get_width() / 2

        # Lower velocity if high

        if self.velX > 0:
            self.velX -= 0.125

        if self.velX < 0:
            self.velX += 0.125

        # for the y velocity now

        if self.velY > 0:
            self.velY -= 0.125

        if self.velY < 0:
            self.velY += 0.125

    def change_vel(self):
        if self.keys[0] and self.velY > -self.mSpeed:
            self.velY -= 0.5
        if self.keys[1] and self.velX > -self.mSpeed:
            self.velX -= 0.5
        if self.keys[2] and self.velY < self.mSpeed:
            self.velY += 0.5
        if self.keys[3] and self.velX < self.mSpeed:
            self.velX += 0.5

    def user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.keys[0] = True
        else:
            self.keys[0] = False

        if keys[pygame.K_a]:
            self.keys[1] = True
        else:
            self.keys[1] = False

        if keys[pygame.K_s]:
            self.keys[2] = True
        else:
            self.keys[2] = False

        if keys[pygame.K_d]:
            self.keys[3] = True
        else:
            self.keys[3] = False

        if pygame.mouse.get_pressed()[0]:
            self.mouse[1] = True
        else:
            self.mouse[1] = False

    def fire_control(self):
        if self.coolDown <= 0 and self.mouse[1]:
            # backfire = random.randint(1, 100)

            if self.fireRate > 0.8 and self.type == 1:
                self.fireRate -= 0.2

            self.pos[0] = self.pos[0] - (5 * math.cos(math.radians(self.angle)))
            self.pos[1] = self.pos[1] - (5 * math.sin(math.radians(self.angle)))

            self.coolDown = self.fireRate

            self.anim_speed = 0.5
            self.current_image = pygame.transform.rotozoom(pygame.image.load(self.anim[0]), -self.angle, self.scale)
            self.holder_image = pygame.transform.rotozoom(pygame.image.load(self.anim[0]), 0, self.scale)

            return True

    def cool(self):
        if self.coolDown > 0:
            self.coolDown -= 0.1

        if self.type == 1 and not self.mouse[1] and self.fireRate < 5:
            self.fireRate += 0.1

    def update_animation(self):
        if self.anim_speed > 0:
            self.anim_speed -= 0.1

        if self.anim_speed <= 0:
            self.holder_image = self.image
            self.current_image = pygame.transform.rotate(self.holder_image, -self.angle)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, img_src, speed, lifeTime, type_, damage, angle, pos):
        super().__init__()
        self.scale = 0.5
        self.image = pygame.transform.rotozoom(pygame.image.load(img_src), 0, self.scale)

        self.speed = speed

        self.life = lifeTime

        self.type = type_

        self.damage = damage

        self.angle = angle

        self.pos = pygame.math.Vector2(pos[0], pos[1])

        self.opacity = 300

        self.image = pygame.transform.rotate(self.image, -self.angle)

        self.pos[0] = self.pos[0] + (5 * math.cos(math.radians(self.angle)))
        self.pos[1] = self.pos[1] + (5 * math.sin(math.radians(self.angle)))

    def refresh(self):
        self.move()
        self.take_time()

    def move(self):
        self.pos[0] = self.pos[0] + (self.speed * math.cos(math.radians(self.angle)))
        self.pos[1] = self.pos[1] + (self.speed * math.sin(math.radians(self.angle)))

    def take_time(self):
        if self.life > 0:
            self.life -= 0.1
        else:
            self.opacity -= 10
