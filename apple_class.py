import pygame  # 1. pygame 선언
from datetime import datetime
from datetime import timedelta
import random
import time

row = col = 40
B_size = 20   # block size

# 스크린 객체 저장
SCREEN = pygame.display.set_mode((B_size*row, B_size*col))
SCREEN.fill((255, 255, 255))


class Apple:
    def __init__(self, position=(10, 10)):
        self.pos_x = position[0]*B_size
        self.pos_y = position[1]*B_size
        self.apple = pygame.image.load("fruit.png").convert_alpha()
        self.apple = pygame.transform.scale(self.apple, (20, 20))
        self.rect_apple = self.apple.get_rect().move(self.pos_x, self.pos_y)  # 이미지 크기와 동일한 사각형 객체 생성

    # def get_rect(self):

    def draw(self):
        SCREEN.blit(self.apple, self.rect_apple)
"""
    def erase(self):
        pygame.draw.rect(SCREEN, (255, 255, 255), self.rect_apple)
"""


    def position(self):
        self.rect_apple.x = B_size * random.randint(0, 41)
        self.rect_apple.y = B_size * random.randint(0, 41)


# test
pygame.init()
apple = Apple()
apple.draw()
pygame.display.flip()
time.sleep(5)


while True:
    apple.position()
    apple.erase()
    apple.draw()
    pygame.display.flip()
    time.sleep(5)





