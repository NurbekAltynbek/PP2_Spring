import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

x, y = 400, 300

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT] and x - 20 >= 25:
        x -= 20
    if pressed[pygame.K_RIGHT] and x + 20 <= 800 - 25:
        x += 20
    if pressed[pygame.K_UP] and y - 20 >= 25:
        y -= 20
    if pressed[pygame.K_DOWN] and y + 20 <= 600 - 25:
        y += 20

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 25)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()