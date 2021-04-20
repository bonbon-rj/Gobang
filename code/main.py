# -*- coding:utf-8 -*-

from chess import Chess
from player import Human, AI


def main():
    chess = Chess(version=1)
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

        if chess.check_game_over():
            chess.show_result()
            break

    chess.window.mainloop()


if __name__ == "__main__":
    main()
