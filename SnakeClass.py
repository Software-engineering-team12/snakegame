# Snake Class
import pygame
import numpy as np

B_size = 18

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
    def __init__(self, game, position=np.array([18, 18]), dir=DIRECTION['u'], player=1):
        self.bodys = []
        self.turns = {}
        self.key = dir
        self.game = game
        self.player = player
        self.head = Snake.Body(position, dir)
        self.bodys.append(self.head)
        self.tail = self.bodys[-1]
        self.load_img(self.player)
        self.last_key = None

    # load_img메소드는 snake의 머리, 몸통, 꼬리에 해당하는 이미지파일을 불러온다
    def load_img(self, player):
        self.head_up = pygame.image.load("img/head_up"+str(player)+".png").convert_alpha()
        self.head_up = pygame.transform.scale(self.head_up, (18, 18))
        self.head_down = pygame.image.load("img/head_down"+str(player)+".png").convert_alpha()
        self.head_down = pygame.transform.scale(self.head_down, (18, 18))
        self.head_left = pygame.image.load("img/head_left"+str(player)+".png").convert_alpha()
        self.head_left = pygame.transform.scale(self.head_left, (18, 18))
        self.head_right = pygame.image.load("img/head_right"+str(player)+".png").convert_alpha()
        self.head_right = pygame.transform.scale(self.head_right, (18, 18))

        self.body_image = pygame.image.load("img/grade.png").convert_alpha()
        self.body_image = pygame.transform.scale(self.body_image, (18, 18))
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
        if self.game.UP_KEY and self.last_key != pygame.K_DOWN:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['u']
            self.key = DIRECTION['u']
            self.last_key = pygame.K_UP
        elif self.game.DOWN_KEY and self.last_key != pygame.K_UP:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['d']
            self.key = DIRECTION['d']
            self.last_key = pygame.K_DOWN
        elif self.game.LEFT_KEY and self.last_key != pygame.K_RIGHT:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['l']
            self.key = DIRECTION['l']
            self.last_key = pygame.K_LEFT
        elif self.game.RIGHT_KEY and self.last_key != pygame.K_LEFT:
            self.turns[tuple(self.head.pos[:])] = DIRECTION['r']
            self.key = DIRECTION['r']
            self.last_key = pygame.K_RIGHT

        self.move()

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

        self.move()

    def move(self):
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
            self.rect_snake.x = B_size * bloc.pos[0]                              # 그려야하는 좌표의 위치에 snake1 이미지 사이즈만큼의 사각형 객체 생성
            self.rect_snake.y = B_size * bloc.pos[1]
            if i == 0:                                                             # 머리 부분 일 떄
                if np.array_equiv(bloc.direction, DIRECTION['u']):
                    screen.blit(self.head_up, self.rect_snake)
                elif np.array_equiv(bloc.direction, DIRECTION['d']):
                    screen.blit(self.head_down, self.rect_snake)
                elif np.array_equiv(bloc.direction, DIRECTION['l']):
                    screen.blit(self.head_left, self.rect_snake)
                elif np.array_equiv(bloc.direction, DIRECTION['r']):
                    screen.blit(self.head_right, self.rect_snake)
            else:  # 몸통 부분일 때
                screen.blit(self.body_image, self.rect_snake)

    def set_body(self, save_body):
        h = save_body.pop(0)
        head = Snake.Body(np.array([h[0], h[1]]), np.array([h[2], h[3]]))
        self.bodys[0] = head
        self.head = self.bodys[0]
        self.tail = self.bodys[-1]
        for i in save_body:
            self.grow()
