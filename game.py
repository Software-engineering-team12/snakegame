from pickle import TRUE
import pygame
from menu import MainMenu, SingleInGameMenu, ScoreMenu, DualAutoInGameMenu
from SnakeClass import Snake
from apple_class import Apple
import numpy as np
import heapq

class Game():
    def __init__(self):
        pygame.init()

        self.playing, self.dual_playing, self.auto_playing, self.running = False, False, False, True
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.BACK_KEY = False, False, False, False, False
        self.W_KEY, self.A_KEY, self.S_KEY, self.D_KEY, self.ENTER_KEY = False, False, False, False, False
        self.WIDTH, self.HEIGHT = 1440, 720
        self.COLUMN, self.ROW = 80, 40
        self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font_name = "font/8-BIT WONDER.TTF"
        self.BLACK, self.WHITE, self.RED, self.BLUE = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 0, 255)
        self.curr_menu = MainMenu(self)
        self.snake = Snake(self, (self.ROW / 2, self.COLUMN / 2))
        self.apple = Apple((30, 30), snake=self.snake)
        self.name = "PLAYER"
        self.background = pygame.image.load("img/cau.png").convert_alpha()

##############################################################
                       #play game#
##############################################################

    def game_loop(self):

        if self.dual_playing == True:
            self.new_snake()
        self.snake.load_img(player=1)



        clock = pygame.time.Clock()


        while self.playing:

            self.check_events()
            
            if self.dual_playing == False and self.auto_playing == False:

                # Trigger InGame Menu
                if self.BACK_KEY:
                    # Pause and InGame Menu
                    self.curr_menu = SingleInGameMenu(self)
                    self.curr_menu.display_menu()
                    self.reset_keys()

                pygame.time.delay(50)
                clock.tick(10)
                self.snake.move_1P()

                self.check_hit(self.snake)
                self.check_eat_apple(self.snake, self.apple)
                
                self.display.fill((255, 255, 255))
                self.drawGrid()
                self.snake.draw(self.display)
                self.apple.draw(self.display)
                self.in_game_score_display(self.snake)
            
            elif self.dual_playing == True :
                if self.BACK_KEY:
                    # Pause and InGame Menu
                    self.curr_menu = DualAutoInGameMenu(self)
                    self.curr_menu.display_menu()
                    self.reset_keys()

                pygame.time.delay(50)
                clock.tick(10)
                self.snake.move_1P()
                self.snake2.move_2P()

                self.check_hit(self.snake, 1)
                self.check_hit(self.snake2, 2)

                self.check_eat_apple(self.snake, self.apple, self.apple2)
                self.check_eat_apple(self.snake2, self.apple, self.apple2)
                self.check_snake_hit(self.snake, self.snake2)

                self.display.fill((255, 255, 255))
                self.drawGrid()
                self.snake.draw(self.display)
                self.apple.draw(self.display)
                self.snake2.draw(self.display)
                self.apple2.draw(self.display)

            elif self.auto_playing == True:

                if self.BACK_KEY:
                    # Pause and InGame Menu
                    self.curr_menu = DualAutoInGameMenu(self)
                    self.curr_menu.display_menu()
                    self.reset_keys()

                pygame.time.delay(10)
                clock.tick(1000)
                finallist = self.a_star()
                if finallist:
                    next = finallist[-1]
                    head = self.snake.head.pos
                    # print(finallist)
                    # print(head)

                    if next[0] == head[0] and next[1] == head[1] + 1:
                        self.DOWN_KEY = True
                    elif next[0] == head[0] and next[1] == head[1] - 1:
                        self.UP_KEY = True
                    elif next[0] == head[0] + 1 and next[1] == head[1]:
                        self.RIGHT_KEY = True
                    elif next[0] == head[0] - 1 and next[1] == head[1]:
                        self.LEFT_KEY = True

                self.snake.move_1P()

                self.check_hit(self.snake)
                self.check_eat_apple(self.snake, self.apple)


                self.display.fill((255, 255, 255))
                self.drawGrid()
                self.snake.draw(self.display)
                self.apple.draw(self.display)
                self.in_game_score_display(self.snake)

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

    def a_star(self):
        board = [[1 for _ in range(self.ROW)] for _ in range(self.COLUMN)]
        dx = [1, -1, 0, 0]
        dy = [0, 0, -1, 1]
        for body in (self.snake.bodys):
            board[int(body.pos[0])][int(body.pos[1])] = 0

        target = self.apple.get_position()
        start = (int(self.snake.head.pos[0]), int(self.snake.head.pos[1]))

        h = abs(start[0] - target[0]) + abs(start[1] - target[1])
        openlist = []
        closelist = []
        heapq.heappush(openlist, (h, 0, start[0], start[1]))  # f,g,x,y,px,py

        while openlist:
            curnode = heapq.heappop(openlist)
            closelist.append(curnode)

            if curnode[2] == target[0] and curnode[3] == target[1]:
                final_list = []
                targetcurnode = target
                while targetcurnode != start:
                    final_list.append(targetcurnode)
                    targetcurnode = board[targetcurnode[0]][targetcurnode[1]]

                return final_list

            for i in range(4):
                next_x = curnode[2] + dx[i]
                next_y = curnode[3] + dy[i]
                if 0 <= next_x < self.COLUMN and 0 <= next_y < self.ROW and board[next_x][next_y] != 0:
                    flag = True
                    for close in closelist:
                        if close[2] == next_x and close[3] == next_y:
                            flag = False
                            break
                    if flag:
                        movecost = curnode[1] + 1
                        flag2 = True
                        for open in openlist:
                            if open[2] == next_x and open[3] == next_y:
                                flag2 = False
                                break
                        if flag2:
                            board[next_x][next_y] = (curnode[2], curnode[3])
                            heapq.heappush(openlist, (
                            movecost + abs(next_x - target[0]) + abs(next_y - target[1]), movecost, next_x, next_y))


    def in_game_score_display(self, snake):
        score = len(self.snake.bodys)
        self.draw_text("The Score is "+str(score), 14, 80, 25, (255, 0, 135))

    def new_snake(self):
        self.snake2 = Snake(self, (0, 0), dir=np.array([0, 1]), player=2)
        self.apple2 = Apple((20, 20), self.snake2)
    
    # 뱀이 사과를 먹었을 때 처리 - apple2가 None이면 single play에서 처리, None 아니면 dual
    def check_eat_apple(self, snake, apple1, apple2=None):
        headPos = snake.head.pos
        appPos = apple1.get_position()

        if headPos[0] == appPos[0] and headPos[1] == appPos[1]:
            snake.grow()
            apple1.move()

        if apple2 != None:
            appPos2 = apple2.get_position()
            if headPos[0] == appPos2[0] and headPos[1] == appPos2[1]:
                snake.grow()
                apple2.move()

   # 뱀이 맵 밖으로 나가는 경우와 자기 몸에 닿아 죽는 경우 처리
    def check_hit(self, snake, player=1):
        headPos = snake.head.pos
        death = False
         # 뱀이 맵 밖으로 나갔을 때 처리
        if headPos[0] >= self.COLUMN or headPos[0] < 0 or headPos[1] >= self.ROW or headPos[1] < 0:
            death = True
        for x in range(1, len(snake.bodys)):                                     # 뱀이 자기 몸과 닿았을 때 처리
            if headPos[0] == snake.bodys[x].pos[0] and headPos[1] == snake.bodys[x].pos[1]:
                death = True
                break

        if death == True:
            if self.dual_playing == False:
                self.curr_menu = ScoreMenu(self)
                self.name = self.curr_menu.input_name()
                self.store_score(len(snake.bodys) - 1)
                self.curr_menu.display_score(len(snake.bodys) - 1)
            else:
                self.curr_menu = ScoreMenu(self)
                self.curr_menu.display_winner(2 if player == 1 else 1)


    def check_snake_hit(self, snake1, snake2):
        headPos = snake1.head.pos
        headPos2 = snake2.head.pos

        if headPos[0] == headPos2[0] and headPos[1] == headPos2[1] :
            self.curr_menu = ScoreMenu(self)
            self.curr_menu.display_winner(0)
        else :
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
        sizeBtwn = self.WIDTH // self.COLUMN
        x = 0
        y = 0
        for i in range(self.ROW):                                                              # 그리드 가로 줄 그리기
            y = y + sizeBtwn
            # 그리드 그리기
            pygame.draw.line(self.display, (160, 188, 194), (0, y), (self.WIDTH, y))                     # 가로 줄

        for i in range(self.COLUMN):                                                              # 그리드 세로 줄 그리기
            x = x + sizeBtwn
            # 그리드 그리기
            pygame.draw.line(self.display, (160, 188, 194), (x, 0), (x, self.WIDTH))  # 세로 줄

        self.display.blit(self.background, ((self.WIDTH- 424) / 2, (self.HEIGHT - 234) / 2))

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


