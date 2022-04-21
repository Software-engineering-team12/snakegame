
import random
import pygame

width = 500
height = 500

cols = 20
rows = 20

 ###########################################################지원#######################################################
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
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        """
        dis는 한 큐브와 다음 큐브와의 거리, 여기서는 정사각형을 그리므로 정사각형 한 변의 길이 됨
        x,y 좌표값에 정사각형 한 변의 길이만큼 곱해줘야지 사격형을 그릴 위치가 나온다.
        x,y축정보에 +1과 dis-2를 한 이유는 각 사각형(큐브)끼리 구분이 되게 하려고 그렇게 함 (i*dis, j*dis, 25,25)해도 무방할 것으로 보임
        """

        if eyes:    # 뱀에 눈 그리기
            centre = dis // 2   # 큐브의 중간값 구함
            radius = 3          # 반지름
            circleMiddle = (i * dis + centre - radius, j * dis + 8)     # 왼쪽 눈 위치
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)    # 오른쪽 눈 위치
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)  # 왼쪽 눈 그리기
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)  # 오른쪽 눈 그리기


###########################################################동현##########################################################
class snake():
    body = []   # cube객체의 배열(Snake body의 각 칸)
    turns = {}  # Snake객체의 회전방향을 저장하는 딕셔너리 ( { key = 좌표 : value = 방향 } )

    # 생성자 - 색, 모양, 길이, 방향 초기화
    def __init__(self, color, pos):
        # pos is given as coordinates on the grid ex (1,5) : pos = 시작위치
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    # 방향키를 입력받아 객체를 이동
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                       # 창닫기 버튼 or 커맨드창에 ctrl+c입력시 게임종료...
                pygame.quit()
            keys = pygame.key.get_pressed()                                     # 키보드 입력값을 keys에 저장

            for key in keys:                                                    # 방향키를 입력받아 이동방향을 turns 딕셔너리에 head.pos에 대한 value로 저장
                if keys[pygame.K_LEFT]:                                         # ex) 현재 head의 위치가 (5,7)에서 좌측 방향키가 입력되었다면
                    self.dirnx = -1                                             # turns = { [5,7] : [-1, 0] }
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

        for i, c in enumerate(self.body):                                       # body의 길이만큼 반복
            p = c.pos[:]
            if p in self.turns:                                                 # p로 참조하는 cube의 위치가 turns 딕셔너리에 저장된 key값일 때
                turn = self.turns[p]                                            # key값에 따른 value값으로 회전
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:                                     # body의 마지막 cube까지 회전을 마쳤다면
                    self.turns.pop(p)                                           # turns 딕셔너리에서 그 좌표에서의 회전방향을 지움
            else:
                c.move(c.dirnx, c.dirny)                                        # 회전방향이 없는 다른좌표면 진행방향대로 이동

    # Snake객체 초기화 (게임오버시) - init과 동일
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    # Snake 객체가 snack을 먹으면 body의 길이를 늘림
    def addCube(self):
        tail = self.body[-1]                                                    # body의 마지막 cube를 tail이라고 선언
        dx, dy = tail.dirnx, tail.dirny                                         # tail의 방향을 불러옴

        if dx == 1 and dy == 0:                                                 # tail의 방향에 따라 새로 추가되는 cube의 위치가 달라짐
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx                                                # 새로 추가된 cube의 방향을 tail의 방향으로 설정
        self.body[-1].dirny = dy

    #Snake객체 그리기 (surface = 배경객체)
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:                                                          # 첫번째 body(=head)에는 눈을 그림
                c.draw(surface, True)
            else:
                c.draw(surface)

###########################################################찬영##########################################################

def redrawWindow():
    global win
    #배경 색깔 설정(현재:검정)
    win.fill((0, 0, 0))
    # 그리드 그리기
    drawGrid(width, rows, win)
    # s(뱀) 그리기
    s.draw(win)
    # snack(스낵) 그리기
    snack.draw(win)
    #윈도우 업데이트
    pygame.display.update()
    pass


#width, rows, window를 매개변수로 받아 그리드 그리기
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        # 그리드 그리기
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w)) # 세로 줄
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y)) # 가로 줄

#랜덤하게 과자 위치 생성하기
def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1, rows - 1)
        y = random.randrange(1, rows - 1)
        # 단, 스낵의 위치가 현재 뱀의 몸통이 위치하고 있는 곳은 제외
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def main():
    #s: 뱀, snack: 과자, win: 스크린 객체
    global s, snack, win
    #스크린 객체 생성
    win = pygame.display.set_mode((width, height))
    # 뱀 객체 생성,(255,0,0)-> 빨강, (10,10)-> 현재 위치 x = 10 ,y = 10
    s = snake((255, 0, 0), (10, 10))
    s.addCube()
    # 과자 객체 생성, randomSnack 이용하여 random한 위치에 생성.
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))

    #게임 종료 신호
    flag = True

    #fps 설정 10fps
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        #현재 머리의 위치
        headPos = s.head.pos
        #머리가 벽에 닿는 경우 처리
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            #현재 스코어 출력
            print("Score:", len(s.body))
            #리셋하고 다시 시작
            s.reset((10, 10))
        #머리가 과자를 먹은 경우 처리
        if s.body[0].pos == snack.pos:
            #뱀의 큐브 추가
            s.addCube()
            #새로운 과자 생성
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            #뱀이 자기 자신과 닿은 경우 처리
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print("Score:", len(s.body))
                s.reset((10, 10))
                break

        redrawWindow()


main()