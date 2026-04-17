import pygame
from clock import MickeyClock

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()
mickey_clock = MickeyClock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mickey_clock.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()