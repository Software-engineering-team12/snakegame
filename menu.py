import sys

import pygame


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.WIDTH / 2, self.game.HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self,color=(255,255,255)):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y,color)

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
        self.run_display =True
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
                self.game.snake.reset((self.game.ROW/2, self.game.COLUMN/2))
                self.game.playing = True
            elif self.state == "Load":
                print("Load state")
            elif self.state == "Ranking":
                print("Ranking state")
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
        self.run_display =True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.WHITE)
            self.game.draw_text("InGame Menu", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 20,self.game.BLACK)
            self.game.draw_text("Resume", 20, self.resumex, self.resumey,self.game.BLACK)
            self.game.draw_text("Restart", 20, self.restartx, self.restarty,self.game.BLACK)
            self.game.draw_text("Save", 20, self.savex, self.savey,self.game.BLACK)
            self.game.draw_text("Return to Main Menu ", 20, self.exitx, self.exity,self.game.BLACK)
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
                self.game.snake.reset((self.game.ROW/2, self.game.COLUMN/2))
                self.run_display = False
            elif self.state == "Save":
                pass
            elif self.state == "Exit":
                self.game.curr_menu = MainMenu(self.game)
                self.run_display = False
                self.game.playing = False

