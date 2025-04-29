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

projectiles = []

# --- Update Loops ---

# Main game loop
while running:
    screen.fill((0, 0, 10))

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

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

    pygame.display.flip()


pygame.quit()
