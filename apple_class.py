import pygame  # 1. pygame 선언
from datetime import datetime
from datetime import timedelta
import random
import time

WIN_SIZE = (40*20)**2
row = col = 40
B_size = WIN_SIZE // row   # block size

# 스크린 객체 저장
SCREEN = pygame.display.set_mode((B_size*row, B_size*col))
SCREEN.fill((255, 255, 255))


class Apple:
    def __init__(self, position=(B_size*10, B_size*10)):
        self.pos_x = position[0]
        self.pos_y = position[1]

    def draw(self):
        apple = pygame.image.load("fruit.png")
        apple = pygame.transform.scale(apple, (25, 25))
        SCREEN.blit(apple, [self.pos_x, self.pos_y])

    def position(self):
        self.pos_x = random.randint(0, 41)
        self.pos_y = random.randint(0, 41)


apple = Apple()
apple.draw()
pygame.display.flip()

time.sleep(100)





