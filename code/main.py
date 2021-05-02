# -*- coding:utf-8 -*-
from chess import Chess
from player import Human, AI


def main():
    # init object
    chess = Chess(version=1, human_first=True)
    human = Human()
    ai = AI(depth=3)

    while True:
        if chess.is_human_turn:
            human.play(chess)
            if not chess.is_close:
                chess.window.update()
            else:
                break
        else:
            ai.calc(chess, ai.calc_depth)
            ai.play(chess)

        # check whether the game is over
        if chess.check_game_over():
            chess.show_result()
            break

    chess.window.mainloop()


if __name__ == "__main__":
    main()
