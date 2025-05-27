import pygame
import time
import random
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, img_src, anim_srcs, pos, type_, mSpeed, fireRate, damage, bull_lifetime, bull_speed, controllable, screen_par, scale=0.4, health=20, maxHealth=20, hit_box_scale=[20, 20]):
        super().__init__()

        self.scale = scale

        self.image = pygame.transform.rotozoom(pygame.image.load(img_src), 0, self.scale)
        self.current_image = self.image
        self.holder_image = self.image

        self.anim = anim_srcs
        self.anim_speed = 0.5

        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.velX = 13
        self.velY = 0
        self.angle = 0

        self.hitBox = self.image.get_rect(center=self.pos)
        self.imOutline = self.image.get_rect(center=self.pos)
        self.rect = self.hitBox.copy()

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

        self.health = health
        self.maxHealth = maxHealth

        self.i_frames = 0

        self.enter = True
        self.loop = 80

        self.level = 0
        self.max_lvl = 50
        self.xp = 0

    def add_xp(self, amount):
        if self.xp + amount > self.max_lvl:
            hold = (self.xp + amount) - self.max_lvl
            self.xp = 0
            self.level += 1
            self.max_lvl += 50
            self.add_xp(hold)
        elif self.xp + amount == self.max_lvl:
            self.xp = 0
            self.level += 1
            self.max_lvl += 50
        else:
            self.xp += amount

    def refresh(self):
        self.user_input()
        self.rotation()
        self.change_vel()
        self.movement()
        fire_check = self.fire_control()
        self.cool()
        self.update_animation()

        if fire_check:
            return self.damage, self.bull_speed, self.bull_life, "1", "Sprites/Projectiles/costume1.svg", "player"

    def rotation(self):
        if not self.controllable == False and not self.type == 2:
            self.mouse[0] = pygame.mouse.get_pos()

            self.mouse[2][0] = (self.mouse[0][0] - self.hitBox.centerx)
            self.mouse[2][1] = (self.mouse[0][1] - self.hitBox.centery)

            self.angle = math.degrees(math.atan2(self.mouse[2][1], self.mouse[2][0]))
            self.current_image = pygame.transform.rotate(self.holder_image, -self.angle)
            self.imOutline = self.current_image.get_rect(center=self.pos)

    def movement(self):
        if self.enter and self.loop > 0:
            self.velX -= 0.1
            self.loop -= 1
        elif self.enter:
            self.enter = False
            self.controllable = True
            self.velX = 0

        self.pos += pygame.math.Vector2(self.velX, self.velY)
        self.hitBox = self.image.get_rect(center=self.pos)
        self.imOutline.center = self.hitBox.center
        self.rect = self.hitBox.copy()

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
        if self.controllable:
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

        if self.i_frames > 0:
            self.i_frames -= 0.1

    def update_animation(self):
        if self.anim_speed > 0:
            self.anim_speed -= 0.1

        if self.anim_speed <= 0:
            self.holder_image = self.image
            self.current_image = pygame.transform.rotate(self.holder_image, -self.angle)

    def take_damage(self, receiving):
        if self.i_frames <= 0:
            self.health -= receiving


