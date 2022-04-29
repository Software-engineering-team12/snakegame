from game import Game

if __name__ == '__main__':

    game = Game()

    while game.running:
        game.curr_menu.display_menu()
        game.game_loop()


