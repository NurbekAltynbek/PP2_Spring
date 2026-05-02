import pygame, json, random
from game import run_game
from db import create_tables, get_top10, get_best

pygame.init()
screen = pygame.display.set_mode((600,600))
font = pygame.font.SysFont(None,40)

def load_settings():
    with open("settings.json") as f:
        return json.load(f)

def save_settings(s):
    with open("settings.json","w") as f:
        json.dump(s,f,indent=4)

def random_color():
    return [random.randint(0,255) for _ in range(3)]

def settings_screen():
    s=load_settings()
    while True:
        screen.fill((0,0,0))
        screen.blit(font.render(f"G Grid:{s['grid']}",True,(255,255,255)),(150,200))
        screen.blit(font.render(f"S Sound:{s['sound']}",True,(255,255,255)),(150,250))
        screen.blit(font.render("C Color",True,(255,255,255)),(150,300))
        pygame.draw.rect(screen,tuple(s["color"]),(250,350,100,50))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE:
                    save_settings(s)
                    return
                if e.key==pygame.K_g:
                    s["grid"]=not s["grid"]
                if e.key==pygame.K_s:
                    s["sound"]=not s["sound"]
                if e.key==pygame.K_c:
                    s["color"]=random_color()

def input_name():
    name=""
    while True:
        screen.fill((0,0,0))
        screen.blit(font.render("Enter name:",True,(255,255,255)),(200,200))
        screen.blit(font.render(name,True,(0,255,0)),(200,250))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN:
                    return name or "Player"
                elif e.key==pygame.K_BACKSPACE:
                    name=name[:-1]
                else:
                    name+=e.unicode

def leaderboard():
    data=get_top10()
    screen.fill((0,0,0))
    y=100
    for i,row in enumerate(data):
        screen.blit(font.render(f"{i+1}. {row[0]} {row[1]}",True,(255,255,255)),(150,y))
        y+=30
    pygame.display.flip()
    pygame.time.delay(3000)

def game_over(username,score,level):
    best=max(score,get_best(username))
    while True:
        screen.fill((0,0,0))
        screen.blit(font.render(f"Score:{score}",True,(255,255,255)),(200,200))
        screen.blit(font.render(f"Best:{best}",True,(255,255,0)),(200,250))
        screen.blit(font.render("R Retry / M Menu",True,(255,255,255)),(150,350))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_r:
                    score,level=run_game(username)
                if e.key==pygame.K_m:
                    return

def menu():
    while True:
        screen.fill((0,0,0))
        screen.blit(font.render("1 Play",True,(255,255,255)),(200,200))
        screen.blit(font.render("2 Leaderboard",True,(255,255,255)),(200,250))
        screen.blit(font.render("3 Settings",True,(255,255,255)),(200,300))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_1:
                    name=input_name()
                    score,level=run_game(name)
                    game_over(name,score,level)
                if e.key==pygame.K_2:
                    leaderboard()
                if e.key==pygame.K_3:
                    settings_screen()

create_tables()
menu()