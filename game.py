from pickle import TRUE
import pygame
from menu import MainMenu,SingleInGameMenu,ScoreMenu,DualAutoInGameMenu
from SnakeClass import Snake
from apple_class import Apple
import numpy as np

class Game():
    def __init__(self):
        pygame.init()

        self.playing, self.dual_playing ,self.running = False,False, True
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.BACK_KEY = False, False, False, False, False
        self.W_KEY,self.A_KEY,self.S_KEY,self.D_KEY, self.ENTER_KEY = False, False, False, False, False
        self.WIDTH, self.HEIGHT = 920, 920
        self.COLUMN, self.ROW = 40, 40
        self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font_name = "font/8-BIT WONDER.TTF"
        self.BLACK, self.WHITE, self.RED, self.BLUE = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 0, 255)
        self.curr_menu = MainMenu(self)
        self.snake = Snake(self, (self.ROW / 2, self.COLUMN / 2))
        self.apple = Apple((30, 30), self.snake)
        self.name = "PLAYER"
        self.background = pygame.image.load("img/cau.png").convert_alpha()

##############################################################
                       #play game#
##############################################################

    def game_loop(self):

        if self.dual_playing == True :
            self.snake.load_img(player=1)
            self.new_snake()
        else:
            self.snake.load_img(player=0)


        clock = pygame.time.Clock()

        while self.playing:

            self.check_events()
            
            if self.dual_playing == False :

                # Trigger InGame Menu
                if self.BACK_KEY:
                    # Pause and InGame Menu
                    self.curr_menu = SingleInGameMenu(self)
                    self.curr_menu.display_menu()
                    self.reset_keys()

                pygame.time.delay(50)
                clock.tick(10)
                self.snake.move_1P()

                self.check_wall_hit(self.snake)
                self.check_eat_apple(self.snake, self.apple)
                self.check_body_hit(self.snake)
                
                self.display.fill((255, 255, 255))
                self.drawGrid()
                self.snake.draw(self.display)
                self.apple.draw(self.display)
            
            else :
                if self.BACK_KEY:
                    # Pause and InGame Menu
                    self.curr_menu = DualAutoInGameMenu(self)
                    self.curr_menu.display_menu()
                    self.reset_keys()

                pygame.time.delay(50)
                clock.tick(10)
                self.snake.move_1P()
                self.snake2.move_2P()

                self.check_wall_hit(self.snake,1)
                self.check_wall_hit(self.snake2,2)

                self.check_eat_apple_dual(self.snake, self.apple, self.apple2)
                self.check_eat_apple_dual(self.snake2, self.apple, self.apple2)

                self.check_body_hit(self.snake,1)
                self.check_body_hit(self.snake2,2)
                
                self.check_snake_hit(self.snake, self.snake2)

                self.display.fill((255, 255, 255))
                self.drawGrid()
                self.snake.draw(self.display)
                self.apple.draw(self.display)
                self.snake2.draw(self.display)
                self.apple2.draw(self.display)



            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

    def new_snake(self) :
        self.snake2 = Snake(self, (0,0),dir=np.array([0, 1]), player=2)
        self.apple2 = Apple((20, 20), self.snake2)
    
    #뱀이 사과를 먹었을 때 처리
    def check_eat_apple(self, snake, apple) :
        headPos = snake.head.pos
        appPos = apple.get_position()

        if headPos[0] == appPos[0] and headPos[1] == appPos[1]:
            snake.grow()
            apple.move()

    #뱀이 사과를 먹었을 때 처리(듀얼플레이)
    def check_eat_apple_dual(self, snake, apple1, apple2) :
        headPos = snake.head.pos
        appPos1 = apple1.get_position()
        appPos2 = apple2.get_position()

        if headPos[0] == appPos1[0] and headPos[1] == appPos1[1]:
            snake.grow()
            apple1.move()

        if headPos[0] == appPos2[0] and headPos[1] == appPos2[1]:
            snake.grow()
            apple2.move()

    #뱀이 맵 밖으로 나갔을 때 처리
    def check_wall_hit(self, snake,player=1) :
        headPos = snake.head.pos
        if headPos[0] >= self.ROW or headPos[0] < 0 or headPos[1] >= self.COLUMN or headPos[1] < 0:
            if self.dual_playing == False :
                self.curr_menu = ScoreMenu(self)
                self.name = self.curr_menu.input_name()
                self.store_score(len(snake.bodys) - 1)
                self.curr_menu.display_score(len(snake.bodys) - 1)
            else :
                self.curr_menu = ScoreMenu(self)
                self.curr_menu.display_winner(2 if player == 1 else 1)

    
    #뱀이 자기 몸과 닿았을 때 처리
    def check_body_hit(self, snake,player=1) :
        headPos = snake.head.pos
        for x in range(1, len(snake.bodys)):
            if headPos[0] == snake.bodys[x].pos[0] and headPos[1] == snake.bodys[x].pos[1]:
                if self.dual_playing == False :
                    self.curr_menu = ScoreMenu(self)
                    self.name = self.curr_menu.input_name()
                    self.store_score(len(self.snake.bodys) - 1)
                    self.curr_menu.display_score(len(snake.bodys) - 1)
                    break
                else :
                    self.curr_menu = ScoreMenu(self)
                    self.curr_menu.display_winner(2 if player == 1 else 1)

                    break

    def check_snake_hit(self, snake1, snake2) :
        headPos = snake1.head.pos
        headPos2 = snake2.head.pos

        # 뱀1이 뱀2에 닿았을 때
        for x in range(len(snake2.bodys)):
            if headPos[0] == snake2.bodys[x].pos[0] and headPos[1] == snake2.bodys[x].pos[1]:
                self.curr_menu = ScoreMenu(self)
                self.curr_menu.display_winner(2)
                break
                
        # 뱀2이 뱀1에 닿았을 때
        for x in range(len(snake1.bodys)):
            if headPos2[0] == snake1.bodys[x].pos[0] and headPos2[1] == snake1.bodys[x].pos[1]:
                self.curr_menu = ScoreMenu(self)
                self.curr_menu.display_winner(1)
                break



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_a:
                    self.A_KEY = True
                if event.key == pygame.K_s:
                    self.S_KEY = True
                if event.key == pygame.K_d:
                    self.D_KEY = True
                if event.key == pygame.K_w:
                    self.W_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ENTER_KEY, self.BACK_KEY,self.W_KEY,self.A_KEY,self.S_KEY,self.D_KEY = False, False, False, False ,False, False,False, False ,False, False

    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def drawGrid(self):
        sizeBtwn = self.WIDTH // self.ROW
        x = 0
        y = 0
        for l in range(self.ROW):
            x = x + sizeBtwn
            y = y + sizeBtwn

            # 그리드 그리기
            pygame.draw.line(self.display, (160, 188, 194), (x, 0), (x, self.WIDTH))                      # 세로 줄
            pygame.draw.line(self.display, (160, 188, 194), (0, y), (self.HEIGHT, y))                     # 가로 줄
        self.display.blit(self.background, (270, 330))

    def store_score(self, score):
        try:
            score_file = open('score.txt', 'r')                                                     # score 파일 있으면 열고 없으면 생성
        except FileNotFoundError:
            score_file = open('score.txt', 'w')
            score_file.close()
            score_file = open('score.txt', 'r')

        try:
            name_file = open('name.txt', 'r')                                                     # name 파일 있으면 열고 없으면 생성
        except FileNotFoundError:
            name_file = open('name.txt', 'w')
            name_file.close()
            name_file = open('name.txt', 'r')

        score_list = score_file.read()
        name_list = name_file.read()
        dict_name = {}
        if len(score_list):                                                                 # 파일에서 불러온 정보 리스트로 저장
            score_list = list(map(int, score_list.replace('[', '').replace(']', '').split(', ')))
            name_list = list(name_list.replace('[', '').replace(']', '').replace('\'', '').split(', '))
        else:
            score_list = []
            name_list = []

        for i in range(len(score_list)):                                                    # 이름과 점수 딕셔너리로 저장
            dict_name[name_list[i]] = score_list[i]

        dict_name[self.name] = score
        score_file.close()
        name_file.close()
        dict_name = dict(sorted(dict_name.items(), key=lambda x: x[1], reverse=True))         # 점수 기준으로 내림차순 정릴시키기
        score_list = list(dict_name.values())                                                # 정렬된 점수들 다시 score_list에 저장
        name_list = list(dict_name.keys())                                                   # 점수 기준 정렬된 이름 다시 name_list에 저장

        score_file = open('score.txt', 'w')
        name_file = open('name.txt', 'w')
        score_file.write(str(score_list))
        name_file.write(str(name_list))
        score_file.close()
        name_file.close()

    def get_bodys(self):
        return self.snake.bodys

    def get_turns(self):
        return self.snake.get_turns()

    def get_apple(self):
        return self.apple.get_position()
