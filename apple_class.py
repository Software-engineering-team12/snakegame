import pygame
import random
import time

row = col = 40
B_size = 20   # block size

# 스크린 객체 저장
screen = pygame.display.set_mode((B_size*row, B_size*col))
screen.fill((255, 255, 255))


class Apple:
    def __init__(self, position=(10, 10)):
        self.apple = pygame.image.load("fruit.png").convert_alpha()
        self.apple = pygame.transform.scale(self.apple, (20, 20))
        self.rect_apple = self.apple.get_rect()  # 이미지 크기와 동일한 사각형 객체 생성
        self.rect_apple.x = position[0]*B_size
        self.rect_apple.y = position[1]*B_size

    def draw(self):
        screen.blit(self.apple, self.rect_apple)

    def erase(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect_apple.x, self.rect_apple.y, B_size, B_size))

    def move(self):
        self.rect_apple.x = B_size * random.randint(0, 41)
        self.rect_apple.y = B_size * random.randint(0, 41)

    def get_position(self):
        return self.rect_apple.x, self.rect_apple.y


# test
pygame.init()
apple = Apple()
apple.draw()
pygame.display.flip()
time.sleep(5)

while True:
    apple.erase()
    apple.move()
    apple.draw()
    pygame.display.flip()
    time.sleep(5)





