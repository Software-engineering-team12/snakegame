import sys
import pygame
import numpy as np

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.WIDTH / 2, self.game.HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 23, 23)
        self.offset = - 110                             # offset 수정했음

    def draw_cursor(self, color=(255, 255, 255)):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y, color)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):                 # 전반적으로 위치 조정 줄 간격 및 글자 크기 조절
        Menu.__init__(self, game)
        self.state = "Single Play"
        self.singlex, self.singley = self.mid_w, self.mid_h - 10
        self.dualx, self.dualy = self.mid_w, self.mid_h + 20
        self.autox, self.autoy = self.mid_w, self.mid_h + 50
        self.loadx, self.loady = self.mid_w, self.mid_h + 80
        self.rankingx, self.rankingy = self.mid_w, self.mid_h + 110
        self.exitx, self.exity = self.mid_w, self.mid_h + 140
        self.cursor_rect.midtop = (self.singlex + self.offset, self.singley)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Main Menu", 35, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 100)
            self.game.draw_text("Single Play", 20, self.singlex, self.singley)
            self.game.draw_text("Dual Play", 20, self.dualx, self.dualy)
            self.game.draw_text("Auto Play", 20, self.autox, self.autoy)
            self.game.draw_text("Load", 20, self.loadx, self.loady)
            self.game.draw_text("Ranking", 20, self.rankingx, self.rankingy)
            self.game.draw_text("Exit", 20, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):

        if self.game.DOWN_KEY:
            if self.state == "Single Play":
                self.cursor_rect.midtop = (self.dualx + self.offset, self.dualy)
                self.state = "Dual Play"
            elif self.state == "Dual Play":
                self.cursor_rect.midtop = (self.autox + self.offset, self.autoy)
                self.state = "Auto Play"
            elif self.state == "Auto Play":
                self.cursor_rect.midtop = (self.loadx + self.offset, self.loady)
                self.state = "Load"
            elif self.state == "Load":
                self.cursor_rect.midtop = (self.rankingx + self.offset, self.rankingy)
                self.state = "Ranking"
            elif self.state == "Ranking":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.singlex + self.offset, self.singley)
                self.state = "Single Play"
        elif self.game.UP_KEY:
            if self.state == "Single Play":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Dual Play":
                self.cursor_rect.midtop = (self.singlex + self.offset, self.singley)
                self.state = "Single Play"
            elif self.state == "Auto Play":
                self.cursor_rect.midtop = (self.dualx + self.offset, self.dualy)
                self.state = "Dual Play"
            elif self.state == "Load":
                self.cursor_rect.midtop = (self.autox + self.offset, self.autoy)
                self.state = "Auto Play"
            elif self.state == "Ranking":
                self.cursor_rect.midtop = (self.loadx + self.offset, self.loady)
                self.state = "Load"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.rankingx + self.offset, self.rankingy)
                self.state = "Ranking"

    def check_input(self):
        self.move_cursor()
        if self.game.ENTER_KEY:
            if self.state == "Single Play":
                self.game.snake.reset((self.game.COLUMN / 2, self.game.ROW / 2))
                self.game.apple.set_position(position=(30, 30))
                #self.game.snake2.reset((self.game.ROW / 4, self.game.COLUMN / 4))
                #self.game.apple2.set_position(position=(20, 20))
                self.game.dual_playing = False
                self.game.playing = True
                self.game.dual_playing = False
                self.run_display = False

            elif self.state == "Dual Play":
                self.game.snake.reset((self.game.COLUMN-1, self.game.ROW-1))
                self.game.apple.set_position(position=(30, 30))
                self.game.dual_playing = True
                self.game.playing = True
                self.run_display = False

            elif self.state == "Auto Play":
                pass                            # 추가 필요
            elif self.state == "Load":
                save_bodys = []
                load_file = open('game_file.txt', 'r')
                load_game = list(load_file.read().split('\n'))
                load_apple = tuple(map(int, load_game[0].split()))
                snake_size = int(load_game[1])
                for i in range(snake_size):
                    save_bodys.append(list(map(int, load_game[i + 2].split())))

                self.game.apple.set_position(load_apple)

                self.game.snake.reset((self.game.COLUMN / 2, self.game.ROW / 2))
                self.game.snake.set_body(save_bodys)
                self.game.playing = True

                load_file.close()
                self.run_display = False

            elif self.state == "Ranking":
                self.game.curr_menu = RankMenu(self.game)
                self.game.curr_menu.display_menu()
                self.game.reset_keys()
                self.run_display = False

            elif self.state == "Exit":
                self.run_display = False
                pygame.quit()
                sys.exit()


