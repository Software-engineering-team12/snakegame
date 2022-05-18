# Snake Class
import pygame
import numpy as np


B_size = 20

DIRECTION = {
    'u': np.array([0, -1]),
    'd': np.array([0, 1]),
    'r': np.array([1, 0]),
    'l': np.array([-1, 0])
}


class Snake:


    # Body클래스는 뱀의 몸통 한칸을 뜻하며 위치와 방향을 가지고 있다.
    class Body:
        def __init__(self, position, direction=DIRECTION['u']):
            self.pos = position
            self.direction = direction

    # 생성자 : 뱀의 머리와 꼬리를 생성한다. 초기상태에서 뱀의 머리와 꼬리는 일치한다.
    def __init__(self, game, position=np.array([20, 20]), dir=DIRECTION['u'], player=0):
        self.bodys = []
        self.turns = {}
        self.key = dir
        self.game = game
        self.player = player
        self.head = Snake.Body(position, dir)
        self.bodys.append(self.head)
        self.tail = self.bodys[-1]
        self.load_img(self.player)

    # load_img메소드는 snake의 머리, 몸통, 꼬리에 해당하는 이미지파일을 불러온다
    def load_img(self, player):
        if player == 0:
            self.head_up = pygame.image.load("img/head_up.png").convert_alpha()
            self.head_up = pygame.transform.scale(self.head_up, (20, 20))
            self.head_down = pygame.image.load("img/head_down.png").convert_alpha()
            self.head_down = pygame.transform.scale(self.head_down, (20, 20))
            self.head_left = pygame.image.load("img/head_left.png").convert_alpha()
            self.head_left = pygame.transform.scale(self.head_left, (20, 20))
            self.head_right = pygame.image.load("img/head_right.png").convert_alpha()
            self.head_right = pygame.transform.scale(self.head_right, (20, 20))

            self.tail_up = pygame.image.load("img/tail_up.png").convert_alpha()
            self.tail_up = pygame.transform.scale(self.tail_up, (20, 20))
            self.tail_down = pygame.image.load("img/tail_down.png").convert_alpha()
            self.tail_down = pygame.transform.scale(self.tail_down, (20, 20))
            self.tail_left = pygame.image.load("img/tail_left.png").convert_alpha()
            self.tail_left = pygame.transform.scale(self.tail_left, (20, 20))
            self.tail_right = pygame.image.load("img/tail_right.png").convert_alpha()
            self.tail_right = pygame.transform.scale(self.tail_right, (20, 20))

            self.body_image = pygame.image.load("img/body.png").convert_alpha()
            self.body_image = pygame.transform.scale(self.body_image, (20, 20))
            self.rect_snake = self.body_image.get_rect()

        if player == 1:
            self.head_up = pygame.image.load("img/head_up1.png").convert_alpha()
            self.head_up = pygame.transform.scale(self.head_up, (20, 20))
            self.head_down = pygame.image.load("img/head_down1.png").convert_alpha()
            self.head_down = pygame.transform.scale(self.head_down, (20, 20))
            self.head_left = pygame.image.load("img/head_left1.png").convert_alpha()
            self.head_left = pygame.transform.scale(self.head_left, (20, 20))
            self.head_right = pygame.image.load("img/head_right1.png").convert_alpha()
            self.head_right = pygame.transform.scale(self.head_right, (20, 20))
            self.tail_up = pygame.image.load("img/grade.png").convert_alpha()
            self.tail_up = pygame.transform.scale(self.tail_up, (20, 20))
            self.tail_down = pygame.image.load("img/grade.png").convert_alpha()
            self.tail_down = pygame.transform.scale(self.tail_down, (20, 20))
            self.tail_left = pygame.image.load("img/grade.png").convert_alpha()
            self.tail_left = pygame.transform.scale(self.tail_left, (20, 20))
            self.tail_right = pygame.image.load("img/grade.png").convert_alpha()
            self.tail_right = pygame.transform.scale(self.tail_right, (20, 20))

            self.body_image = pygame.image.load("img/grade.png").convert_alpha()
            self.body_image = pygame.transform.scale(self.body_image, (20, 20))
            self.rect_snake = self.body_image.get_rect()

        if player == 2:
            self.head_up = pygame.image.load("img/head_up2.png").convert_alpha()
            self.head_up = pygame.transform.scale(self.head_up, (20, 20))
            self.head_down = pygame.image.load("img/head_down2.png").convert_alpha()
            self.head_down = pygame.transform.scale(self.head_down, (20, 20))
            self.head_left = pygame.image.load("img/head_left2.png").convert_alpha()
            self.head_left = pygame.transform.scale(self.head_left, (20, 20))
            self.head_right = pygame.image.load("img/head_right2.png").convert_alpha()
            self.head_right = pygame.transform.scale(self.head_right, (20, 20))
            self.tail_up = pygame.image.load("img/grade.png").convert_alpha()
            self.tail_up = pygame.transform.scale(self.tail_up, (20, 20))
            self.tail_down = pygame.image.load("img/grade.png").convert_alpha()
            self.tail_down = pygame.transform.scale(self.tail_down, (20, 20))
            self.tail_left = pygame.image.load("img/grade.png").convert_alpha()
            self.tail_left = pygame.transform.scale(self.tail_left, (20, 20))
            self.tail_right = pygame.image.load("img/grade.png").convert_alpha()
            self.tail_right = pygame.transform.scale(self.tail_right, (20, 20))

            self.body_image = pygame.image.load("img/grade.png").convert_alpha()
            self.body_image = pygame.transform.scale(self.body_image, (20, 20))
            self.rect_snake = self.body_image.get_rect()

    # reset 메소드에서는 게임을 다시 시작할 때 뱀을 초기상태로 되돌린다.
    def reset(self, position, dir = DIRECTION['u']):
        self.bodys = []
        self.turns = {}
        self.head = Snake.Body(position, dir)
        self.bodys.append(self.head)
        self.tail = self.bodys[-1]

    # move 메소드에서는 키보드 입력을 받아 뱀을 움직인다.
    def move_1P(self):
        if self.game.UP_KEY:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['u']
            self.key = DIRECTION['u']
        elif self.game.DOWN_KEY:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['d']
            self.key = DIRECTION['d']
        elif self.game.LEFT_KEY:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['l']
            self.key = DIRECTION['l']
        elif self.game.RIGHT_KEY:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['r']
            self.key = DIRECTION['r']

        for i, bloc in enumerate(self.bodys):
            p = bloc.pos[:]
            d = bloc.direction
            if tuple(p) in self.turns:
                bloc.pos = p + self.turns[tuple(p)]
                bloc.direction = self.turns[tuple(p)]
                if i == len(self.bodys) - 1:
                    self.turns.pop(tuple(p))
            else:
                bloc.pos = p + d

    def move_2P(self):
        if self.game.W_KEY:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['u']
            self.key = DIRECTION['u']
        elif self.game.S_KEY:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['d']
            self.key = DIRECTION['d']
        elif self.game.A_KEY:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['l']
            self.key = DIRECTION['l']
        elif self.game.D_KEY:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['r']
            self.key = DIRECTION['r']

        for i, bloc in enumerate(self.bodys):
            p = bloc.pos[:]
            d = bloc.direction
            if tuple(p) in self.turns:
                bloc.pos = p + self.turns[tuple(p)]
                bloc.direction = self.turns[tuple(p)]
                if i == len(self.bodys) - 1:
                    self.turns.pop(tuple(p))
            else:
                bloc.pos = p + d

    # grow 메소드에서는 뱀이 사과를 먹으면 길이가 늘어나는 행동을 취한다.
    def grow(self):
        self.bodys.append(Snake.Body(self.tail.pos - self.tail.direction, self.tail.direction))
        self.tail = self.bodys[-1]

    # draw 메소드에서는 bodys의 각각의 요소들의 위치를 참고하여 창에 뱀을 그린다.
    def draw(self, screen):
        for i, bloc in enumerate(self.bodys):
            self.rect_snake.x = B_size * bloc.pos[0]                                                        # 그려야하는 좌표의 위치에 snake1 이미지 사이즈만큼의 사각형 객체 생성
            self.rect_snake.y = B_size * bloc.pos[1]
            if i == 0:                                                                                      # 머리 부분 일 떄
                if np.array_equiv(bloc.direction, DIRECTION['u']):
                    screen.blit(self.head_up, self.rect_snake)
                elif np.array_equiv(bloc.direction, DIRECTION['d']):
                    screen.blit(self.head_down, self.rect_snake)
                elif np.array_equiv(bloc.direction, DIRECTION['l']):
                    screen.blit(self.head_left, self.rect_snake)
                elif np.array_equiv(bloc.direction, DIRECTION['r']):
                    screen.blit(self.head_right, self.rect_snake)

            elif i == self.bodys.index(self.tail):                                                          # 꼬리 부분 일 떄
                if np.array_equiv(bloc.direction, DIRECTION['u']):
                    screen.blit(self.tail_up, self.rect_snake)
                elif np.array_equiv(bloc.direction, DIRECTION['d']):
                    screen.blit(self.tail_down, self.rect_snake)
                elif np.array_equiv(bloc.direction, DIRECTION['l']):
                    screen.blit(self.tail_left, self.rect_snake)
                elif np.array_equiv(bloc.direction, DIRECTION['r']):
                    screen.blit(self.tail_right, self.rect_snake)

            else:                                                                                           # 몸통 부분일 때
                screen.blit(self.body_image, self.rect_snake)

    def set_body(self, save_body):
        h = save_body.pop(0)
        head = Snake.Body(np.array([h[0], h[1]]), np.array([h[2], h[3]]))
        self.bodys[0] = head
        self.head = self.bodys[0]
        self.tail = self.bodys[-1]

        for i in save_body:
            self.grow()
