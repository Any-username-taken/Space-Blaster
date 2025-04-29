from Space_Blaster_game.Classes import *
from Space_Blaster_game.Constants import *

# --- Setup ---

running = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

projectiles = []

# --- Update Loops ---

# Main game loop
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))


pygame.quit()