class SingleInGameMenu(Menu):                              # singleplay 일 떄 ingamemenu -> 과제1의 ingamemenu와 동일
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Resume"
        self.resumex, self.resumey = self.mid_w, self.mid_h + 10
        self.restartx, self.restarty = self.mid_w, self.mid_h + 40
        self.savex, self.savey = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.WHITE)
            self.game.draw_text("InGame Menu", 35, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 100, self.game.BLACK)
            self.game.draw_text("Resume", 20, self.resumex, self.resumey, self.game.BLACK)
            self.game.draw_text("Restart", 20, self.restartx, self.restarty, self.game.BLACK)
            self.game.draw_text("Save", 20, self.savex, self.savey, self.game.BLACK)
            self.game.draw_text("Return to Main Menu ", 20, self.exitx, self.exity, self.game.BLACK)
            self.draw_cursor(self.game.BLACK)
            self.blit_screen()

    def move_cursor(self):

        if self.game.DOWN_KEY:
            if self.state == "Resume":
                self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)
                self.state = "Restart"
            elif self.state == "Restart":
                self.cursor_rect.midtop = (self.savex + self.offset, self.savey)
                self.state = "Save"
            elif self.state == "Save":
                self.cursor_rect.midtop = (self.exitx + self.offset * 2, self.exity)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
                self.state = "Resume"
        elif self.game.UP_KEY:
            if self.state == "Resume":
                self.cursor_rect.midtop = (self.exitx + self.offset * 2, self.exity)
                self.state = "Exit"
            elif self.state == "Restart":
                self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
                self.state = "Resume"
            elif self.state == "Save":
                self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)
                self.state = "Restart"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.savex + self.offset, self.savey)
                self.state = "Save"

    def check_input(self):
        self.move_cursor()
        if self.game.ENTER_KEY:
            if self.state == "Resume":
                self.run_display = False
            elif self.state == "Restart":
                self.game.snake.reset((self.game.COLUMN / 2, self.game.ROW / 2))
                self.game.apple.set_position((30, 30))                             # apple 위치 초기화
                self.run_display = False
            elif self.state == "Save":
                game_file = open('game_file.txt', 'w')
                game_file.write(str(self.game.get_apple()[0]) + " " + str(self.game.get_apple()[1]) + '\n')
                game_file.write(str(len(self.game.get_bodys())) + '\n')
                for i in self.game.get_bodys():
                    game_file.write("{0} {1} {2} {3}\n".format(int(i.pos[0]), int(i.pos[1]), int(i.direction[0]),
                                                               int(i.direction[1])))
                game_file.close()

                self.game.curr_menu = MainMenu(self.game)
                self.run_display = False
                self.game.playing = False

            elif self.state == "Exit":
                self.game.curr_menu = MainMenu(self.game)
                self.run_display = False
                self.game.playing = False


class DualAutoInGameMenu(Menu):                                    # dual과 auto의 ingamemenue 기능 동일
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Resume"
        self.resumex, self.resumey = self.mid_w, self.mid_h + 10
        self.restartx, self.restarty = self.mid_w, self.mid_h + 40
        self.exitx, self.exity = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.WHITE)
            self.game.draw_text("InGame Menu", 35, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 100, self.game.BLACK)
            self.game.draw_text("Resume", 20, self.resumex, self.resumey, self.game.BLACK)
            self.game.draw_text("Restart", 20, self.restartx, self.restarty, self.game.BLACK)
            self.game.draw_text("Return to Main Menu ", 20, self.exitx, self.exity, self.game.BLACK)
            self.draw_cursor(self.game.BLACK)
            self.blit_screen()

    def move_cursor(self):

        if self.game.DOWN_KEY:
            if self.state == "Resume":
                self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)
                self.state = "Restart"
            elif self.state == "Restart":
                self.cursor_rect.midtop = (self.exitx + self.offset * 2, self.exity)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.resumex + self.offset , self.resumey)
                self.state = "Resume"
        elif self.game.UP_KEY:
            if self.state == "Resume":
                self.cursor_rect.midtop = (self.exitx + self.offset * 2, self.exity)
                self.state = "Exit"
            elif self.state == "Restart":
                self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
                self.state = "Resume"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)
                self.state = "Restart"

    def check_input(self):
        self.move_cursor()
        if self.game.ENTER_KEY:
            if self.state == "Resume":
                self.run_display = False
            elif self.state == "Restart":
                self.game.snake.reset((self.game.COLUMN-1, self.game.ROW-1), dir=np.array([0, -1]))
                self.game.snake2.reset((0, 0), dir=np.array([0, 1]))
                self.game.apple.set_position((30, 30))                               # apple 위치 초기화
                self.game.apple2.set_position((20, 20))
                self.run_display = False
            elif self.state == "Exit":
                self.game.curr_menu = MainMenu(self.game)
                self.run_display = False
                self.game.playing = False


