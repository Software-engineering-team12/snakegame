
import random
import pygame

width = 500
height = 500

cols = 25
rows = 20

###########################################################지원##########################################################
class cube():
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start                            # 일단 현재 위치 start 초기화
        self.dirnx = dirnx                          # x방향 이동 -  입력 받은 매개 별수로 지정(기본값 1)
        self.dirny = dirny  # "L", "R", "U", "D"    # y방향 이동 - 입력 받은 매개 변수로 지정(기본값 0)
        self.color = color                          # 색 설정 - 입력 받은 매개 변수로 지정(기본값 red)

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
        """
        현재 큐브의 위치를 나타 내는 pos
        pos[0]에는 큐브의 x축 좌표 정보
        pos[1]에는 큐브의 y축 좌표 정보 
        원하는 만큼 큐브의 위치를 이동 시킬 떄 move(x축 이동량,y축 이동량) 사용 
         - 큐브의 다음 위치 pos = pos[x좌표]+ x축 이동량, pos[y좌표] + y축 이동량 됨
        """

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows   # 각 큐브의 width / height - 여기서는 500//20 ->25
        i = self.pos[0]             # 현재 큐브의 x좌표
        j = self.pos[1]             # 현재 큐브의 y좌표

        # pygame.draw.rect(화면 선언한 변수 값, 색, (사각형의 x축, y축, 가로, 세로))
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2 ))
        """
        dis는 한 큐브와 다음 큐브와의 거리, 여기서는 정사각형을 그리므로 정사각형 한 변의 길이 됨
        x,y 좌표값에 정사각형 한 변의 길이만큼 곱해줘야지 사격형을 그릴 위치가 나온다.
        x,y축정보에 +1과 dis-2를 한 이유는 각 사각형(큐브)끼리 구분이 되게 하려고 그렇게 함 (i*dis, j*dis, 25,25)해도 무방할 것으로 보임
        """

        if eyes:   # 뱀에 눈 그리기
            centre = dis // 2    # 큐브의 중간값 구함
            radius = 3           # 반지름
            circleMiddle = (i * dis + centre - radius, j * dis + 8)    # 왼쪽 눈 위치
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)   # 오른쪽 눈 위치
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)  # 왼쪽 눈 그리기
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)  # 오른쪽 눈 그리기


###########################################################동현##########################################################
class snake():
    body = []
    turns = {}

    def __init__(self, color, pos):
        # pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

###########################################################찬영##########################################################
def redrawWindow():
    global win
    win.fill((0, 0, 0))
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()
    pass


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1, rows - 1)
        y = random.randrange(1, rows - 1)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def main():
    global s, snack, win
    win = pygame.display.set_mode((width, height))
    s = snake((255, 0, 0), (10, 10))
    s.addCube()
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        headPos = s.head.pos
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            print("Score:", len(s.body))
            s.reset((10, 10))

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print("Score:", len(s.body))
                s.reset((10, 10))
                break

        redrawWindow()


main()