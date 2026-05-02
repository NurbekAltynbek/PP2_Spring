import pygame, random, json
from db import save_score, get_best

WIDTH, HEIGHT = 600, 600
CELL = 20

def load_settings():
    with open("settings.json") as f:
        return json.load(f)

def draw_grid(screen):
    for x in range(0, WIDTH, CELL):
        for y in range(0, HEIGHT, CELL):
            pygame.draw.rect(screen,(40,40,40),(x,y,CELL,CELL),1)

# 🔥 безопасные препятствия
def generate_obstacles_safe(snake):
    obstacles = []

    safe_zone = set()
    hx, hy = snake[0]

    for dx in range(-2, 3):
        for dy in range(-2, 3):
            safe_zone.add((hx + dx*CELL, hy + dy*CELL))

    while len(obstacles) < 10:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        p = (x, y)

        if p not in snake and p not in obstacles and p not in safe_zone:
            obstacles.append(p)

    return obstacles

def run_game(username):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None,30)

    settings = load_settings()
    snake_color = tuple(settings["color"])

    snake = [(100,100),(80,100),(60,100)]
    direction = (20,0)

    obstacles = []

    # 🔥 правильный спавн
    def gen_pos():
        while True:
            p = (random.randrange(0,WIDTH,CELL),
                 random.randrange(0,HEIGHT,CELL))

            if p not in snake and p not in obstacles:
                return p

    food = gen_pos()
    poison = gen_pos()

    power = None
    power_type = None
    spawn_time = 0
    active_time = 0

    score = 0
    level = 1
    speed = 7
    shield = False

    best = get_best(username)

    running = True
    while running:
        now = pygame.time.get_ticks()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return score, level
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: direction=(0,-20)
                if e.key == pygame.K_DOWN: direction=(0,20)
                if e.key == pygame.K_LEFT: direction=(-20,0)
                if e.key == pygame.K_RIGHT: direction=(20,0)

        head = (snake[0][0]+direction[0], snake[0][1]+direction[1])

        # столкновения
        if head in snake or not(0<=head[0]<WIDTH and 0<=head[1]<HEIGHT):
            if shield:
                shield = False
            else:
                break

        if head in obstacles:
            if shield:
                shield = False
            else:
                break

        snake.insert(0, head)

        # еда
        if head == food:
            score += 1
            food = gen_pos()
        else:
            snake.pop()

        # яд
        if head == poison:
            snake = snake[:-2] if len(snake)>2 else snake
            if len(snake) <= 1:
                break
            poison = gen_pos()

        # power spawn
        if power is None and random.random() < 0.01:
            power = gen_pos()
            power_type = random.choice(["speed","slow","shield"])
            spawn_time = now

        # исчезновение (8 сек)
        if power and now - spawn_time > 8000:
            power = None

        # подбор
        if power and head == power:
            if power_type == "speed":
                speed += 5
                active_time = now
            elif power_type == "slow":
                speed = max(5, speed - 3)
                active_time = now
            elif power_type == "shield":
                shield = True
            power = None

        # окончание эффекта (5 сек)
        if power_type in ["speed","slow"] and now - active_time > 5000:
            speed = 10 + level

        # 🔥 УРОВЕНЬ + ПРЕПЯТСТВИЯ
        if score >= level * 3:
            level += 1
            speed += 1

            if level >= 3:
                obstacles = generate_obstacles_safe(snake)

        # РЕНДЕР
        screen.fill((0,0,0))

        if settings["grid"]:
            draw_grid(screen)

        for s in snake:
            pygame.draw.rect(screen, snake_color, (*s,CELL,CELL))

        pygame.draw.rect(screen,(0,255,0),(*food,CELL,CELL))
        pygame.draw.rect(screen,(150,0,0),(*poison,CELL,CELL))

        if power:
            colors = {"speed":(0,255,255),"slow":(255,255,0),"shield":(255,0,255)}
            pygame.draw.rect(screen, colors[power_type], (*power,CELL,CELL))

        # 🔥 стены
        for o in obstacles:
            pygame.draw.rect(screen, (0,0,255), (*o,CELL,CELL))

        best = max(best, score)

        screen.blit(font.render(f"Score: {score}",True,(255,255,255)),(10,10))
        screen.blit(font.render(f"Best: {best}",True,(255,255,0)),(10,40))
        screen.blit(font.render(f"Level: {level}",True,(0,255,255)),(10,70))

        pygame.display.flip()
        clock.tick(speed)

    save_score(username, score, level)
    return score, level