import pygame
from menu import MainMenu,InGameMenu,ScoreMenu
from SnakeClass import Snake
from apple_class import Apple
import time

class Game():
    def __init__(self):
        pygame.init()

        self.playing,self.running = False,True
        self.UP_KEY,self.DOWN_KEY,self.LEFT_KEY,self.RIGHT_KEY,self.BACK_KEY,self.ENTER_KEY = False,False,False,False,False,False
        self.WIDTH,self.HEIGHT = 800,800
        self.COLUMN,self.ROW = 40,40
        self.display = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.window = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.font_name = "font/8-BIT WONDER.TTF"
        self.BLACK, self.WHITE, self.RED= (0, 0, 0), (255, 255, 255), (255,0,0)
        self.curr_menu = MainMenu(self)
        self.snake = Snake(self,(self.ROW/2, self.COLUMN/2))
        self.apple = Apple((30,30),self.snake)


##############################################################
                       #play game#
##############################################################

    def game_loop(self):

        # snake = self.snake
        # apple = self.apple
        clock = pygame.time.Clock()

        while self.playing:

            self.check_events()

            #Trigger InGame Menu
            if self.BACK_KEY:
                print("InGame Menu")
                #Pause and InGame Menu
                self.curr_menu = InGameMenu(self)
                self.curr_menu.display_menu()
                self.reset_keys()



            pygame.time.delay(50)
            clock.tick(10)
            self.snake.move()
            headPos = self.snake.head.pos
            appPos = self.apple.get_position()

            if headPos[0] >= self.ROW or headPos[0] < 0 or headPos[1] >= self.COLUMN or headPos[1] < 0:
                self.store_score(len(self.snake.bodys))
                self.curr_menu = ScoreMenu(self)
                self.curr_menu.display_score(len(self.snake.bodys))

            if headPos[0] == appPos[0] and headPos[1] == appPos[1]:
                self.snake.grow()
                self.apple.move()

            for x in range(1, len(self.snake.bodys)):
                if headPos[0] == self.snake.bodys[x].pos[0] and headPos[1] == self.snake.bodys[x].pos[1]:
                    self.store_score(len(self.snake.bodys))
                    self.curr_menu = ScoreMenu(self)
                    self.curr_menu.display_score(len(self.snake.bodys))
                    break

            self.display.fill((255, 255, 255))
            self.drawGrid()
            self.snake.draw(self.display)
            self.apple.draw(self.display)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()


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

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY,self.LEFT_KEY,self.RIGHT_KEY, self.ENTER_KEY, self.BACK_KEY = False, False, False, False ,False, False

    def draw_text(self, text, size, x, y,color= (255,255,255)):
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
            pygame.draw.line(self.display, (0, 0, 0), (x, 0), (x, self.WIDTH)) # 세로 줄
            pygame.draw.line(self.display, (0, 0, 0), (0, y), (self.HEIGHT, y)) # 가로 줄


    def store_score(self, score):
        try:
            score_file = open('score.txt', 'r')  # score 파일 있으면 열고 없으면 생성
        except FileNotFoundError:
            score_file = open('score.txt', 'w')
            score_file.close()
            score_file = open('score.txt', 'r')

        score_list = score_file.read()
        print(score_list)
        if len(score_list):
            score_list = list(map(int, score_list.replace('[', '').replace(']', '').split(', ')))
        else:
            score_list = []

        score_file.close()
        score_list.append(score)
        score_list.sort(reverse=True)
        print(score_list)

        score_file = open('score.txt', 'w')
        score_file.write(str(score_list))
        score_file.close()


    def get_bodys(self):
        return self.snake.bodys

    def get_keys(self):
        return
    def get_turns(self):
        print(self.snake.get_turns())
        return self.snake.get_turns()

    def get_apple(self):
        return self.apple.get_position()



    #
    # def update(self):
    #
    #     self.display.fill((255, 255, 255))
    #     self.drawGrid(screen)
    #     snake.draw(screen)
    #     apple.draw(screen)
    #     pygame.display.update()


    # def playgame(self):
    #
    #     snake = Snake((10, 10))
    #     apple = Apple((30,30), snake)
    #     clock = pygame.time.Clock()
    #
    #     while self.playing:
    #
    #         pygame.time.delay(50)
    #         clock.tick(10)
    #         snake.move()
    #         headPos = snake.head.pos
    #         appPos = apple.get_position()
    #
    #         if headPos[0] >= self.ROW or headPos[0] < 0 or headPos[1] >= self.COLUMN or headPos[1] < 0:
    #             print("Score:", len(snake.bodys))
    #             snake.reset((10, 10))
    #
    #
    #         if headPos[0] == appPos[0] and headPos[1] == appPos[1]:
    #             snake.grow()
    #             apple.move()
    #
    #         for x in range(1,len(snake.bodys)):
    #             if headPos[0] == snake.bodys[x].pos[0] and headPos[1] == snake.bodys[x].pos[1] :
    #                 print("Score :", len(snake.bodys))
    #                 snake.reset((10,10))
    #                 break
    #
    #
    #         self.display.fill((255, 255, 255))
    #         self.drawGrid()
    #         snake.draw(self.display)
    #         apple.draw(self.display)
    #         self.window.blit(self.display, (0, 0))
    #         pygame.display.update()