class Enemy(pygame.sprite.Sprite):
    def __init__(self, img_src, anim_srcs, pos, type_, mSpeed, fireRate, damage, bull_lifetime, bull_speed, controllable, screen_par, scale=0.4, health=20, maxHealth=20, angle=180, xp=3):
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
        self.angle = angle

        self.hitBox = self.image.get_rect(center=self.pos)
        self.imOutline = self.hitBox.copy()
        self.rect = self.hitBox.copy()

        self.type = type_

        self.mSpeed = -mSpeed

        self.fireRate = fireRate
        self.coolDown = fireRate
        self.damage = damage
        self.bull_life = bull_lifetime
        self.bull_speed = bull_speed

        self.rotation = controllable

        self.screen_par = screen_par

        self.health = health
        self.maxHealth = maxHealth

        self.enter = False
        self.turn = False
        self.target_pos = [0, 0]
        self.loop = 0

        self.player_pos = [[0, 0], [0, 0]]

        self.xp = xp

        if self.type == "1":
            self.velX -= 8

    def refresh(self):
        self.move()
        self.rotate()
        fire_check = self.fire_control()
        self.cool()
        self.update_animation()

        if fire_check:
            return self.damage, self.bull_speed, self.bull_life, "1", "Sprites/Projectiles/enemyBullet.svg", "enemy"

    def rotate(self):
        if self.rotation:
            self.player_pos[1][0] = (self.player_pos[0][0] - self.hitBox.centerx)
            self.player_pos[1][1] = (self.player_pos[0][1] - self.hitBox.centery)

            self.angle = math.degrees(math.atan2(self.player_pos[1][1], self.player_pos[1][0]))
            self.current_image = pygame.transform.rotate(self.holder_image, -self.angle)
            self.imOutline = self.current_image.get_rect(center=self.hitBox.center)
            self.rect = self.imOutline.copy()

    def move(self):
        self.pos += pygame.math.Vector2(self.velX, self.velY)
        self.hitBox.center = self.pos
        self.imOutline.center = self.hitBox.center
        self.rect = self.imOutline.copy()
        if self.type == "1":
            if not self.enter and self.velX < 0:
                self.velX += 0.1
            elif self.loop == 0 and not self.enter:
                self.enter = 1
                self.velX = 0
                self.loop = 80
            elif self.enter == 1 and self.loop > 0:
                self.loop -= 1
            elif self.enter == 1:
                self.enter = 2
                self.loop = 60
            elif self.enter == 2 and self.loop > 0:
                self.velX -= 0.1
                self.loop -= 1
            elif self.enter == 2:
                self.loop = 80
                self.enter = 3
            elif self.enter == 3 and self.loop > 0:
                self.loop -= 1
            elif self.enter == 3:
                self.enter = 4
                self.loop = 60
            elif self.enter == 4 and self.loop > 0:
                self.velX += 0.1
                self.loop -= 1
            elif self.enter == 4:
                self.enter = 5
                self.velX = 0
                self.loop = 160
            elif self.enter == 5 and self.loop > 0:
                self.loop -= 1
            elif self.enter == 5:
                self.enter = 6
                self.loop = 60
            elif self.enter == 6 and self.loop > 0:
                self.velX += 0.1
                self.loop -= 1
            elif self.enter == 6:
                self.enter = 7
                self.loop = 80
            elif self.enter == 7 and self.loop > 0:
                self.loop -= 1
            elif self.enter == 7:
                self.enter = 8
                self.loop = 60
            elif self.enter == 8 and self.loop > 0:
                self.velX -= 0.1
                self.loop -= 1
            elif self.enter == 8:
                self.enter = 1
                self.loop = 160

        if self.type == "2":
            self.rotation = False
            if self.pos[0] > -100:
                self.pos[0] += self.mSpeed
            else:
                self.pos[0] = 1280 + 100

    def fire_control(self):
        if self.coolDown <= 0:
            # backfire = random.randint(1, 100)

            self.coolDown = self.fireRate

            self.anim_speed = 0.5
            self.current_image = pygame.transform.rotozoom(pygame.image.load(self.anim[0]), -self.angle, self.scale)
            self.holder_image = pygame.transform.rotozoom(pygame.image.load(self.anim[0]), 0, self.scale)

            return True

    def cool(self):
        if self.coolDown > 0:
            self.coolDown -= 0.1

    def update_animation(self):
        if self.anim_speed > 0:
            self.anim_speed -= 0.1

        if self.anim_speed <= 0:
            self.holder_image = self.image
            self.current_image = pygame.transform.rotate(self.holder_image, -self.angle)

    def take_damage(self, amount):
        self.health -= amount


class Bullet(pygame.sprite.Sprite):
    def __init__(self, img_src, speed, lifeTime, type_, damage, angle, pos):
        super().__init__()
        self.scale = 0.5
        self.image = pygame.transform.rotozoom(pygame.image.load(img_src), 0, self.scale)
        self.holderImage = self.image.copy()

        self.speed = speed

        self.life = lifeTime

        self.type = type_

        self.damage = damage

        self.angle = angle

        self.pos = pygame.math.Vector2(pos[0], pos[1])

        self.rect_stationary = self.image.get_rect(center=self.pos)
        self.hurtBox = self.rect_stationary.copy()
        self.rect = self.rect_stationary.copy()

        self.opacity = 300

        self.pos[0] = self.pos[0] + (5 * math.cos(math.radians(self.angle)))
        self.pos[1] = self.pos[1] + (5 * math.sin(math.radians(self.angle)))

    def refresh(self):
        self.rotate()
        self.move()
        self.take_time()

    def move(self):
        self.pos[0] = self.pos[0] + (self.speed * math.cos(math.radians(self.angle)))
        self.pos[1] = self.pos[1] + (self.speed * math.sin(math.radians(self.angle)))
        self.rect_stationary.center = self.pos
        self.hurtBox = self.image.get_rect(center=self.rect_stationary.center)
        self.rect = self.hurtBox.copy()

    def rotate(self):
        self.image = pygame.transform.rotate(self.holderImage, -self.angle)
        self.hurtBox = self.image.get_rect(center=self.rect_stationary.center)
        self.rect = self.hurtBox.copy()

    def take_time(self):
        if self.life > 0:
            self.life -= 0.1
        else:
            self.opacity -= 10


