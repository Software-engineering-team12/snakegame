import pygame
import random
import time

row = col = 40
B_size = 20   # block size

# 스크린 객체 저장
screen = pygame.display.set_mode((B_size*row, B_size*col))
# screen_rect = screen.get_rect()
# screen.fill((255, 255, 255))
cover = pygame.Surface(screen.get_size())
cover = cover.convert()
cover.fill((255, 255, 255))
screen.blit(cover, (0, 0))


class Apple:
    def __init__(self, position=(10, 10)):
        self.apple = pygame.image.load("fruit.png").convert_alpha()
        self.apple = pygame.transform.scale(self.apple, (20, 20))
        self.rect_apple = self.apple.get_rect() # 이미지 크기와 동일한 사각형 객체 생성
        self.rect_apple.x = position[0]*B_size
        self.rect_apple.y = position[1]*B_size

    # def get_rect(self):

    def draw(self):
        screen.blit(self.apple, self.rect_apple)

    def erase(self):
        screen.blit(cover, (0, 0))

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





