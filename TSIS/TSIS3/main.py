import pygame
from ui import main_menu, leaderboard_screen, username_input, settings_screen
from racer import run_game

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((480, 720))
pygame.display.set_caption("Racer Game")

while True:
    action = main_menu(screen)

    if action == "play":
        username = username_input(screen)
        if username:
            run_game(screen, username)

    elif action == "leaderboard":
        leaderboard_screen(screen)

    elif action == "settings":
        settings_screen(screen)

    else:
        break

pygame.quit()