class HealthBar:
    def __init__(self, health, max_health, screen, pos_x=10, pos_y=10, len_=700):
        self.image = pygame.transform.rotozoom(pygame.image.load("Sprites/Extras/0.svg"), 0, 1.5)
        self.health = health
        self.mx_health = max_health
        self.screen = screen
        self.pos_x, self.pos_y = pos_x, pos_y
        self.len = self.image.get_width()
        self.height = self.image.get_height()
        self.target_health = self.len
        self.health_change_speed = 0.5

        self.dmg_delay = 1

    def show_bar(self):
        shown = (self.health / self.mx_health) * self.len

        self.screen.blit(self.image, (self.pos_x, self.pos_y))

        # // Catchup Bar //
        if shown != self.target_health:
            if self.target_health > shown:
                if self.dmg_delay <= 0:
                    self.target_health -= self.health_change_speed
                else:
                    self.dmg_delay -= 0.1
                pygame.draw.rect(self.screen, (250, 0, 0), (self.pos_x, self.pos_y, self.target_health, self.height))
            else:
                self.target_health = shown
                self.dmg_delay = 1

        # // Inner Bar //
        pygame.draw.rect(self.screen, (0, 250, 0), (self.pos_x, self.pos_y, shown, self.height))

    def down(self):
        # This is just a test function to see if the healthBar actually works
        self.health -= 1

    def update(self):
        self.show_bar()


class Deaths:
    def __init__(self, type_, image, pos, damage=0):
        self.type = type_
        self.image = pygame.transform.rotozoom(pygame.image.load(image), 0, 1)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pos = pygame.math.Vector2(pos[0] - self.width / 4, pos[1] - self.height / 2)
        self.rect = self.image.get_rect(center=self.pos)
        self.opacity = 400
        self.damage = damage
        self.dealt = False

    def refresh(self):
        self.opacity -= 25


class PickUp:
    def __init__(self, angle, speed, position, type_, image, lifetime, value):
        self.pick_up_range = 900

        if 0.3 + (value/10) < 1:
            self.scale = 0.3 + (value/10)
        else:
            self.scale = 1

        self.enter = speed

        self.image = pygame.transform.rotozoom(pygame.image.load(image), angle, self.scale)
        self.holder_image = self.image.copy()

        self.pos = pygame.math.Vector2(position[0], position[1])

        self.rect = self.image.get_rect(center=self.pos)
        self.hitBox = self.rect.copy()

        self.angle = angle

        self.player_pos = [[0, 0], [0, 0]]

        self.type = type_

        self.speed = speed

        self.lifetime = lifetime

        self.opacity = 300

        self.value = value

        self.distance = 100

        self.take = 0

    def refresh(self):
        self.rotate()
        self.move()
        self.take_life()

    def rotate(self):
        if self.enter > 0:
            self.image = pygame.transform.rotozoom(self.holder_image, -self.angle, self.scale)
            self.enter -= 0.1
            self.speed -= 0.1
            if self.enter <= 0:
                self.speed = 0
        elif self.distance < self.pick_up_range:
            self.player_pos[1][0] = (self.player_pos[0][0] - self.hitBox.centerx)
            self.player_pos[1][1] = (self.player_pos[0][1] - self.hitBox.centery)

            self.angle = math.degrees(math.atan2(self.player_pos[1][1], self.player_pos[1][0]))
            self.image = pygame.transform.rotozoom(self.holder_image, -self.angle, self.scale)
            self.hitBox.center = self.pos
            self.rect = self.image.get_rect(center=self.hitBox.center)

    def move(self):
        if self.distance < self.pick_up_range and self.enter <= 0:
            if self.speed < 20:
                self.speed += 0.2
        self.pos[0] = self.pos[0] + (self.speed * math.cos(math.radians(self.angle)))
        self.pos[1] = self.pos[1] + (self.speed * math.sin(math.radians(self.angle)))
        self.rect.center = self.pos
        self.hitBox = self.rect.copy()

        # Screen wrap top - bottom

        if self.pos[1] > 720:
            self.pos[1] = 0

        if self.pos[1] < -1:
            self.pos[1] = 720

        # Screen wrap left - right

        if self.pos[0] > 1280:
            self.pos[0] = 0

        if self.pos[0] < -1:
            self.pos[0] = 1280

    def take_life(self):
        if self.speed > 0 >= self.enter:
            self.speed -= 0.05

        if self.lifetime > 0 >= self.enter:
            self.lifetime -= 0.1
        elif self.lifetime <= 0:
            self.opacity -= 10
            self.scale += 0.1
            self.image = pygame.transform.rotozoom(self.holder_image, -self.angle, self.scale)
            self.hitBox.center = self.pos
            self.rect = self.image.get_rect(center=self.hitBox.center)

    def set_player_position(self, position):
        self.player_pos[0] = position
