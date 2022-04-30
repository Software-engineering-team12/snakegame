import pygame
import random
import SnakeClass

row = col = 40
B_size = 23   # block size


class Apple:
    def __init__(self, position=(30, 30), snake=SnakeClass.Snake):
        self.apple = pygame.image.load("image/grade.png").convert_alpha()
        self.apple = pygame.transform.scale(self.apple, (23, 23))
        self.rect_apple = self.apple.get_rect()                                         # 이미지 크기와 동일한 사각형 객체 생성
        self.rect_apple.x = position[0]
        self.rect_apple.y = position[1]
        self.snake = snake

    def draw(self, screen):
        self.rect_apple.x = B_size*self.rect_apple.x                                    # block size 만큼 곱해서 좌표 변경
        self.rect_apple.y = B_size*self.rect_apple.y
        screen.blit(self.apple, self.rect_apple)
        self.rect_apple.x = self.rect_apple.x / B_size                                  # 다시 block size 만큼 나눠 주기
        self.rect_apple.y = self.rect_apple.y / B_size

    def erase(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.rect_apple.x, self.rect_apple.y, B_size, B_size))

    def move(self):
        flag = True
        while flag:
            self.rect_apple.x = random.randint(0, 39)                                     # 0~39 사이 난수 생성
            self.rect_apple.y = random.randint(0, 39)
            flag = False
            for i in self.snake.bodys:
                if (i.pos[0], i.pos[1]) == self.get_position():                           # 뱀의 위치와 같은 곳에 사과 생성 되면 다시 사과 위치 조정
                    flag = True                                                           # 뱀과 위치 겹치면 while문 반복

    def get_position(self):
        return self.rect_apple.x, self.rect_apple.y

    def set_position(self, position):
        self.rect_apple.x, self.rect_apple.y = position