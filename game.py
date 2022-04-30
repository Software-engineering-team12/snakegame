import pygame
from menu import MainMenu,InGameMenu,ScoreMenu
from SnakeClass import Snake
from apple_class import Apple


class Game():
    def __init__(self):
        pygame.init()

        self.playing, self.running = False, True
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.BACK_KEY, self.ENTER_KEY = False, False, False, False, False, False
        self.WIDTH, self.HEIGHT = 920, 920
        self.COLUMN, self.ROW = 40, 40
        self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font_name = "font/8-BIT WONDER.TTF"
        self.BLACK, self.WHITE, self.RED, self.BLUE = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 0, 255)
        self.curr_menu = MainMenu(self)
        self.snake = Snake(self, (self.ROW/2, self.COLUMN/2))
        self.apple = Apple((30, 30), self.snake)
        self.name = "PLAYER"
        self.background = pygame.image.load("image/cau.png").convert_alpha()

##############################################################
                       #play game#
##############################################################

    def game_loop(self):

        clock = pygame.time.Clock()

        while self.playing:

            self.check_events()

            #Trigger InGame Menu
            if self.BACK_KEY:
                #Pause and InGame Menu
                self.curr_menu = InGameMenu(self)
                self.curr_menu.display_menu()
                self.reset_keys()

            pygame.time.delay(50)
            clock.tick(10)
            self.snake.move()
            headPos = self.snake.head.pos
            appPos = self.apple.get_position()

            #뱀이 맵 밖으로 나갔을 때 처리
            if headPos[0] >= self.ROW or headPos[0] < 0 or headPos[1] >= self.COLUMN or headPos[1] < 0:
                self.curr_menu = ScoreMenu(self)
                self.name = self.curr_menu.input_name()
                self.store_score(len(self.snake.bodys)-1)
                self.curr_menu.display_score(len(self.snake.bodys)-1)

            #뱀이 사과를 먹었을 때 처리
            if headPos[0] == appPos[0] and headPos[1] == appPos[1]:
                self.snake.grow()
                self.apple.move()

            #뱀이 자기 몸과 닿았을 때 처리
            for x in range(1, len(self.snake.bodys)):
                if headPos[0] == self.snake.bodys[x].pos[0] and headPos[1] == self.snake.bodys[x].pos[1]:
                    self.curr_menu = ScoreMenu(self)
                    self.name = self.curr_menu.input_name()
                    self.store_score(len(self.snake.bodys)-1)
                    self.curr_menu.display_score(len(self.snake.bodys)-1)
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
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ENTER_KEY, self.BACK_KEY = False, False, False, False ,False, False

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
        self.display.blit(self.background, (200, 250))

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
