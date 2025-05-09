import pygame
import random
from Space_Blaster_game.Classes import *
from Space_Blaster_game.Constants import *

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

projectiles = []

level_start = False
current_username = False

# --- Class Creation ---
player = Player("Sprites/Player/basic ship.svg", ["Sprites/Player/basic ship2.svg"], [100, 500], 1, 5, 2, 5, 15, 10, True, [WIDTH, HEIGHT])


# --- Update Loops ---
def check_collision(danger, target):
    return danger.pos[0] < target.pos[0] + target.width and danger.pos[0] + danger.width > target.pos[0] and danger.pos[1] < target.pos[1] + target.height and danger.pos[1] + danger.height > target.pos[1]


def update_projectile(screen):
    count = 0
    for pew in projectiles:
        pew.refresh()

        pew.image.set_alpha(pew.opacity)
        screen.blit(pew.image, pew.pos)

        if pew.opacity <= 0:
            projectiles.pop(count)
            print("\b" * 9999, end="", flush=True)
            print(f"{len(projectiles)}", end="")

        count += 1


# --- Create Functions ---
def create_projectile(type_, speed, damage, pos, angle, lifeTime):
    projectile = Bullet(type_[0], speed, lifeTime, type_[1], damage, angle, pos)
    projectiles.append(projectile)
    print("\b" * 9999, end="", flush=True)
    print(f"{len(projectiles)}", end="")


# --- Save Files ---
def save_current():
    with open("Text/Important_text/saves.txt") as file:
        file = file.read().split("|")

    print(len(file))


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

            player.screen_par = [width, height]
            screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    # Update screen
    screen.fill((0, 0, 10))

    screen.blit(background, (0, 0))

    screen.blit(player.current_image, player.imOutline)
    pygame.draw.rect(screen, "red", player.hitBox, width=2)
    pygame.draw.rect(screen, "green", player.imOutline, width=2)
    update_projectile(screen)
    idk = player.refresh()

    if idk:
        create_projectile([idk[4], "player"], idk[1], idk[0], player.imOutline.center, player.angle + random.randint(-100, 100)/10, idk[2])

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
