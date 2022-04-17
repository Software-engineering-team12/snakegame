import pygame  # 1. pygame 선언
from datetime import datetime
from datetime import timedelta
import random

pygame.init()  # 2. pygame 초기화

# 3. pygame에 사용되는 전역변수 선언
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

width = 400
height = 400
cols = rows = 20
screen = pygame.display.set_mode((width,height))


done = False
clock = pygame.time.Clock()
last_moved_time = datetime.now()

KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}


def draw_block(screen, color, position):
    block = pygame.Rect((position[0] * rows, position[1] * rows),
                        (rows, rows))
    pygame.draw.rect(screen, color, block)


class Snake:
    def __init__(self):
        self.positions = [(10,10)]  # 초기 뱀의 위치
        self.direction = ''

    def draw(self):
        for position in self.positions:
            draw_block(screen, GREEN, position)

    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'W':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'N':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(y, x + 1)] + self.positions[:-1]

    def grow(self):
        tail_position = self.positions[-1]
        x, y = tail_position
        if self.direction == 'N':
            self.positions.append((x, y + 1))
        elif self.direction == 'S':
            self.positions.append((x, y - 1))
        elif self.direction == 'W':
            self.positions.append((x + 1, y))
        elif self.direction == 'E':
            self.positions.append((x - 1, y))


    def reset(self):
            self.positions = [(10,10)]  # 초기 뱀의 위치
            self.direction = 'E'


class Apple:
    def __init__(self, position=(10, 10)):
        self.position = position
        #self.pos_x = position[0]
        #self.pos_y = position[1]

    def draw(self):
        apple = pygame.image.load("fruit.png")
        apple = pygame.transform.scale(apple, (40, 40))
        screen.blit(apple, [40*self.position[0], 40*self.position[1]])


def randomSnack(rows, item):
    positions = item.positions

    while True:
        x = random.randrange(1, rows - 1)
        y = random.randrange(1, rows - 1)
        # 단, 스낵의 위치가 현재 뱀의 몸통이 위치하고 있는 곳은 제외
        if len(list(filter(lambda z: z == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


#width, rows, window를 매개변수로 받아 그리드 그리기
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    screen.fill((0,0,0))
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        # 그리드 그리기
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w)) # 세로 줄
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y)) # 가로 줄


# 4. pygame 무한루프
def runGame():
    global done, last_moved_time
    # 게임 시작 시, 뱀과 사과를 초기화
    snake = Snake()
    apple = Apple()

    while not done:

        clock.tick(10)
        print(snake.positions)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        if timedelta(seconds=0.5) <= datetime.now() - last_moved_time:
            snake.move()

        headPos = snake.positions[0]
        if headPos[0] >= rows or headPos[0] < 0 or headPos[1] >= rows or headPos[1] < 0:
            #현재 스코어 출력
            print("Score:", len(snake.positions))
            #리셋하고 다시 시작
            snake.reset()


        if headPos[0] == apple.position[0] and headPos[1] == apple.position[1]:
            snake.grow()
            # 새로운 과자 생성
            apple = Apple(randomSnack(rows, snake))

        for x in range(len(snake.positions)):
            #뱀이 자기 자신과 닿은 경우 처리
            if snake.positions[x] in list(map(lambda z: z, snake.positions[x + 1:])):
                print("Score:", len(snake.positions))
                snake.reset()
                break

        drawGrid(width, rows, screen)
        snake.draw()
        apple.draw()

        pygame.display.update()


runGame()
pygame.quit()