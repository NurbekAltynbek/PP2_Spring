import pygame
from player import play_track, stop_track, next_track, previous_track, get_track_name, get_track_position

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((700, 300))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

running = True

while running:
    screen.fill((30, 30, 30))

    title = font.render("Music Player", True, (255, 255, 255))
    track_text = small_font.render("Track: " + get_track_name(), True, (255, 255, 255))
    pos_text = small_font.render("Position: " + get_track_position(), True, (200, 200, 200))
    controls_text = small_font.render("P-play  S-stop  N-next  B-back  Q-quit", True, (200, 200, 200))

    screen.blit(title, (250, 40))
    screen.blit(track_text, (50, 110))
    screen.blit(pos_text, (50, 150))
    screen.blit(controls_text, (50, 220))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play_track()
            elif event.key == pygame.K_s:
                stop_track()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                previous_track()
            elif event.key == pygame.K_q:
                running = False

pygame.quit()