import pygame
import random
from Space_Blaster_game.Classes import *
from Space_Blaster_game.Important_Variables import *

pygame.init()

# --- Setup ---

running = True

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
window_adjust = (pygame.display.Info().current_w, pygame.display.Info().current_h)

clock = pygame.time.Clock()
pygame.display.set_caption("Space Blaster")
winWidget = pygame.image.load("OtherImg/window widget.svg")
pygame.display.set_icon(winWidget)

spawn = []

# -- Less Important Setup --
background = pygame.transform.scale(pygame.image.load("Sprites/Backgrounds/bground1.svg"), (100, 100))

plist = []
phealth = []
projectiles = []
healthBars = []
enemies = []
deaths = []

current_username = False

i_frames = 0

# --- Class Creation ---


# --- Update Loops ---
def check_collision(danger, target):
    return danger.pos[0] < target.pos[0] + target.width and danger.pos[0] + danger.width > target.pos[0] and danger.pos[1] < target.pos[1] + target.height and danger.pos[1] + danger.height > target.pos[1]


def check_collide():
    # Remember to come back to add mine explosions, target list is deaths[]

    count = 0
    for bull in projectiles:
        if bull.opacity >= 100:
            if bull.type == "player":
                for i in enemies:
                    temp = pygame.sprite.collide_rect(i, bull)
                    if temp:
                        i.take_damage(bull.damage)
                        projectiles.pop(count)
            else:
                for pl in plist:
                    temp = pygame.sprite.collide_rect(pl, bull)
                    if temp:
                        pl.take_damage(bull.damage)
                        projectiles.pop(count)

        count += 1


def update_health(pos, health, index, offset):
    healthBars[index].pos_x, healthBars[index].pos_y = pos[0] - healthBars[index].len/2, pos[1] - offset
    healthBars[index].health = health
    healthBars[index].update()


def player_update_health(pos, health, index, offset):
    phealth[index].pos_x, phealth[index].pos_y = pos[0] - phealth[index].len/2, pos[1] - offset
    phealth[index].health = health
    phealth[index].update()


def update_player(screen):
    count = 0
    for p in plist:
        p.screen_par = [c_w, c_h]
        check = p.refresh()

        global player_pos
        player_pos = p.pos

        global player_health
        player_health = p.health

        screen.blit(p.current_image, p.imOutline)

        player_update_health(p.pos, p.health, count, p.image.get_height() + 10)

        if hitBoxes:
            pygame.draw.rect(screen, "red", p.hitBox, width=2)
            pygame.draw.rect(screen, "green", p.imOutline, width=2)

        if check:
            if check[5] == "player":
                create_projectile([check[4], "player"], check[1], check[0], p.imOutline.center,
                                  p.angle + random.randint(-100, 100) / 10, check[2])

        count += 1

        # this is just to test out damage
        keys = pygame.key.get_pressed()

        global i_frames

        if keys[pygame.K_r] and i_frames <= 0:
            p.take_damage(3)
            i_frames += 1
        elif i_frames > 0:
            i_frames -= 0.1

    count = 0

    for p in plist:
        try:
            if p.health <= 0:
                create_death(p.pos, "s")
                phealth.pop(count)
                plist.pop(count)
            count += 1
        except IndexError:
            pass

    if count == 0:
        pass


def update_enemies(screen):
    count = 0

    for enemy in enemies:
        check = enemy.refresh()

        screen.blit(enemy.current_image, enemy.imOutline)

        enemy.player_pos[0] = player_pos

        update_health(enemy.pos, enemy.health, count, enemy.image.get_height() + 10)

        if hitBoxes:
            pygame.draw.rect(screen, "red", enemy.hitBox, width=2)
            pygame.draw.rect(screen, "green", enemy.imOutline, width=2)

        if check:
            if check[5] == "enemy":
                create_projectile([check[4], "enemy"], check[1], check[0], enemy.imOutline.center,
                                  enemy.angle + random.randint(-50, 50) / 10, check[2])

        count += 1

        # this is just to test out damage
        keys = pygame.key.get_pressed()

        global i_frames

        if keys[pygame.K_p] and i_frames <= 0:
            enemy.take_damage(5)
            i_frames += 1
        elif i_frames > 0:
            i_frames -= 0.1

    count = 0

    for enemy in enemies:
        try:
            if enemy.health <= 0:
                create_death(enemy.pos, "s")
                healthBars.pop(count)
                enemies.pop(count)
            count += 1
        except IndexError:
            pass


def update_projectile(screen):
    count = 0
    for pew in projectiles:
        pew.refresh()

        pew.image.set_alpha(pew.opacity)
        screen.blit(pew.image, pew.pos)

        if hitBoxes:
            if pew.type == "player":
                pygame.draw.rect(screen, "green", pew.hurtBox, width=2)
            else:
                pygame.draw.rect(screen, "red", pew.hurtBox, width=2)

        count += 1

    count = 0

    for pew in projectiles:
        try:
            if pew.opacity <= 0:
                projectiles.pop(count)

            count += 1
        except IndexError:
            pass


