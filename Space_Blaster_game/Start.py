import pygame
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

surf = pygame.Surface((100, 200))
surf.fill("white")

projectiles = []
level_start = False
current_username = False


# --- Update Loops ---
def projectile_update():
    for bullet in projectiles:
        bullet.update()


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
            screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    # Update screen
    screen.fill((0, 0, 10))

    screen.blit(surf, (100, 150))
    pygame.display.update()

pygame.quit()
