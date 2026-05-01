# Imports
import pygame, sys
from pygame.locals import *
import random, time

pygame.init()
pygame.mixer.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
SCORE = 0
COINS = 0

#система уровней
LEVEL_THRESHOLD = 10   # каждые 10 монет
next_level = 10

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

DISPLAYSURF = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Game")


# ===================== ENEMY =====================
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# ===================== PLAYER =====================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


# ===================== COIN =====================
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.base_image = pygame.image.load("coin.png")
        self.base_image = pygame.transform.scale(self.base_image, (30, 30))

        self.image = self.base_image
        self.rect = self.image.get_rect()

        self.weight = random.choice([1, 3, 5])  # вес монеты
        self.respawn()

    def respawn(self):
        # случайный вес
        self.weight = random.choice([1, 3, 5])

        # визуально меняем размер
        size = 20 + self.weight * 5
        self.image = pygame.transform.scale(self.base_image, (size, size))
        self.rect = self.image.get_rect()

        self.rect.center = (
            random.randint(30, SCREEN_WIDTH - 30),
            random.randint(-100, -40)
        )

    def move(self):
        self.rect.move_ip(0, 4)

        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()


# объекты
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)


# ===================== GAME LOOP =====================
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))

    # текст
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    coins_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coins_text, (300, 10))

    # движение
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # ===================== СБОР МОНЕТ =====================
    if pygame.sprite.spritecollideany(P1, coins):
        COINS += C1.weight
        C1.respawn()

        # 🔥 правильное увеличение скорости
        if COINS >= next_level:
            SPEED += 1
            next_level += LEVEL_THRESHOLD

    # ===================== СТОЛКНОВЕНИЕ =====================
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        pygame.mixer.Sound("crash.wav").play()
        time.sleep(1)

        DISPLAYSURF.fill((255, 0, 0))
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)