def update_deaths(screen):
    count = 0
    for boom in deaths:
        boom.refresh()

        boom.image.set_alpha(boom.opacity)
        screen.blit(boom.image, boom.pos)

        if hitBoxes:
            if boom.type == "p":
                pygame.draw.rect(screen, "green", boom.hurtBox, width=2)
            else:
                pygame.draw.rect(screen, "red", boom.hurtBox, width=2)

        count += 1

    count = 0

    for boom in projectiles:
        try:
            if boom.opacity <= 0:
                deaths.pop(count)

            count += 1
        except IndexError:
            pass


# --- Create Functions ---
def create_healthBar(type_, health, maxHealth, screen, pos):
    bar = HealthBar(health, maxHealth, screen, pos[0], pos[1])

    if type_ == "p":
        phealth.append(bar)
    else:
        healthBars.append(bar)


def create_player():
    player = Player("Sprites/Player/basic ship.svg", ["Sprites/Player/basic ship2.svg"], [-100, 360], 1, 4.5, 2, 5, 15, 10,
                    False, [WIDTH, HEIGHT])
    create_healthBar("p", player.health, player.maxHealth, screen, player.pos)
    plist.append(player)


def create_enemy(img, anim_paths, start_pos, type_, speed, fireRate, damage, bull_speed, scale, starting_angle=180, health=50, max_health=50):
    enemy = Enemy(img, anim_paths, start_pos, type_, speed, fireRate, damage, 15, bull_speed, True, [WIDTH, HEIGHT], scale, health, max_health, starting_angle)
    enemies.append(enemy)
    create_healthBar("e", enemy.health, enemy.maxHealth, screen, enemy.pos)


def create_projectile(type_, speed, damage, pos, angle, lifeTime):
    projectile = Bullet(type_[0], speed, lifeTime, type_[1], damage, angle, pos)
    projectiles.append(projectile)


def create_death(pos, type_):
    if type_ == "s":
        death = Deaths("s", "Sprites/Extras/Deaths/EXPLOSION small.svg", pos)
        deaths.append(death)
    elif type_ == "minePlayer":
        death = Deaths("p", "Sprites/Extras/Deaths/EXPLOSION small.svg", pos)
        deaths.append(death)
    elif type_ == "mineEnemy":
        death = Deaths("e", "Sprites/Extras/Deaths/EXPLOSION small.svg", pos)
        deaths.append(death)


# --- Enemy Spawner ---
def spawn_queue():
    if len(spawn):
        if spawn[0][1] > 0:
            spawn[0][1] -= 0.1
        else:
            create_enemy(spawn[0][0][0], spawn[0][0][1], spawn[0][0][2], spawn[0][0][3], spawn[0][0][4], spawn[0][0][5], spawn[0][0][6], spawn[0][0][7], spawn[0][0][8], spawn[0][0][9], spawn[0][0][10], spawn[0][0][11])
            spawn.pop(0)


def enemy_presets(type_, formation):
    # 1st Image, [collection of images here], [posX, posY], type, speed, fire rate, damage, bullet speed, scale, angle,
    # health, max health
    if type_ == "1":
        if formation == "1":
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 360], "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 0])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 460], "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 5])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 260], "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 0])
        elif formation == "2":
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 50],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 0])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 120],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 3])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 190],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 3])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 670],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 10])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 600],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 3])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 530],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 3])
        elif formation == "3":
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 360],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 0])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 460],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 5])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 260],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 0])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 560],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 5])
            spawn.append([["Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [1380, 160],
                           "1", 3, 30, 1, 5, 0.5, 180, 50, 50], 0])
        else:
            print("ERROR! Formation not found!")
    elif type_ == "2":
        if formation == "1":
            spawn.append([["Sprites/Enemies/Enemy2/basic.svg", ["Sprites/Enemies/Enemy2/basic2.svg"], [1380, 360], "2", 2, 10, 2, 5, 0.7, 180, 150, 150], 0])
            spawn.append([["Sprites/Enemies/Enemy2/basic.svg", ["Sprites/Enemies/Enemy2/basic2.svg"], [1380, 460], "2",
                           2, 10, 2, 5, 0.7, 180, 150, 150], 5])
            spawn.append([["Sprites/Enemies/Enemy2/basic.svg", ["Sprites/Enemies/Enemy2/basic2.svg"], [1380, 260], "2",
                           2, 10, 2, 5, 0.7, 180, 150, 150], 0])
        elif formation == "2":
            spawn.append([["Sprites/Enemies/Enemy2/basic.svg", ["Sprites/Enemies/Enemy2/basic2.svg"], [1380, 70], "2",
                           2, 10, 2, 5, 0.7, 180, 150, 150], 0])
            spawn.append([["Sprites/Enemies/Enemy2/basic.svg", ["Sprites/Enemies/Enemy2/basic2.svg"], [1380, 650], "2",
                           2, 10, 2, 5, 0.7, 180, 150, 150], 0])
        else:
            print("ERROR! Formation not found!")
    else:
        print("ERROR! Enemy not found!")


