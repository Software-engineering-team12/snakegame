import sys

import pygame


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.WIDTH / 2, self.game.HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self, color=(255, 255, 255)):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y, color)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.loadx, self.loady = self.mid_w, self.mid_h + 50
        self.rankingx, self.rankingy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Main Menu", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Load", 20, self.loadx, self.loady)
            self.game.draw_text("Ranking", 20, self.rankingx, self.rankingy)
            self.game.draw_text("Exit", 20, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):

        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.loadx + self.offset, self.loady)
                self.state = "Load"
            elif self.state == "Load":
                self.cursor_rect.midtop = (self.rankingx + self.offset, self.rankingy)
                self.state = "Ranking"
            elif self.state == "Ranking":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Load":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            elif self.state == "Ranking":
                self.cursor_rect.midtop = (self.loadx + self.offset, self.loady)
                self.state = "Load"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.rankingx + self.offset, self.rankingy)
                self.state = "Ranking"

    def check_input(self):
        self.move_cursor()
        if self.game.ENTER_KEY:
            if self.state == "Start":
                self.game.snake.reset((self.game.ROW / 2, self.game.COLUMN / 2))
                self.game.apple.set_position(position=(30,30))
                self.game.playing = True
            elif self.state == "Load":
                save_bodys = []
                load_file = open('game_file.txt', 'r')
                load_game = list(load_file.read().split('\n'))
                load_apple = tuple(map(int, load_game[0].split()))
                snake_size = int(load_game[1])
                for i in range(snake_size):
                    save_bodys.append(list(map(int, load_game[i + 2].split())))

                self.game.apple.set_position(load_apple)

                self.game.snake.reset((self.game.ROW / 2, self.game.COLUMN / 2))
                self.game.snake.set_body(save_bodys)
                self.game.playing = True

                load_file.close()

            elif self.state == "Ranking":
                self.game.curr_menu = RankMenu(self.game)
                self.game.curr_menu.display_menu()
                self.game.reset_keys()

            elif self.state == "Exit":
                pygame.quit()
                sys.exit()
            self.run_display = False


class InGameMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Resume"
        self.resumex, self.resumey = self.mid_w, self.mid_h + 30
        self.restartx, self.restarty = self.mid_w, self.mid_h + 50
        self.savex, self.savey = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.WHITE)
            self.game.draw_text("InGame Menu", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 20, self.game.BLACK)
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
                self.game.snake.reset((self.game.ROW / 2, self.game.COLUMN / 2))
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


class ScoreMenu(Menu):
    def __init__(self, game):
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
                self.game.snake.reset((self.game.ROW / 2, self.game.COLUMN / 2))
                self.run_display = False
            elif self.state == "Exit":
                self.game.curr_menu = MainMenu(self.game)
                self.run_display = False
                self.game.playing = False


class RankMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Menu"
        self.rankx, self.ranky = self.mid_w, self.mid_h-150
        self.menux, self.menuy = self.mid_w + 220, self.mid_h + 260
        self.startx, self.starty = self.mid_w + 220, self.mid_h + 290
        self.exitx, self.exity = self.mid_w + 220, self.mid_h + 310
        self.cursor_rect.midtop = (self.menux + self.offset, self.menuy)

    def display_menu(self):
        self.run_display = True
        rank = self.get_ranking()
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.WHITE)
            self.game.draw_text("TOP Ranking", 30, self.rankx, self.ranky, self.game.RED)
            self.game.draw_text("%s" % rank[0], 20, self.rankx, self.ranky+40, self.game.BLACK)
            self.game.draw_text("%s" % rank[1], 20, self.rankx, self.ranky + 60, self.game.BLACK)
            self.game.draw_text("%s" % rank[2], 20, self.rankx, self.ranky + 80, self.game.BLACK)
            self.game.draw_text("%s" % rank[3], 20, self.rankx, self.ranky + 100, self.game.BLACK)
            self.game.draw_text("%s" % rank[4], 20, self.rankx, self.ranky + 120, self.game.BLACK)
            self.game.draw_text("Menu", 25, self.menux, self.menuy, self.game.BLACK)
            self.game.draw_text("Start", 20, self.startx, self.starty, self.game.BLACK)
            self.game.draw_text("Exit", 20, self.exitx, self.exity, self.game.BLACK)
            self.draw_cursor(self.game.BLACK)
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.menux + self.offset, self.menuy)
                self.state = "Menu"
            else:
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.menux + self.offset, self.menuy)
                self.state = "Menu"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            else:
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"

    def check_input(self):
        self.move_cursor()
        if self.game.ENTER_KEY:
            if self.state == "Start":
                self.game.snake.reset((self.game.ROW / 2, self.game.COLUMN / 2))
                self.game.playing = True
                self.run_display = False
            elif self.state == "Exit":
                self.game.curr_menu = MainMenu(self.game)
                self.run_display = False
                self.game.playing = False

    def get_ranking(self):
        try:
            score_file = open('score.txt', 'r')                                             # score 파일 있으면 열고 없으면 생성
        except FileNotFoundError:
            score_file = open('score.txt', 'w')
            score_file.close()
            score_file = open('score.txt', 'r')

        rank = score_file.read()
        if len(rank) !=0:
            rank = list(rank.replace('[', '').replace(']', '').replace(',', '').split())
        else:
            rank = []

        if len(rank)<5:
            while len(rank) != 5:
                rank.append('empty')
        score_file.close()
        return rank