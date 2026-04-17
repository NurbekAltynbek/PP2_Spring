import pygame
import datetime
import math


class MickeyClock:
    def __init__(self):
        self.width = 800
        self.height = 600

        self.center = (400, 300)

        self.background = pygame.image.load("images/mickeyclock.jpeg").convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def get_time(self):
        now = datetime.datetime.now()
        return now.minute, now.second

    def draw_hand(self, screen, angle_deg, length, width):
        angle_rad = math.radians(angle_deg - 90)

        end_x = self.center[0] + length * math.cos(angle_rad)
        end_y = self.center[1] + length * math.sin(angle_rad)

        pygame.draw.line(screen, (0, 0, 0), self.center, (end_x, end_y), width)

    def draw(self, screen):
        minutes, seconds = self.get_time()

        minute_angle = minutes * 6
        second_angle = seconds * 6

        screen.blit(self.background, (0, 0))

        # минутная стрелка
        self.draw_hand(screen, minute_angle, 140, 8)

        # секундная стрелка
        self.draw_hand(screen, second_angle, 180, 4)

        # центр часов
        pygame.draw.circle(screen, (0, 0, 0), self.center, 10)