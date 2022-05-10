from game import Game

if __name__ == '__main__':

    game = Game()

    while game.running:
        game.dual_playing = True
        game.curr_menu.display_menu()
        game.game_loop()


