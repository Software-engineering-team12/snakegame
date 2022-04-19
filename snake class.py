# Snake Class
import pygame
import numpy as np

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
    def __init__(self, position = np.array([20,20])) :
        self.head = Snake.Body(position)
        self.bodys.append(self.head)
        self.tail = self.bodys[-1]

    #reset 메소드에서는 게임을 다시 시작할 때 뱀을 초기상태로 되돌린다.
    def reset(self, position) :
        self.bodys = []
        self.turns = {}
        self.head = Snake.Body(position)
        self.bodys.append(self.head)
        self.tail = self.bodys[-1]

    #move 메소드에서는 키보드 입력을 받아 뱀을 움직인다.
    def move(self) :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            #elif event.type == KEY['ESC'] :
                #show_ingame_menu
            #    pass
            keys = pygame.key.get_pressed()

            for key in keys :
                if keys[ KEY['UP'] ] :
                    self.turns[ tuple(self.head.pos[:]) ] = DIRECTION['u']
                elif keys[ KEY['DOWN'] ] :
                    self.turns[ tuple(self.head.pos[:]) ] = DIRECTION['d']
                elif keys[ KEY['LEFT'] ] :
                    self.turns[ tuple(self.head.pos[:]) ] = DIRECTION['l']
                elif keys[ KEY['RIGHT'] ] :
                    self.turns[ tuple(self.head.pos[:]) ] = DIRECTION['r']
                
        for i, bloc in enumerate(self.bodys) :
            p = bloc.pos[:]
            d = bloc.direction
            if tuple(p) in self.turns :
                bloc.pos = p + self.turns[tuple(p)]
                bloc.direction = self.turns[tuple(p)]
                if i == len(self.bodys) - 1 :
                    self.turns.pop(tuple(p))
            else :
                bloc.pos = p + d


    #grow 메소드에서는 뱀이 사과를 먹으면 길이가 늘어나는 행동을 취한다. 참고한 코드와 다르게 현재 꼬리자리에 몸통을 한칸 만들고 꼬리를 진행방행과 반대 방향으로 한칸 민다.
    def grow(self) :
        if self.head == self.tail :
            self.bodys.append(Snake.Body(self.tail.pos - self.tail.direction, self.tail.direction))
            self.tail = self.bodys[-1]
        else :
            self.bodys.insert(-2, Snake.Body(self.tail.pos, self.tail.direction))
            self.tail.pos = self.tail.pos - self.tail.direction

    #draw 메소드에서는 bodys의 각각의 요소들의 위치를 참고하여 창에 뱀을 그린다.
    def draw(self, window) :
        for i, bloc in enumerate(self.bodys) :
            if i == 0 :
                draw_block(window, bloc.pos, type = 'head')   #draw_block메소드 정의 필요 - def draw_block(배경, 위치, 타입(머리, 몸통)) <- 지원님 코드 스타일에 맞게 바꿀수 있습니다.
            #elif i == (len(self.bodys) - 1) :
            #    draw_block(window, c.pos, type = 'tail')  #추후 이미지 삽입시 머리, 몸통 꼬리로 나눌수 있다면 사용할 예정입니다.
            else :
                draw_block(window, bloc.pos, type = 'body')
                