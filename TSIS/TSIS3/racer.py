import pygame, random, time
from persistence import save_score, load_settings

WIDTH, HEIGHT = 480,720

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("assets/player.png")
        self.rect=self.image.get_rect(center=(WIDTH//2,HEIGHT-100))
        self.speed=5
        self.shield=False

    def move(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left>0:
            self.rect.move_ip(-self.speed,0)
        if keys[pygame.K_RIGHT] and self.rect.right<WIDTH:
            self.rect.move_ip(self.speed,0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,player,speed):
        super().__init__()
        self.image=pygame.image.load("assets/enemy.png")

        while True:
            x=random.randint(40,WIDTH-40)
            if abs(x-player.rect.centerx)>100:
                break

        self.rect=self.image.get_rect(center=(x,-50))
        self.speed=speed

    def move(self):
        self.rect.move_ip(0,self.speed)
        if self.rect.top>HEIGHT:
            self.rect.top=-50
            self.rect.centerx=random.randint(40,WIDTH-40)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img=pygame.image.load("assets/coin.png")
        self.image=pygame.transform.scale(img,(30,30))
        self.rect=self.image.get_rect(center=(random.randint(40,WIDTH-40),-50))
        self.value=random.choice([1,3,5])

    def move(self):
        self.rect.move_ip(0,4)
        if self.rect.top>HEIGHT:
            self.respawn()

    def respawn(self):
        self.rect.top=-50
        self.rect.centerx=random.randint(40,WIDTH-40)
        self.value=random.choice([1,3,5])

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.type=random.choice(["barrier","oil"])
        self.image=pygame.Surface((40,40))
        self.image.fill((100,100,100) if self.type=="barrier" else (0,0,0))

        while True:
            x=random.randint(40,WIDTH-40)
            if abs(x-player.rect.centerx)>100:
                break

        self.rect=self.image.get_rect(center=(x,-50))

    def move(self):
        self.rect.move_ip(0,5)
        if self.rect.top>HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.type=random.choice(["nitro","shield","repair"])
        self.image=pygame.Surface((30,30),pygame.SRCALPHA)

        color=(255,0,0) if self.type=="nitro" else (0,0,255) if self.type=="shield" else (0,255,0)
        pygame.draw.circle(self.image,color,(15,15),15)

        while True:
            x=random.randint(40,WIDTH-40)
            if abs(x-player.rect.centerx)>100:
                break

        self.rect=self.image.get_rect(center=(x,-50))

    def move(self):
        self.rect.move_ip(0,4)
        if self.rect.top>HEIGHT:
            self.kill()

def run_game(screen,username):
    settings=load_settings()

    base_speed=4 if settings["difficulty"]=="easy" else 7 if settings["difficulty"]=="hard" else 5

    bg=pygame.transform.scale(pygame.image.load("assets/animatedstreet.png"),(WIDTH,HEIGHT))

    if settings["sound"]:
        pygame.mixer.music.load("assets/background.wav")
        pygame.mixer.music.play(-1)
        crash=pygame.mixer.Sound("assets/crash.wav")
    else:
        crash=None

    player=Player()
    enemies=pygame.sprite.Group(Enemy(player,base_speed))
    coins=pygame.sprite.Group(Coin())
    obstacles=pygame.sprite.Group()
    powerups=pygame.sprite.Group()

    all_sprites=pygame.sprite.Group(player,*enemies,*coins)

    score=0
    coins_count=0
    distance=0
    lives=1
    last_hit=0

    active_power=None
    power_timer=0

    clock=pygame.time.Clock()

    while True:
        screen.blit(bg,(0,0))

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                return

        player.move()

        for e in enemies:
            e.speed=base_speed+distance//500

        if len(enemies)<1+distance//600:
            new=Enemy(player,base_speed)
            enemies.add(new)
            all_sprites.add(new)

        if random.randint(0,1000)<(5+distance//300):
            ob=Obstacle(player)
            obstacles.add(ob)
            all_sprites.add(ob)

        if random.randint(0,1000)<4:
            p=PowerUp(player)
            powerups.add(p)
            all_sprites.add(p)

        for e in enemies: e.move()
        for c in coins: c.move()
        for o in obstacles: o.move()
        for p in powerups: p.move()

        # coins
        hit=pygame.sprite.spritecollideany(player,coins)
        if hit:
            coins_count+=hit.value
            score+=hit.value*10
            hit.respawn()

        # powerups
        hit=pygame.sprite.spritecollideany(player,powerups)
        if hit:
            active_power=None

            if hit.type=="nitro":
                active_power="nitro"
                power_timer=time.time()
            elif hit.type=="shield":
                player.shield=True
            elif hit.type=="repair":
                lives+=1

            hit.kill()

        if active_power=="nitro":
            player.speed=8
            if time.time()-power_timer>4:
                player.speed=5
                active_power=None

        # collision
        if pygame.sprite.spritecollideany(player,enemies) or pygame.sprite.spritecollideany(player,obstacles):
            now=time.time()
            if now-last_hit>1:
                last_hit=now

                if player.shield:
                    player.shield=False
                elif lives>0:
                    lives-=1
                else:
                    if settings["sound"]:
                        crash.play()
                        time.sleep(1)
                    save_score(username,score,distance)
                    return

        distance+=1

        for s in all_sprites:
            screen.blit(s.image,s.rect)

        font=pygame.font.SysFont(None,25)
        screen.blit(font.render(f"Score:{score}",1,(0,0,0)),(10,10))
        screen.blit(font.render(f"Coins:{coins_count}",1,(0,0,0)),(10,30))
        screen.blit(font.render(f"Dist:{distance}",1,(0,0,0)),(10,50))
        screen.blit(font.render(f"Lives:{lives}",1,(0,0,0)),(10,70))

        if active_power:
            screen.blit(font.render(f"{active_power}",1,(255,0,0)),(350,10))

        pygame.display.update()
        clock.tick(60)