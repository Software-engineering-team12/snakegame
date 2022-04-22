import pygame
from menu import MainMenu
from SnakeClass import Snake
from apple_class import Apple

class Game():
    def __init__(self):
        pygame.init()

        self.playing,self.running = False,True
        self.UP_KEY,self.DOWN_KEY,self.BACK_KEY,self.ENTER_KEY = False,False,False,False
        self.WIDTH,self.HEIGHT = 800,800
        self.COLUMN,self.ROW = 40,40
        self.display = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.window = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.font_name = "font/8-BIT WONDER.TTF"
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.curr_menu = MainMenu(self)


    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.ENTER_KEY:
                self.playing = False
            self.playgame()
            # self.display.fill(self.BLACK)
            # self.draw_text('Thanks for Playing', 20, self.WIDTH / 2, self.HEIGHT / 2)
            # self.window.blit(self.display, (0, 0))
            # pygame.display.update()
            # self.reset_keys()

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

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)



##############################################################
                        #play game#
##############################################################
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

    #
    # def update(self):
    #
    #     self.display.fill((255, 255, 255))
    #     self.drawGrid(screen)
    #     snake.draw(screen)
    #     apple.draw(screen)
    #     pygame.display.update()


    def playgame(self):

        snake = Snake((10, 10))
        apple = Apple((30,30), snake)
        clock = pygame.time.Clock()

        while self.playing:

            pygame.time.delay(50)
            clock.tick(10)
            snake.move()
            headPos = snake.head.pos
            appPos = apple.get_position()

            if headPos[0] >= self.ROW or headPos[0] < 0 or headPos[1] >= self.COLUMN or headPos[1] < 0:
                print("Score:", len(snake.bodys))
                snake.reset((10, 10))


            if headPos[0] == appPos[0] and headPos[1] == appPos[1]:
                snake.grow()
                apple.move()

            for x in range(1,len(snake.bodys)):
                if headPos[0] == snake.bodys[x].pos[0] and headPos[1] == snake.bodys[x].pos[1] :
                    print("Score :", len(snake.bodys))
                    snake.reset((10,10))
                    break


            self.display.fill((255, 255, 255))
            self.drawGrid()
            snake.draw(self.display)
            apple.draw(self.display)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
