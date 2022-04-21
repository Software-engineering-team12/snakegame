# Snake Class
import pygame
import numpy as np

row = col = 40
B_size = 20   # block size

KEY = {
    'UP' : pygame.K_UP ,
    'DOWN' : pygame.K_DOWN,
    'LEFT' : pygame.K_LEFT,
    'RIGHT' : pygame.K_RIGHT,
    'ESC' : pygame.K_ESCAPE,
}

DIRECTION = {
    'u' : np.array([0, -1]),
    'd' : np.array([0, 1]),
    'r' : np.array([1, 0]),
    'l' : np.array([-1, 0])
}


class Snake :
    bodys = []
    turns = {}
    
    #Body클래스는 뱀의 몸통 한칸을 뜻하며 위치와 방향을 가지고 있다.
    class Body :
        def __init__(self, position, direction = DIRECTION['u']) : 
            self.pos = position
            self.direction = direction

    #생성자 : 뱀의 머리와 꼬리를 생성한다. 초기상태에서 뱀의 머리와 꼬리는 일치한다.
    def __init__(self, position = np.array([20, 20])):
        self.head = Snake.Body(position)
        self.bodys.append(self.head)
        self.tail = self.bodys[-1]
        self.head_image = pygame.image.load("image/head.png").convert_alpha()
        self.head_image = pygame.transform.scale(self.head_image, (20, 20))
        self.body_image = pygame.image.load("image/body.png").convert_alpha()
        self.body_image = pygame.transform.scale(self.body_image, (20, 20))
        self.rect_snake = self.head_image.get_rect()  # 이미지 크기와 동일한 사각형 객체 생성

    #reset 메소드에서는 게임을 다시 시작할 때 뱀을 초기상태로 되돌린다.
    def reset(self, position):
        self.bodys = []
        self.turns = {}
        self.head = Snake.Body(position)
        self.bodys.append(self.head)
        self.tail = self.bodys[-1]

    #move 메소드에서는 키보드 입력을 받아 뱀을 움직인다.
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            #elif event.type == KEY['ESC'] :
                #show_ingame_menu
            #    pass
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[ KEY['UP'] ]:
                    self.turns[ tuple(self.head.pos[:]) ] = DIRECTION['u']
                elif keys[ KEY['DOWN'] ] :
                    self.turns[ tuple(self.head.pos[:]) ] = DIRECTION['d']
                elif keys[ KEY['LEFT'] ] :
                    self.turns[ tuple(self.head.pos[:]) ] = DIRECTION['l']
                elif keys[ KEY['RIGHT'] ] :
                    self.turns[ tuple(self.head.pos[:]) ] = DIRECTION['r']
                
        for i, bloc in enumerate(self.bodys):
            p = bloc.pos[:]
            d = bloc.direction
            if tuple(p) in self.turns:
                bloc.pos = p + self.turns[tuple(p)]
                bloc.direction = self.turns[tuple(p)]
                if i == len(self.bodys) - 1:
                    self.turns.pop(tuple(p))
            else :
                bloc.pos = p + d


    #main함수에서 grow 함수 동작시 문제 발생하여 주석 처리 해놨습니다.
    #grow 메소드에서는 뱀이 사과를 먹으면 길이가 늘어나는 행동을 취한다. 참고한 코드와 다르게 현재 꼬리자리에 몸통을 한칸 만들고 꼬리를 진행방행과 반대 방향으로 한칸 민다.
    def grow(self):
        # if self.head == self.tail :
        self.bodys.append(Snake.Body(self.tail.pos - self.tail.direction, self.tail.direction))
        self.tail = self.bodys[-1]
        # else :
        #     self.bodys.insert(-2, Snake.Body(self.tail.pos, self.tail.direction))
        #     self.tail.pos = self.tail.pos - self.tail.direction

    #draw 메소드에서는 bodys의 각각의 요소들의 위치를 참고하여 창에 뱀을 그린다.
    def draw(self, screen):
        for i, bloc in enumerate(self.bodys):
            self.rect_snake.x = B_size * bloc.pos[0]  # 그려야하는 좌표의 위치에 snake 이미지 사이즈만큼의 사각형 객체 생성
            self.rect_snake.y = B_size * bloc.pos[1]
            if i == 0:   # 머리 부분 일 떄
                screen.blit(self.head_image, self.rect_snake)

            else:  # 몸통 부분일 때
                screen.blit(self.body_image, self.rect_snake)
