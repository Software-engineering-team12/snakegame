import pygame  # 1. pygame 선언
from datetime import datetime
from datetime import timedeltaS
import random

win_size = 1600
low = 40

class Apple:
    def __init__(self, position=(10, 10)):
        self.position = position

    def draw(self):
        apple = pygame.image.load("fruit.png")
        apple = pygame.transform.scale(apple, (40, 40))



