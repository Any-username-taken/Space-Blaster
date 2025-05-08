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

# -- Less Important Setup --
background = pygame.transform.scale(pygame.image.load("Sprites/Backgrounds/bground1.svg"), (100, 100))

level_start = False
current_username = False

# --- Class Creation ---
player = Player("Sprites/Player/basic ship.svg", ["Sprites/Player/basic ship2.svg"], [100, 500], 1, 10, 2, 5, 30, 6, True, [WIDTH, HEIGHT])


# --- Update Loops ---
def check_collision(danger, target):
    return danger.pos[0] < target.pos[0] + target.width and danger.pos[0] + danger.width > target.pos[0] and danger.pos[1] < target.pos[1] + target.height and danger.pos[1] + danger.height > target.pos[1]


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
    screen.blit(background, (0, 0))

    screen.blit(player.current_image, player.imOutline)
    pygame.draw.rect(screen, "red", player.hitBox, width=2)
    pygame.draw.rect(screen, "green", player.imOutline, width=2)
    player.refresh()

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