def level_reader(world):
    global level_complete

    if level_complete:
        return

    with open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "r") as lines:
        wave, timer, min_e, complete, time_until = lines.read().split("\n")
        wave = int(wave)
        timer = float(timer)
        min_e = int(min_e)
        complete = int(complete)
        time_until = float(time_until)

    print("\b" * 9999, end="", flush=True)
    print(f"Wave: {wave} Timer: {timer} Minimum Enemy: {min_e} Wave Completed: {complete} Time Until: {time_until}", end="")

    try:
        if world[wave] == "pass":
            pass
    except IndexError:
        return

    if time_until > 0:
        time_until -= 0.1
        file = open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "w")
        file.write(f"{wave}\n{world[wave].split("/")[3]}\n{world[wave].split("/")[2]}\n{complete}\n{time_until}")
        file.close()
        return
    else:
        pass

    if complete:
        if world[wave].split("/")[4] == "C":
            if min_e >= 0:
                if len(enemies) <= min_e:
                    if wave == len(world):
                        wave += 1
                        file = open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "w")
                        file.write(f"{wave}\n0\n0\n0\n0")
                        file.close()

                        level_complete = True
                    else:
                        wave += 1

                        file = open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "w")
                        file.write(f"{wave}\n{world[wave].split("/")[3]}\n{world[wave].split("/")[2]}\n0\n0")
                        file.close()
            if timer == -5:
                print("Running", end="")
                pass
            elif timer > 0:
                timer -= 0.1
                file = open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "w")
                file.write(f"{wave}\n{timer}\n{world[wave].split("/")[2]}\n{complete}\n0")
                file.close()
            else:
                if wave == len(world):
                    wave += 1

                    file = open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "w")
                    file.write(f"{wave}\n0\n0\n0\n0")
                    file.close()

                    level_complete = True
                else:
                    wave += 1

                    file = open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "w")
                    file.write(f"{wave}\n{world[wave].split("/")[3]}\n{world[wave].split("/")[2]}\n0\n0")
                    file.close()
        else:
            if len(enemies) <= 0:
                if wave == len(world) - 1:
                    wave += 1
                    file = open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "w")
                    file.write(f"{wave}\n0\n0\n0\n8")
                    file.close()

                    level_complete = True
                else:
                    wave += 1

                    file = open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "w")
                    file.write(f"{wave}\n{world[wave].split("/")[3]}\n{world[wave].split("/")[2]}\n0\n8")
                    file.close()

    else:
        enemy_presets(world[wave].split("/")[0], world[wave].split("/")[1])
        file = open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "w")
        file.write(f"{wave}\n{world[wave].split("/")[3]}\n{world[wave].split("/")[2]}\n1\n0")
        file.close()


# --- Save Files ---
def open_levels(world):
    with open("Text/Important_text/levels.txt", "r") as lines:
        lines = lines.read().split("|")

    lines.pop(0)

    var = False
    for i in lines:
        if world == i.split("\n")[1]:

            var = i

    if len(var.split("\n")) > 4:
        # Trust me when I say that this part is totally necessary
        var = var.split("\n")
        var.pop(0)
        var.pop(0)
        var.pop(-1)
        print("Found star system.")
        print(f"Result: \033[92m{var}\033[0m")
        file = open("Text/Important_text/Too_lazy_to_make_efficient_level_thing_so_Im_making_this.txt", "w")
        file.write(f"0\n{var[0].split("/")[1]}\n{var[0].split("/")[2]}\n0\n8")
        # 1st one is wave, second one is timer, third one is minimum enemy,
        # fourth one is completed (0 = False, 1 = True), 5th one is timer till next wave
        file.close()
        return var
    else:
        print("ERROR! Levels not found!")
        print(f"Result: \033[91m{var}\033[0m")


# -- Test Area --
create_player()

world = open_levels("S1")

stars = pygame.transform.rotozoom(pygame.image.load("Sprites/Extras/Backgrounds/Star Preset1.svg"), 0, 2.7)

# Main game loop
while running:
    # Event/User input loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Doesn't let the window shrink past this size
            width, height = event.size
            if width < 850:
                width = 850
            if height < 500:
                height = 500

            c_w, c_h = width, height

            screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    # Update screen
    if not game_pause and level_start:
        screen.fill((0, 0, 10))

        screen.blit(stars, [0, -100])

        level_reader(world)

        spawn_queue()

        update_projectile(screen)

        check_collide()

        update_player(screen)
        update_enemies(screen)

        update_deaths(screen)

        pygame.display.update()

    clock.tick(FPS)

    # print("\b" * 9999, end="", flush=True)
    # print(f"Health Bar count: [{len(healthBars)}] [{len(phealth)}]", end="")

pygame.quit()
