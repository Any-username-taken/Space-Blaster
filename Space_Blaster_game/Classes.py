import pygame
import time
import random
import math


class PlayerV3(pygame.sprite.Sprite):
    # Sadly, the third time I'm rewriting this class
    def __init__(self, screen, anim_dict, pos, angle, type_, size, health, max_health, speed, damage, bullet_stats, kb_strength, accuracy, scale, fireRate, velXY, hit_box_dimensions):
        super().__init__()

        self.screen = screen
        # Screen imported to the class

        self.anim_dict = anim_dict
        # Information split like so:
        # {"Sprites/Player/Path/...": [[OffsetX, OffsetY], anim_style, anim_type, time until next],
        # "Sprites/Player/Path/...2": [[OffsetX, OffsetY], anim_style, anim_type, time until next]}
        # anim_style is in case of multiple parts rendered at once
        # anim_type - Idle, Attack, Permanent, Never rendered | Either for multiple parts or single sprite
        self.anim_index = 0

        self.scale = scale

        self.angle = angle

        self.current_img = pygame.transform.rotozoom(pygame.image.load(list(self.anim_dict.keys())[0]), self.angle, self.scale)

        self.current_offset = self.anim_dict[list(self.anim_dict.keys())[0]][0]  # offset of 1st img in dict

        self.time_till_next = 0

        self.pos = pygame.math.Vector2(pos[0], pos[1])

        self.type = type_

        self.size = size

        self.health = health

        self.max_health = max_health

        self.speed = speed

        self.damage = damage

        self.bullet_stats = bullet_stats
        # Includes:
        # speed | lifetime | bullet type - Includes: normal, lazer, mine, drone, etc.

        self.kb = kb_strength

        self.accuracy = accuracy

        self.fireRate = fireRate

        self.vel_x, self.vel_y = velXY

        self.hit_box_dimensions = hit_box_dimensions
        # Making hit box distant based seems better due to only needing distance calculations instead of
        # rotating hit box, meaning the 4th index is radius

        self.rect = pygame.rect.Rect(self.hit_box_dimensions[0], self.hit_box_dimensions[1], self.hit_box_dimensions[2], self.hit_box_dimensions[3])
        # Normal rect needed for bliting to screen and rotation from pivot point

        self.keys = [False, False, False, False]  # [W, A, S, D]
        self.control = [False, False]
        self.charge = 0
        self.start = False
        self.loop = 0
        self.mouse = [pygame.mouse.get_pos(), False, [0, 0]]

        self.i_frames = 0

        self.level = 0
        self.xp = 0
        self.xp_next = 50

        self.upgrades = []

        self.brightness = 0
        self.opacity = 300

    def refresh(self):
        pass

    # def turn(self): - Come back to this one when anim is finished
        # rotated_img = pygame.transform.rotozoom(self.current_img, -self.angle, self.scale)
        # rotated_offset = self.current_offset.rotate(self.angle)
        # self.current_image = rotated_img
        # self.rect.center = self.pos
        # self.imOutline = rotated_img.get_rect(center=self.pos + rotated_offset)

    def point_mouse(self):
        if self.control[1]:  # checks if player is allowed to rotate
            self.mouse[0] = pygame.mouse.get_pos()

            self.mouse[2][0] = (self.mouse[0][0] - self.pos[0])
            self.mouse[2][1] = (self.mouse[0][1] - self.pos[1])

            self.angle = math.degrees(math.atan2(self.mouse[2][1], self.mouse[2][0]))

    def movement(self):
        window_dimensions = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.pos[0] += self.vel_x
        self.pos[1] += self.vel_y

    def add_xp(self, amount):
        self.xp += amount

        if self.xp >= self.xp_next:
            self.level += 1

            self.xp_next += self.xp_next