class ScoreMenu(Menu):                               # single과 dual 게임 종로 시 나타나는 메뉴로 single시 display_score 호출
    def __init__(self, game):                        # dual 시 승리한 사람 매개변수 받아서 display_winner 메소드 호출
        Menu.__init__(self, game)
        self.state = "Restart"
        self.restartx, self.restarty = self.mid_w, self.mid_h + 30
        self.exitx, self.exity = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)



    def display_score(self, score):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.WHITE)
            self.game.draw_text("Your score is ", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 20, self.game.BLACK)
            self.game.draw_text(str(score), 20, self.game.WIDTH / 2 + 140, self.game.HEIGHT / 2 - 20, self.game.RED)
            self.game.draw_text("Restart", 20, self.restartx, self.restarty, self.game.BLACK)
            self.game.draw_text("Return to Main Menu ", 20, self.exitx, self.exity, self.game.BLACK)
            self.draw_cursor(self.game.BLACK)
            self.blit_screen()

    def display_winner(self, winner):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.WHITE)
            self.game.draw_text("The Winner is %d" %winner, 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 20, self.game.BLACK)
            self.game.draw_text("Restart", 20, self.restartx, self.restarty, self.game.BLACK)
            self.game.draw_text("Return to Main Menu ", 20, self.exitx, self.exity, self.game.BLACK)
            self.draw_cursor(self.game.BLACK)
            self.blit_screen()

    def input_name(self):
        self.run_display = True
        temp = ''
        while self.run_display:
            self.game.display.fill(self.game.WHITE)
            self.game.draw_text("what is your name ", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 40, self.game.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running, self.playing = False, False
                    self.curr_menu.run_display = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.run_display = False
                        return temp
                    elif event.key == pygame.K_BACKSPACE:
                        temp = temp[:-1]
                    else:
                        temp += event.unicode

            self.game.draw_text(temp, 20, self.game.WIDTH / 2, self.game.HEIGHT / 2, self.game.BLUE)
            self.blit_screen()

    def move_cursor(self):

        if self.game.DOWN_KEY:
            if self.state == "Restart":
                self.cursor_rect.midtop = (self.exitx + self.offset * 2, self.exity)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)
                self.state = "Restart"
        elif self.game.UP_KEY:
            if self.state == "Restart":
                self.cursor_rect.midtop = (self.exitx + self.offset * 2, self.exity)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.restartx + self.offset, self.restarty)
                self.state = "Restart"

    def check_input(self):
        self.move_cursor()
        if self.game.ENTER_KEY:
            if self.state == "Restart":
                if self.game.dual_playing == False:
                    self.game.snake.reset((self.game.COLUMN / 2, self.game.ROW / 2))
                    self.game.apple.set_position((30, 30))
                else:
                    self.game.snake.reset((self.game.COLUMN - 1, self.game.ROW - 1), dir=np.array([0, -1]))
                    self.game.snake2.reset((0, 0), dir=np.array([0, 1]))
                    self.game.apple.set_position((30, 30))
                    self.game.apple2.set_position((20, 20))

                self.run_display = False
            elif self.state == "Exit":
                self.game.curr_menu = MainMenu(self.game)
                self.run_display = False
                self.game.playing = False
                

class RankMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Menu"
        self.rankx, self.ranky = self.mid_w, self.mid_h-120
        self.exitx, self.exity = self.mid_w + 220, self.mid_h + 310
        self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)

    def display_menu(self):
        self.run_display = True
        name, score = self.get_ranking()
        while self.run_display:
            self.game.display.fill(self.game.WHITE)
            self.game.draw_text("TOP Ranking", 30, self.rankx, self.ranky, self.game.RED)
            self.game.draw_text("1st  %s  %s" % (name[0], score[0]), 20, self.rankx, self.ranky+40, self.game.BLACK)
            self.game.draw_text("2nd  %s  %s" % (name[1], score[1]), 20, self.rankx, self.ranky + 60, self.game.BLACK)
            self.game.draw_text("3rd  %s  %s" % (name[2], score[2]), 20, self.rankx, self.ranky + 80, self.game.BLACK)
            self.game.draw_text("4th  %s  %s" % (name[3], score[3]), 20, self.rankx, self.ranky + 100, self.game.BLACK)
            self.game.draw_text("5th  %s  %s" % (name[4], score[4]), 20, self.rankx, self.ranky + 120, self.game.BLACK)
            self.game.draw_text("Exit", 20, self.exitx, self.exity, self.game.BLACK)
            self.draw_cursor(self.game.BLACK)
            self.blit_screen()
            self.game.check_events()
            self.check_input()

    def check_input(self):
        if self.game.ENTER_KEY:
            self.game.curr_menu = MainMenu(self.game)
            self.run_display = False
            self.game.playing = False

    def get_ranking(self):
        try:
            score_file = open('score.txt', 'r')  # score 파일 있으면 열고 없으면 생성
        except FileNotFoundError:
            score_file = open('score.txt', 'w')
            score_file.close()
            score_file = open('score.txt', 'r')

        try:
            name_file = open('name.txt', 'r')  # name 파일 있으면 열고 없으면 생성
        except FileNotFoundError:
            name_file = open('name.txt', 'w')
            name_file.close()
            name_file = open('name.txt', 'r')

        score = score_file.read()
        name = name_file.read()
        if len(score) !=0:
            score = list(score.replace('[', '').replace(']', '').replace(',', '').split())
            name = list(name.replace('[', '').replace(']', '').replace(',', '').replace('\'', '').split())
        else:
            score = []
            name = []

        if len(score) < 5:
            while len(score) != 5:
                score.append(' ')
                name.append('empty')
        score_file.close()
        name_file.close()
        return name, score
