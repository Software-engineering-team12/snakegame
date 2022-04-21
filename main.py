import numpy as np
import pygame
import random
from SnakeClass import Snake
from apple_class import Apple


# 윈도우 크기
WIDTH = 500
HEIGHT = 500
# 행과 열의 수
COLUMN = 25
ROW = 25

def drawGrid(screen):
    sizeBtwn = WIDTH // ROW
    x = 0
    y = 0
    for l in range(ROW):
        x = x + sizeBtwn
        y = y + sizeBtwn
        # 그리드 그리기
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, WIDTH)) # 세로 줄
        pygame.draw.line(screen, (0, 0, 0), (0, y), (WIDTH, y)) # 가로 줄


def update():

    screen.fill((255, 255, 255))
    drawGrid(screen)
    snake.draw(screen)
    apple.draw(screen)
    pygame.display.update()


def main():
    global snake,screen,apple

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    snake = Snake((10, 10))
    apple = Apple()

    flag = True
    clock = pygame.time.Clock()


    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        headPos = snake.head.pos
        appPos = apple.get_position()

        if headPos[0] >= ROW or headPos[0] < 0 or headPos[1] >= COLUMN or headPos[1] < 0:
            print("Score:", len(snake.bodys))
            snake.reset((10, 10))
            # flag=  False

        if headPos[0] == appPos[0]//20 and headPos[1] == appPos[1]//20:
            snake.grow()
            apple.move()


        for x in range(1,len(snake.bodys)):
            if headPos[0] == snake.bodys[x].pos[0] and headPos[1] == snake.bodys[x].pos[1] :
                print("Score connected:", len(snake.bodys))
                snake.reset((10,10))
                break



        update()




if __name__ == '__main__':

    main()
    pygame.quit()