import pygame
from persistence import load_leaderboard, load_settings, save_settings

def main_menu(screen):
    font = pygame.font.SysFont(None, 50)

    while True:
        screen.fill((220,220,220))
        screen.blit(font.render("PLAY",1,(0,0,0)),(170,250))
        screen.blit(font.render("LEADERBOARD",1,(0,0,0)),(100,320))
        screen.blit(font.render("SETTINGS",1,(0,0,0)),(140,390))
        screen.blit(font.render("QUIT",1,(0,0,0)),(170,460))

        for e in pygame.event.get():
            if e.type==pygame.QUIT: return "quit"
            if e.type==pygame.MOUSEBUTTONDOWN:
                _,y=pygame.mouse.get_pos()
                if 250<y<300: return "play"
                if 320<y<370: return "leaderboard"
                if 390<y<440: return "settings"
                if 460<y<510: return "quit"

        pygame.display.update()

def username_input(screen):
    font=pygame.font.SysFont(None,40)
    name=""
    while True:
        screen.fill((255,255,255))
        screen.blit(font.render("Enter Username:",1,(0,0,0)),(130,200))
        pygame.draw.rect(screen,(0,0,0),(120,260,240,50),2)
        screen.blit(font.render(name,1,(0,0,0)),(130,270))

        for e in pygame.event.get():
            if e.type==pygame.QUIT: return None
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN: return name
                elif e.key==pygame.K_BACKSPACE: name=name[:-1]
                else:
                    if len(name)<12: name+=e.unicode

        pygame.display.update()

def leaderboard_screen(screen):
    data=load_leaderboard()
    font=pygame.font.SysFont(None,35)

    while True:
        screen.fill((255,255,255))
        for i,d in enumerate(data):
            txt=f"{i+1}. {d['name']} - {d['score']}"
            screen.blit(font.render(txt,1,(0,0,0)),(100,100+i*40))

        for e in pygame.event.get():
            if e.type==pygame.QUIT or e.type==pygame.KEYDOWN:
                return

        pygame.display.update()

def settings_screen(screen):
    s=load_settings()
    font=pygame.font.SysFont(None,40)

    while True:
        screen.fill((200,200,200))

        screen.blit(font.render(f"Sound:{s['sound']}",1,(0,0,0)),(120,200))
        screen.blit(font.render(f"Difficulty:{s['difficulty']}",1,(0,0,0)),(120,260))
        screen.blit(font.render("BACK",1,(0,0,0)),(160,350))

        for e in pygame.event.get():
            if e.type==pygame.QUIT: return
            if e.type==pygame.MOUSEBUTTONDOWN:
                _,y=pygame.mouse.get_pos()
                if 200<y<240: s["sound"]=not s["sound"]
                elif 260<y<300:
                    s["difficulty"]="easy" if s["difficulty"]=="hard" else "hard" if s["difficulty"]=="normal" else "normal"
                elif 350<y<400:
                    save_settings(s)
                    return

        pygame.display.update()