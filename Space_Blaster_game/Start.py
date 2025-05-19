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

# -- Less Important Setup --
background = pygame.transform.scale(pygame.image.load("Sprites/Backgrounds/bground1.svg"), (100, 100))

plist = []
phealth = []
projectiles = []
healthBars = []
enemies = []

level_start = False
current_username = False

i_frames = 0

# --- Class Creation ---


# --- Update Loops ---
def check_collision(danger, target):
    return danger.pos[0] < target.pos[0] + target.width and danger.pos[0] + danger.width > target.pos[0] and danger.pos[1] < target.pos[1] + target.height and danger.pos[1] + danger.height > target.pos[1]


def check_collide():
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

        if p.health <= 0:
            plist.pop(count)
            print("player died")

        count += 1

        # this is just to test out damage
        keys = pygame.key.get_pressed()

        global i_frames

        if keys[pygame.K_r] and i_frames <= 0:
            p.take_damage(3)
            i_frames += 1
        elif i_frames > 0:
            i_frames -= 0.1
    if count == 0:
        player_pos = [0, 0]


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

        if enemy.health <= 0:
            enemies.pop(count)

        count += 1

        # this is just to test out damage
        keys = pygame.key.get_pressed()

        global i_frames

        if keys[pygame.K_p] and i_frames <= 0:
            enemy.take_damage(3)
            i_frames += 1
        elif i_frames > 0:
            i_frames -= 0.1


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

        if pew.opacity <= 0:
            projectiles.pop(count)
            print("\b" * 9999, end="", flush=True)
            print(f"{len(projectiles)}", end="")

        count += 1


# --- Create Functions ---
def create_healthBar(type_, health, maxHealth, screen, pos):
    bar = HealthBar(health, maxHealth, screen, pos[0], pos[1])

    if type_ == "p":
        phealth.append(bar)
    else:
        healthBars.append(bar)


def create_player():
    player = Player("Sprites/Player/basic ship.svg", ["Sprites/Player/basic ship2.svg"], [100, 500], 1, 5, 2, 5, 15, 10,
                    True, [WIDTH, HEIGHT])
    create_healthBar("p", player.health, player.maxHealth, screen, player.pos)
    plist.append(player)


def create_enemy(img, anim_paths, start_pos, type_, speed, fireRate, damage, bull_speed, scale, starting_angle=180, health=50, max_health=50):
    enemy = Enemy(img, anim_paths, start_pos, type_, speed, fireRate, damage, 15, bull_speed, True, [WIDTH, HEIGHT], scale, health, max_health, starting_angle)
    enemies.append(enemy)
    create_healthBar("e", enemy.health, enemy.maxHealth, screen, enemy.pos)


def create_projectile(type_, speed, damage, pos, angle, lifeTime):
    projectile = Bullet(type_[0], speed, lifeTime, type_[1], damage, angle, pos)
    projectiles.append(projectile)


# --- Save Files ---
def save_current():
    with open("Text/Important_text/saves.txt") as file:
        file = file.read().split("|")

    print(len(file))


# -- Test Area --
create_player()
create_enemy("Sprites/Enemies/Enemy1/common.svg", ["Sprites/Enemies/Enemy1/common2.svg"], [50, 50], "1", 3, 10, 1, 7, 0.5)
create_enemy("Sprites/Enemies/Enemy2/basic.svg", ["Sprites/Enemies/Enemy2/basic2.svg"], [1380, 500], "2", 2, 10, 1, 7, 0.7, 180, 150, 150)
create_enemy("Sprites/Enemies/Enemy2/basic.svg", ["Sprites/Enemies/Enemy2/basic2.svg"], [1380, 200], "2", 2, 10, 1, 7, 0.7, 180, 150, 150)

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
    screen.fill((0, 0, 10))

    update_projectile(screen)
    check_collide()
    update_player(screen)
    update_enemies(screen)

    pygame.display.update()

    clock.tick(FPS)

    print("\b" * 9999, end="", flush=True)
    print(f"Bullet count: {len(projectiles)} Player pos: {player_pos} Player Health: {player_health}", end="")

pygame.quit()
