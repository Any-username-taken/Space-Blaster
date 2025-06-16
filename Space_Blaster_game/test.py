import pygame as pg


def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pg.transform.rotozoom(surface, -angle, 0.5)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
BG_COLOR = pg.Color('gray12')
# The original image will never be modified.
IMAGE = pg.image.load("Sprites/Player/Ship 4/RailGun2.svg")
# Change image here so that I can find the center of rotation
# Store the original center position of the surface.
pivot = [250, 250]
# This offset vector will be added to the pivot point, so the
# resulting rect will be blitted at `rect.topleft + offset`.
offset = pg.math.Vector2(0, 0)
angle = 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_d]:
        angle += 1
    elif keys[pg.K_a]:
        angle -= 1
    elif keys[pg.K_SPACE]:
        angle = 0
    if keys[pg.K_RIGHT]:
        pivot[0] += 5
    if keys[pg.K_LEFT]:
        pivot[0] -= 5
    if keys[pg.K_UP]:
        pivot[1] -= 5
    if keys[pg.K_DOWN]:
        pivot[1] += 5
    if keys[pg.K_k]:
        offset[1] += 1
    if keys[pg.K_i]:
        offset[1] -= 1
    if keys[pg.K_j]:
        offset[0] -= 1
    if keys[pg.K_l]:
        offset[0] += 1


    # Rotated version of the image and the shifted rect.
    rotated_image, rect = rotate(IMAGE, angle, pivot, offset)

    rectangle = rotated_image.get_rect()

    # Drawing.
    screen.fill(BG_COLOR)
    screen.blit(rotated_image, rect)  # Blit the rotated image.
    pg.draw.circle(screen, (30, 250, 70), pivot, 3)  # Pivot point.
    pg.draw.rect(screen, (30, 250, 70), rect, 1)  # The rect.
    pg.display.set_caption(f"Angle: {angle}, Offset pos: {offset}, Pivot: {pivot}")
    pg.display.flip()
    clock.tick(30)

pg.quit()