class PlayerV2(pygame.sprite.Sprite):
    def __init__(self, anim_dict, screen, pos=pygame.math.Vector2(0, 0), type_=1, size=50, health=50, max_health=50, speed=5, damage=3, bull_speed=4, bull_lifetime=20, kb=3, accuracy=100, scale=0.7, fireRate=4, vel_x=13):
        super().__init__()
        self.coolDown = 0
        self.anim = anim_dict  # suggested that it is a dictionary

        self.screen = screen  # gives the class access to the display (blits to the screen from inside the class,
        # reformat update function)

        self.type = type_  # type of ship = different abilities

        self.control = False  # disables movement and firing controls

        self.rotate = True  # disables mouse tracking controls

        self.i_frames = 0  # if invincibility upgrade/hit by beam-type projectile, prevents damage for a brief period

        self.maxHealth = max_health  # Max health can be reduced while health stays the same
        self.health = health  # Health can go into override, past max hp also can be set to half when reviving

        if self.type == 2:  # allows for rotation on start if ship type 2, mine layer
            self.rotate = True
        else:
            self.rotate = False

        self.scale = scale  # size of ship, can be smaller/larger with abilities/debuffs
        self.brightness = 0  # when the ship gets hit, it gets brighter
        self.angle = 0  # current angle the ship faces
        self.pos = pygame.math.Vector2(pos[0], pos[1])  # position of pivot point

        self.enter = True  # set to true when spawning for the first time
        self.loop = 80  # used for enter animation

        self.vel_X = vel_x  # current speed on the x-axis
        self.vel_Y = 0  # current speed on the y-axis

        self.mSpeed = speed  # maximum speed the player is allowed to travel

        # img and hit boxes
        # current img in animation
        self.current_image = pygame.transform.rotozoom(pygame.image.load(list(anim_dict.keys())[0]), 0, self.scale)
        self.image = self.current_image.copy()  # stationary image that never changes, for transformation and rotation

        try:
            self.current_offset = pygame.math.Vector2(*anim_dict[list(anim_dict.keys())[0]][2])  # two values containing
            # the offset for pivot
        except IndexError:
            self.current_offset = pygame.math.Vector2(0, 0)  # sets offset to center of image

        # hit box goes first
        self.rect_size = size
        self.rect = pygame.rect.Rect(size, size, size, size)  # hit box used for collisions
        self.imOutline = self.current_image.get_rect()  # rect for show, kinda useless
        self.imOutline.center = self.pos  # centering around pivot point

        self.keys = [False, False, False, False]  # [W, A, S, D]
        self.mouse = [pygame.mouse.get_pos(), False, [0, 0]]

        self.fireRate = fireRate  # time taken until player can shoot again, HOLD THE MOUSE BUTTON PLEASE FOR THE LOVE O
        self.damage = damage  # damage projectile inherits
        self.bull_speed = bull_speed  # Speed projectile travels
        self.bull_life = bull_lifetime  # How long the bullets last
        self.kb = kb  # How far the player is pushed back from shooting
        self.accuracy = accuracy  # How the bullet spreads
        self.charge = 0  # For charge ships

        self.level = 0  # used as currency for cards [NOT FINAL]
        self.xp = 0  # used as secondary currency for healing and basic upgrades [NOT FINAL]
        self.xp_limit = 50  # amount of xp needed until next level

        self.upgrades = []  # contains information for all upgrades [NOT FINAL]

        # Sets up important information for animations
        self.idle_index = 0
        for i in range(len(list(self.anim.keys()))):
            pass

    def add_xp(self, amount):
        if self.xp + amount > self.xp_limit:  # checks if xp plus amount is greater than xp limit
            left = (self.xp + amount) - self.xp_limit  # calculates left over xp after level-up
            # resets information and adds one to level
            self.xp = self.xp_limit
            self.xp_limit += 50
            self.level += 1

            self.add_xp(left)  # calls function again to check if another level up is possible/adds remaining xp
        elif self.xp + amount == self.xp_limit:  # checks if xp plus amount is equal to xp limit
            # resets information and adds one to level
            self.xp += amount
            self.xp_limit += 50
            self.level += 1
        else:  # adds to xp normally
            self.xp += amount

    def refresh(self):
        item = False
        self.point_mouse()
        self.turn()
        self.user_input()
        self.change_vel()
        self.movement()
        self.reduce_cooldown()
        if self.type == 1:
            item = self.spawn_bullet1()
        elif self.type == 4:
            item = self.spawn_bullet4()

        if item:
            hold_charge = self.charge
            self.charge = 0
            if self.type == 1:
                return (self.damage + hold_charge), self.bull_speed, self.bull_life, "1", "Sprites/Projectiles/costume1.svg", "player"
            elif self.type == 4:
                return (self.damage + hold_charge), self.bull_speed, self.bull_life, "1", "Sprites/Projectiles/costume1.svg", "pxpl"

    def turn(self):
        rotated_img = pygame.transform.rotozoom(self.image, -self.angle, self.scale)
        rotated_offset = self.current_offset.rotate(self.angle)
        self.current_image = rotated_img
        self.rect.center = self.pos
        self.imOutline = rotated_img.get_rect(center=self.pos + rotated_offset)

    def point_mouse(self):
        if self.rotate:
            self.mouse[0] = pygame.mouse.get_pos()

            self.mouse[2][0] = (self.mouse[0][0] - self.pos[0])
            self.mouse[2][1] = (self.mouse[0][1] - self.pos[1])

            self.angle = math.degrees(math.atan2(self.mouse[2][1], self.mouse[2][0]))
            self.turn()

    def movement(self):
        if self.enter and self.loop > 0:
            self.vel_X -= 0.1
            self.loop -= 1
        elif self.enter:
            self.enter = False
            self.control = True
            self.rotate = True
            self.vel_X = 0

        self.pos += pygame.math.Vector2(self.vel_X, self.vel_Y)

        # Screen wrap top - bottom

        if self.pos[1] > 720:
            self.pos[1] = -100

        if self.pos[1] < -100:
            self.pos[1] = 720

        # Screen wrap left - right

        if self.pos[0] > 1280:
            self.pos[0] = -100

        if self.pos[0] < -100:
            self.pos[0] = 1280

        # Lower velocity if high

        if self.vel_X > 0:
            self.vel_X -= 0.125

        if self.vel_X < 0:
            self.vel_X += 0.125

        # for the y velocity now

        if self.vel_Y > 0:
            self.vel_Y -= 0.125

        if self.vel_Y < 0:
            self.vel_Y += 0.125

    def change_vel(self):
        if self.control:
            if self.keys[0] and self.vel_Y > -self.mSpeed:
                self.vel_Y -= 0.5
            if self.keys[1] and self.vel_X > -self.mSpeed:
                self.vel_X -= 0.5
            if self.keys[2] and self.vel_Y < self.mSpeed:
                self.vel_Y += 0.5
            if self.keys[3] and self.vel_X < self.mSpeed:
                self.vel_X += 0.5

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

    def spawn_bullet1(self):
        if self.coolDown <= 0 and self.mouse[1]:
            # backfire = random.randint(1, 100)
            if self.fireRate > 0.8 and self.type == 1:
                self.fireRate -= 0.2

            if self.type == 1:
                self.pos[0] = self.pos[0] - (5 * math.cos(math.radians(self.angle)))
                self.pos[1] = self.pos[1] - (5 * math.sin(math.radians(self.angle)))
            else:
                # Invert to go backwards
                self.vel_X = -(self.kb * math.cos(math.radians(self.angle)))
                self.vel_Y = -(self.kb * math.sin(math.radians(self.angle)))

            self.coolDown = self.fireRate

            return True

    def spawn_bullet4(self):
        if self.coolDown <= 0 and self.mouse[1]:
            if self.charge <= 100:
                self.charge += 0.1

        elif not self.mouse[1] and self.charge > 0:
            self.vel_X = int(-(self.kb * math.cos(math.radians(self.angle))))
            self.vel_Y = int(-(self.kb * math.sin(math.radians(self.angle))))
            self.coolDown = self.fireRate
            return True

    def reduce_cooldown(self):
        if self.coolDown > 0:
            self.coolDown -= 0.1

        if self.type == 1 and not self.mouse[1] and self.fireRate < 5:
            self.fireRate += 0.1

        if self.i_frames > 0:
            self.i_frames -= 0.1

    def take_damage(self, amount, i=False):
        if i and self.i_frames > 0:
            pass
        else:
            if self.health - amount >= 0:
                self.health -= amount
            else:
                self.health = 0
            if i:
                self.i_frames = i

    def class_info(self):  # Information for me about this class (I can't remember anything after 5 hours)
        """
        -- Anim --
        Information for self.anim is split like so:
        {img1: (idle?, next anim speed, [offset x, offset y] | None (non-existent)), ...}

        if not [offset x, offset y], use default value of img center

        -- Upgrades --
            -- Costs --
            Upgrades will require a minimum level, AND a specific amount of xp, increasing each time the player buys the
            same upgrade, Example:
                        Level: 2
                        Xp: 76
                        _______________________  _______________________  _______________________
                        |  -Health upgrade I- |  | -Damage upgrade II- |  | -Speed upgrade III- |
                        |  __________________ |  |  __________________ |  | ___________________ |
                        | |                 | |  | |                 | |  | |                 | |
                        | |  Level req: 1   | |  | |  Level req: 3   | |  | |  Level req: 2   | |
                        | |   xp cost: 25   | |  | |   xp cost: 60   | |  | |  xp cost: 120   | |
                        | |                 | |  | |                 | |  | |                 | |
                        | |_________________| |  | |-----------------| |  | |_________________| |
                        |      Available      |  |       Locked        |  |       Locked        |
                        |_____________________|  |_____________________|  |_____________________|

                    -- If first upgrade chosen, subtracts 25 xp, but not any levels
                    -- If second or third chosen, nothing happens cause cant afford due to level or xp cost
            Some ships will have different level limits and nothing regarding xp and levels are final right now.
            -- Basics --
            H1 - Basic health upgrade increasing max hp by 5
            Sp1 - Basic speed upgrade increasing speed by 0.5 [NOT FINAL]
            F1 - Basic fire rate upgrade decreasing fire rate by 0.1
                NOTE: Cannot go below 0.5 unless ship type == 1 due to ability
                Ship type 1 also resets to 0.5 if maxed, not that it matters
            D1 - Basic damage upgrade increasing damage by 3
            -- Normals --
            H2 - Normal health upgrade increasing max hp by 10% [NOT FINAL]
            Sp2 - Adds dash ability allowing player to become [TITLE CARD] while dashing
                NOTE: First upgrade adds the dash with distance being 50, i frames lasting for 3f after dash
                Further upgrades increase distance up to 100, 10 per upgrade, while increasing i frames by 1f
                [NOT FINAL]
            F2 - Increases bullets shot
                NOTE: Beam-type ships can only get up to 4 beams because they are continuous
                Ship type 1 can only go up to 6 because of rapid fire rate
                Otherwise, limit is 10 bullets at once
                Increases kb by 5 [kb value NOT FINAL]
            KB1 - Decreases kb from shooting by 5
                NOTE: Cannot go negative... Useful for beam-type ships and fast firing ships or multi-shot upgrades
            D2 - Increases damage by 6 AND adds splash effect(?)
                NOTE: Splash damage [NOT FINAL] will have an initial radius of 20, increasing by 10 per upgrade
                No limit(?)
            IF1 - Adds an [TITLE CARD]ity ability granting player with 180 [TITLE CARD] frames
                NOTE: Use [enter key here] to activate for a brief period of taking no damage
                First upgrade deactivates weapons until [TITLE CARD]ity ends (SEA SALT) 5th upgrade allows player to use
                weapons while [TITLE CARD] All other abilities can be activated while [TITLE CARD] (WHERE IS OMNI-MAN)
            Dr1 - Basic drone upgrade adding a little companion [MHp: self.max_health/2, Dmg: self.damage/2]
                NOTE: If player damage is lower than 15, which will usually be beam-type ships, damage is set to 5 + any
                damage upgrades the player has, same goes for max Hp, Each upgrade increases health by 10% of player MHp
                and damage by 5, and fire rate by -0.1 (fire rate starts at 5, not affected by upgrades reducing fr)
                The drone is affected by damage mult upgrades, and multi-shot, If damage exceeds 15
                after drone upgrade acquired, if new damage is lower than existing damage, damage is not changed
                Drone shoots a burst of 3 bullets at the players mouse when firing
                Respawn time: 50s
                Max number of drones attainable: 3
            Dr2 - Contact drone flies around to a randomly assigned target until either side is dead [MHp: 100, Dmg: 0.5]
                NOTE: Since this is a contact-based drone, it does low damage due to damaging like a beam-type ship
                Not affected by damage upgrades (except dmg mult) or fire rate or multi-shot, but is affected by speed
                upgrades, If implementation successful, all other drones will be able to switch between auto or manual
                modes
                    Auto mode-
                    Randomly targets enemy until enemy dead or drone dead, modes switched with [enter key here]
                    Semi-manual mode-
                    Aims at mouse pointer, but shoots as soon as it can, modes switched with [enter key here]
                    Manual mode-
                    Aims at mouse pointer and only fires when player fires, modes switched with [enter key here]
                    Exceptions-
                    Contact drones, Flame drones, Charged drones, and Beam drones are all permanently set to Auto mode
                    due to how they operate
            -- Advanced --
            H3 - Increases max health by 10, and adds regen ability (0.1% health per second)
                NOTE: increases by 0.4% until 5% | Variant of this upgrade makes 0.1% of health recover per xp pick up
                Increases by 0.1% per upgrade until 5%
            Dou1 - Doubles the effect of all applicable upgrades
                NOTE: This does not affect ship evolution cards, Ignores card limit, Applied first, Can only obtain once
            -- Class Cards --
                Description - Class specific cards that only are obtainable through certain types of ships
            Ship 1 - [Fire rate increases the longer the shoot button is held down]
                Fire Speed - Decreases the time it takes to get to minimum fire speed
                Super Armor - Decreases all damage by 90% for 20s [NOT FINAL]
                    NOTE: Each upgrade will decrease the time until ability can be used again and increase the time the
                    ability lasts by 0.5s until 30s
            Ship 2 - [Shoots mines with space bar]
                Bigger Mines - Mines have more range and a larger explosion radius (up to 5x)
                Recover time - Decreases time to wait for mine to reload
                Life time - Increases mine lifetime to stay on the field for longer (10% time increase per upgrade)
                Extra Mine - Adds 1 more mine (obtainable only once) [NOT FINAL]
            Ship 3 - [Starts off shooting 2 bullets, No spray (no random angle the bullets follow)]
                Extra Bullets - Adds two more bullets
                    NOTE: This might replace the F2 upgrade entirely, only allowing you to obtain it through specific
                    ships
                Rage Mode - Increases damage by 75% and increases damage taken by 50%
                    NOTE: Triggered by [enter key here] | Triggered by taking damage [NOT FINAL]
                    All upgrades decrease damage taken by 5% and increase damage dealt by 3% AND increases time in rage
                    by 10% AND decreases time until ability can be used again by 5% [NOT FINAL]
            Ship 4 - [Charged shot, does damage proportional to the time the shoot button has been held]
                Charge time - Decreases the time it takes to charge fully by 0.5s
                Echo shot - Shortly after the first shot, another will immediately fire
                    NOTE: The echo shot will have the same damage as the previous shot, with the added bonus that you
                    can aim in the brief window that it doesn't exist (You get what I'm trying to say)
                    Can add up to 10 Echo shots, Upgrading will increase Echo shot by 1 and increase reload by 0.5
                    Past 5 Echo shots, adds an overheat effect which increases damage by 10% each time after the 5th
                    shot
            -- Evolution Cards --
            Ship 5 [Evo of ship 1] - Evolves during gameplay and grants the option to start as this ship
                NOTE: Replaces bullets with a sword that flies towards the mouse and dashes forward on click
                Please make a gif that shows the tutorial, I don't want to do a frame by frame animation :(
                Sword speeds up as it gets further from mouse, Choose one of two options to implement ->
                    Screen wrap ability - Dashes in a straight line with a little curve wrapping around when off-screen
                        NOTE: Damage buff by 50%
                    Lazer ability - Shoots a lazer out of the tip of the sword
                        NOTE: Lazer deals half damage, sword is unable to move while the lazer is firing
            Ship 6 [Evo of ship 2] - Shoots black holes that sucks bullets into it while damaging enemies [NOT FINAL]
                NOTE: This requires a fish-eye effect to work, which will be very hard to do. Also, the code is just
                find the angle between bullet and black hole, check if that angle is less than, or greater than current
                angle, change angle accordingly
                    NOTE NOTE:
                    When changing the angle, only do it if the distance from the nearest black hole is less than 1.5x
                    radius of black hole, also change angle by ((1.5x * radius) - distance) and delete bullet when 0.5x
                    from radius (DRAW BLACK HOLES UNDER BULLETS) By delete I mean fast fade (set lifetime to 0)

        :return:
        """
        pass


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

        self.i_frames = 0

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
        if self.i_frames > 0:
            self.i_frames -= 0.1

    def update_animation(self):
        if self.anim_speed > 0:
            self.anim_speed -= 0.1

        if self.anim_speed <= 0:
            self.holder_image = self.image
            self.current_image = pygame.transform.rotate(self.holder_image, -self.angle)

    def take_damage(self, amount, i=False):
        if i and self.i_frames > 0:
            pass
        else:
            if self.health - amount >= 0:
                self.health -= amount
            else:
                self.health = 0
            if i:
                self.i_frames = i


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
    def __init__(self, health, max_health, screen, pos_x=10, pos_y=10, type_="h"):
        self.image = pygame.transform.rotozoom(pygame.image.load("Sprites/Extras/0.svg"), 0, 1.5)
        self.health = health
        self.mx_health = max_health
        self.screen = screen
        self.pos_x, self.pos_y = pos_x, pos_y
        self.len = self.image.get_width()
        self.height = self.image.get_height()
        self.target_health = self.len
        self.health_change_speed = 0.5

        self.type = type_

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

        if self.type == "h":
            color = (0, 250, 0)
        else:
            color = (0, 100, 250)

        # // Inner Bar //
        pygame.draw.rect(self.screen, color, (self.pos_x, self.pos_y, shown, self.height))

    def down(self):
        # This is just a test function to see if the healthBar actually works
        self.health -= 1

    def update(self):
        self.show_bar()


