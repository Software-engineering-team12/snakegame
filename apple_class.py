import pygame
import random
import time

row = col = 40
B_size = 20   # block size

# 스크린 객체 저장
# screen = pygame.display.set_mode((B_size*row, B_size*col))
# screen.fill((255, 255, 255))

#draw,erase메서드에 screen 매개변수 추가
class Apple:
    def __init__(self, position=(30, 30)):
        self.apple = pygame.image.load("image/fruit.png").convert_alpha()
        self.apple = pygame.transform.scale(self.apple, (20, 20))
        self.rect_apple = self.apple.get_rect()  # 이미지 크기와 동일한 사각형 객체 생성
        self.rect_apple.x = position[0]
        self.rect_apple.y = position[1]

    def draw(self, screen):
        self.rect_apple.x = B_size*self.rect_apple.x    # block size 만큼 곱해서 좌표 변경
        self.rect_apple.y = B_size*self.rect_apple.y
        screen.blit(self.apple, self.rect_apple)
        self.rect_apple.x = self.rect_apple.x / B_size    # 다시 block size 만큼 나눠 주기
        self.rect_apple.y = self.rect_apple.y / B_size

    def erase(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect_apple.x, self.rect_apple.y, B_size, B_size))

    def move(self):
        self.rect_apple.x = random.randint(1, 41)
        self.rect_apple.y = random.randint(1, 41)

    def get_position(self):
        return self.rect_apple.x, self.rect_apple.y


# test
# pygame.init()
# apple = Apple()
# apple.draw()
# pygame.display.flip()
# time.sleep(5)
#
# while True:
#     apple.erase()
#     apple.move()
#     apple.draw()
#     pygame.display.flip()
#     time.sleep(5)
#
#
#


