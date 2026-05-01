import pygame
import random
from color_palette import *

pygame.init()

# Размер окна
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Размер клетки
CELL = 30
ROWS = HEIGHT // CELL
COLS = WIDTH // CELL

# Шрифты
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)

clock = pygame.time.Clock()


def draw_grid():
    # рисуем сетку
    for i in range(ROWS):
        for j in range(COLS):
            pygame.draw.rect(screen, colorGRAY, (j * CELL, i * CELL, CELL, CELL), 1)


def draw_walls():
    # рисуем границы
    for x in range(COLS):
        pygame.draw.rect(screen, colorBLUE, (x * CELL, 0, CELL, CELL))
        pygame.draw.rect(screen, colorBLUE, (x * CELL, (ROWS - 1) * CELL, CELL, CELL))

    for y in range(ROWS):
        pygame.draw.rect(screen, colorBLUE, (0, y * CELL, CELL, CELL))
        pygame.draw.rect(screen, colorBLUE, ((COLS - 1) * CELL, y * CELL, CELL, CELL))


class Point:
    # точка
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        self.body = [Point(10, 10), Point(9, 10), Point(8, 10)]
        self.dx = 1
        self.dy = 0

    def move(self):
        # движение змейки
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        # рисуем змейку
        pygame.draw.rect(screen, colorRED, (self.body[0].x * CELL, self.body[0].y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def grow(self):
        # увеличиваем длину
        tail = self.body[-1]
        self.body.append(Point(tail.x, tail.y))

    def check_self_collision(self):
        # столкновение с собой
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    def check_wall_collision(self):
        # столкновение со стеной
        head = self.body[0]
        if head.x <= 0 or head.x >= COLS - 1 or head.y <= 0 or head.y >= ROWS - 1:
            return True
        return False

    def check_food_collision(self, food):
        # съел еду
        head = self.body[0]
        return head.x == food.pos.x and head.y == food.pos.y


class Food:
    def __init__(self, snake):
        self.pos = Point(0, 0)

        # 🔥 вес еды (1 или 3)
        self.weight = random.choice([1, 3])

        # 🔥 таймер
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000  # 5 секунд

        self.generate_random_pos(snake)

    def draw(self):
        # цвет зависит от веса
        color = colorGREEN if self.weight == 1 else colorRED
        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake):
        while True:
            x = random.randint(1, COLS - 2)
            y = random.randint(1, ROWS - 2)

            if not any(segment.x == x and segment.y == y for segment in snake.body):
                self.pos = Point(x, y)

                # новый вес и таймер
                self.weight = random.choice([1, 3])
                self.spawn_time = pygame.time.get_ticks()
                break


def draw_info(score, level, speed):
    # отображение текста
    screen.blit(font.render(f"Score: {score}", True, colorWHITE), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, colorWHITE), (10, 35))
    screen.blit(font.render(f"Speed: {speed}", True, colorWHITE), (10, 60))


def game_over_screen(score, level):
    screen.fill(colorBLACK)

    screen.blit(big_font.render("GAME OVER", True, colorRED), (180, 250))
    screen.blit(font.render(f"Score: {score}", True, colorWHITE), (240, 300))
    screen.blit(font.render(f"Level: {level}", True, colorWHITE), (240, 330))

    pygame.display.flip()
    pygame.time.delay(3000)


# старт
snake = Snake()
food = Food(snake)

score = 0
level = 1
foods_eaten = 0

FPS = 5

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx = 1; snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1; snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0; snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0; snake.dy = -1

    if not game_over:
        snake.move()

        # столкновения
        if snake.check_wall_collision() or snake.check_self_collision():
            game_over = True

        # 🔥 съел еду
        if snake.check_food_collision(food):
            snake.grow()
            score += food.weight
            foods_eaten += 1
            food.generate_random_pos(snake)

            # уровень
            if foods_eaten % 4 == 0:
                level += 1
                FPS += 2

        # 🔥 таймер исчезновения еды
        if pygame.time.get_ticks() - food.spawn_time > food.lifetime:
            food.generate_random_pos(snake)

        # отрисовка
        screen.fill(colorBLACK)
        draw_grid()
        draw_walls()
        snake.draw()
        food.draw()
        draw_info(score, level, FPS)

        pygame.display.flip()
        clock.tick(FPS)

    else:
        game_over_screen(score, level)
        running = False

pygame.quit()