class Deaths:
    def __init__(self, type_, image, pos, damage=0, size=1):
        self.type = type_
        self.size = size
        self.image = pygame.transform.rotozoom(pygame.image.load(image), 0, size)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.rect = self.image.get_rect(center=self.pos)
        self.opacity = 400
        self.damage = damage
        self.dealt = False

    def refresh(self):
        self.opacity -= 25


class PickUp:
    def __init__(self, angle, speed, position, type_, image, lifetime, value):
        self.pick_up_range = 100

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


class TitleButtons:
    def __init__(self, image, pos, scale, type_, max_scale, direction_exit=0, enter=0, enter_loop=50, velX=10, opacity=300, increase=6):
        self.current_img = pygame.transform.rotozoom(pygame.image.load(image), 0, scale)
        self.type = type_
        self.scale = scale
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.velX = velX
        self.velY = 0
        self.perm_scale = scale
        self.brightness = 0
        self.opacity = opacity
        self.target_scale = self.scale
        self.rect = self.current_img.get_rect(center=self.pos)
        self.mouse = [False, False, False, direction_exit]
        self.enter = enter
        self.loop = enter_loop
        self.max_scale = max_scale
        self.opacity_increase = increase
        self.is_alive = True

    def change_scale(self):
        if self.target_scale != self.scale:
            if self.target_scale < self.scale:
                self.scale -= 0.1
            else:
                self.scale += 0.1

    def check_mouse(self):
        if self.brightness > 0:
            self.brightness -= 5
        if self.mouse[1] and self.target_scale != self.max_scale:
            self.target_scale = self.max_scale
        elif not self.mouse[1] and self.target_scale != self.perm_scale:
            self.target_scale = self.perm_scale

    def exit_click(self):
        if self.mouse[0] and self.mouse[1] and not self.mouse[2]:
            self.mouse[2] = True
            self.brightness = 200
        if self.mouse[2]:
            if self.mouse[3] == 0:
                self.velX -= 0.1
            else:
                self.velX += 0.1

    def enter_anim(self):
        if self.enter == 0 and self.loop > 0:
            if self.mouse[3] == 0:
                self.velX += 0.1
            elif self.mouse[3] == 1:
                self.velX -= 0.1
            elif self.mouse[3] == 2:
                self.opacity += 6

            self.loop -= 1
        elif self.enter == 0:
            self.enter = 1

    def not_static_return(self):
        if self.mouse[0] and self.mouse[1]:
            return True

    def update_pos(self):
        self.pos[0] += self.velX
        self.pos[1] += self.velY
        self.rect = self.current_img.get_rect(center=self.pos)

    def refresh(self):
        item = False
        if self.type != "static":
            self.change_scale()
            self.check_mouse()
            item = self.not_static_return()
        self.exit_click()
        self.enter_anim()
        self.update_pos()
        if item:
            return self.type
