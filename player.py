import _tkinter
import random


class Human:
    def __init__(self):
        self.color = "black"

    def play(self, chess):
        try:
            chess.chess.bind("<Button-1>", lambda event: chess.human_press_mouse(event, color=self.color))
        except _tkinter.TclError:
            chess.is_close = True


class AI:
    def __init__(self):
        self.color = "white"
        self.x = 500
        self.y = 500
        self.calc_depth = 3
        #  TODO if depth %2 ==0
        self.calc_tree = []
        self.calc_num = 3  # 每一步棋计算最优前

    def calc(self, chess, n):

        if n > 0:
            final_result = []
            if not ((self.calc_depth - n) % 2):
                ai_result = []
                for col in range(chess.width_offset, chess.width - chess.width_offset + chess.spacing, chess.spacing):
                    for row in range(chess.height_offset, chess.height - chess.height_offset + chess.spacing,
                                     chess.spacing):
                        # TODO judge whether in
                        ai_score = chess.get_score(col, row, False)
                        human_score = chess.get_score(col, row, True)
                        ai_result.append([ai_score + human_score, col, row])
                ai_result = sorted(ai_result, key=lambda s: s[0], reverse=True)

                cnt = 0
                for i in range(len(ai_result)):
                    if [ai_result[i][1], ai_result[i][2]] not in chess.human_press_history:
                        if [ai_result[i][1], ai_result[i][2]] not in chess.ai_press_history:
                            final_result.append(ai_result[i])
                            cnt += 1
                            if cnt >= self.calc_num:
                                break
                print("ai:", final_result)
                for i in range(len(final_result)):
                    chess.ai_press_history.append((final_result[i][1], final_result[i][2]))
                    self.calc(chess, n - 1)

                    if n == 1:
                        self.calc_tree.append(final_result[i])
                    chess.ai_press_history.pop()
            else:
                human_result = []
                for col in range(chess.width_offset, chess.width - chess.width_offset + chess.spacing, chess.spacing):
                    for row in range(chess.height_offset, chess.height - chess.height_offset + chess.spacing,
                                     chess.spacing):
                        ai_score = chess.get_score(col, row, False)
                        human_score = chess.get_score(col, row, True)
                        human_result.append([ai_score + human_score, col, row])
                human_result = sorted(human_result, key=lambda s: s[0], reverse=False)
                cnt = 0
                for i in range(len(human_result)):
                    if [human_result[i][1], human_result[i][2]] not in chess.human_press_history:
                        if [human_result[i][1], human_result[i][2]] not in chess.ai_press_history:
                            final_result.append(human_result[i])
                            cnt += 1
                            if cnt >= self.calc_num:
                                break
                print("human:", final_result)
                for i in range(len(final_result)):
                    chess.human_press_history.append([final_result[i][1], final_result[i][2]])
                    self.calc(chess, n - 1)
                    # self.calc_tree.append(final_result[i])
                    chess.human_press_history.pop()

        # if result[0][0] == 0:
        #     self.x = 100 + random.randint(6, 8) * 50
        #     self.y = 100 + random.randint(6, 8) * 50
        # else:
        #     for i in range(len(result)):
        #         if [result[i][1], result[i][2]] not in chess.human_press_history:
        #             if [result[i][1], result[i][2]] not in chess.ai_press_history:
        #                 self.x = result[i][1]
        #                 self.y = result[i][2]
        #                 break
        # self.x = 100 + random.randint(0, 12) * 50
        # self.y = 100 + random.randint(0, 12) * 50
        # result = chess.get_score(chess.human_press_history[-1][0], chess.human_press_history[-1][1], True)
        # print(f"active_five:{result[0]}\n"
        #       f"active_four:{result[1]}\n"
        #       f"sleep_four:{result[2]}\n"
        #       f"active_three:{result[3]}\n"
        #       f"sleep_three::{result[4]}\n"
        #       f"active_two:{result[5]}\n"
        #       f"sleep_two:{result[6]}\n")

    def judge(self, chess):

        if len(chess.human_press_history) == 0:
            self.x = 400
            self.y = 400
            self.calc_tree = []
        else:
            length = self.calc_depth
            while length > 0:
                if not ((self.calc_depth - length) % 2):
                    temp = []
                    max1 = 0
                    max_x = self.calc_tree[0][1]
                    max_y = self.calc_tree[0][2]
                    # TODO has problem if =0
                    for i in range(len(self.calc_tree)):

                        if self.calc_tree[i][0] > max1:
                            max1 = self.calc_tree[i][0]
                            max_x = self.calc_tree[i][1]
                            max_y = self.calc_tree[i][2]
                        if not (i + 1) % self.calc_num:
                            temp.append([max1, max_x, max_y])
                            max1 = 0
                    self.calc_tree = temp[:]
                else:
                    temp = []
                    min1 = 0
                    min_x = self.calc_tree[0][1]
                    min_y = self.calc_tree[0][2]
                    for i in range(len(self.calc_tree)):
                        if self.calc_tree[i][0] < min1:
                            min1 = self.calc_tree[i][0]
                            min_x = self.calc_tree[i][1]
                            min_y = self.calc_tree[i][2]
                        if not (i + 1) % self.calc_num:
                            temp.append([min1, min_x, min_y])
                            min1 = 0
                    self.calc_tree = temp[:]

                length -= 1

            self.x = self.calc_tree[0][1]
            self.y = self.calc_tree[0][2]
            self.calc_tree = []

    def play(self, chess):
        chess.ai_show_piece(self.x, self.y, self.color)
