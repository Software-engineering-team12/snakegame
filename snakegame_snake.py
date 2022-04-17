import pygame  # 1. pygame 선언
from datetime import datetime
from datetime import timedelta
import random
import time

win_size = 1600
row = col = 40

# 스크린 객체 저장
SCREEN = pygame.display.set_mode((row, col))
SCREEN.fill((255, 255, 255))


class Apple:
    def __init__(self, position=(100, 100)):
        self.pos_x = position[0]
        self.pos_y = position[1]

    def draw(self):
        apple = pygame.image.load("fruit.png")
        apple = pygame.transform.scale(apple, (40, 40))
        SCREEN.blit(apple, [self.pos_x, self.pos_y])


apple = Apple()
apple.draw()
pygame.display.flip()

time.sleep(100)





