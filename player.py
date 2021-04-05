import _tkinter
import math


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
        self.x = 0
        self.y = 0
        self.calc_depth = 1
        #  TODO if depth %2 ==0
        self.going_step = []
        self.bottom_score = []
        self.calc_num = 3  # 每一步棋计算最优前

        self.version = 1
        #  0 :Fast Think Current Situation simply
        #  1 :Slow Think Future Situation recursion

    def calc(self, chess, n):

        if self.version == 0:
            if len(chess.human_press_history) == 0:
                self.x = 450
                self.y = 450
            else:
                result = []
                for col in range(chess.width_offset, chess.width - chess.width_offset + chess.spacing, chess.spacing):
                    for row in range(chess.height_offset, chess.height - chess.height_offset + chess.spacing,
                                     chess.spacing):
                        if [col, row] not in chess.human_press_history:
                            if [col, row] not in chess.ai_press_history:
                                ai_score = chess.get_now_step_score(col, row, False)
                                human_score = chess.get_now_step_score(col, row, True)
                                result.append([ai_score + human_score, col, row])
                ai_result = max(result, key=lambda s: s[0])
                self.x = ai_result[1]
                self.y = ai_result[2]

        elif self.version == 1:
            if len(chess.human_press_history) == 0:
                self.x = 450
                self.y = 450
            else:
                if len(chess.ai_press_history) == 0:
                    self.x = chess.human_press_history[0][0] - 50
                    self.y = chess.human_press_history[0][1] - 50
                else:
                    if n > 0:
                        final_result = []
                        if not ((self.calc_depth - n) % 2):
                            ai_result = []
                            for col in range(chess.width_offset, chess.width - chess.width_offset + chess.spacing,
                                             chess.spacing):
                                for row in range(chess.height_offset,
                                                 chess.height - chess.height_offset + chess.spacing,
                                                 chess.spacing):
                                    if [col, row] not in chess.human_press_history:
                                        if [col, row] not in chess.ai_press_history:
                                            human_score_now = chess.get_global_score(True)
                                            chess.ai_press_history.append([col, row])
                                            ai_score = chess.get_global_score(False)
                                            human_score_future = chess.get_global_score(True)
                                            chess.ai_press_history.pop()
                                            # chess.ai_press_history.append([col, row])
                                            # ai_score = chess.get_global_score(False)
                                            # chess.ai_press_history.pop()
                                            # chess.human_press_history.append([col, row])
                                            # human_score = chess.get_global_score(True)
                                            # chess.human_press_history.pop()

                                            ai_result.append([ai_score + 3*(human_score_now-human_score_future), col, row])
                            ai_result = sorted(ai_result, key=lambda s: s[0], reverse=True)
                            print("test:", ai_result)
                            cnt = 0
                            for i in range(len(ai_result)):
                                final_result.append(ai_result[i])
                                cnt += 1
                                if cnt >= self.calc_num:
                                    break
                            # print("ai:", final_result)
                            for i in range(len(final_result)):
                                chess.ai_press_history.append([final_result[i][1], final_result[i][2]])
                                self.calc(chess, n - 1)

                                if n == self.calc_depth:
                                    self.going_step.append(final_result[i])
                                if n == 1:
                                    self.bottom_score.append(final_result[i])
                                chess.ai_press_history.pop()
                        else:
                            human_result = []
                            for col in range(chess.width_offset, chess.width - chess.width_offset + chess.spacing,
                                             chess.spacing):
                                for row in range(chess.height_offset,
                                                 chess.height - chess.height_offset + chess.spacing,
                                                 chess.spacing):
                                    if [col, row] not in chess.human_press_history:
                                        if [col, row] not in chess.ai_press_history:
                                            chess.human_press_history.append([col, row])
                                            ai_score = chess.get_global_score(False)
                                            human_score = chess.get_global_score(True)
                                            chess.human_press_history.pop()

                                            human_result.append([ai_score - 10 * human_score, col, row])
                            human_result = sorted(human_result, key=lambda s: s[0], reverse=False)
                            cnt = 0
                            for i in range(len(human_result)):
                                final_result.append(human_result[i])
                                cnt += 1
                                if cnt >= self.calc_num:
                                    break
                            print("human:", final_result)
                            for i in range(len(final_result)):
                                chess.human_press_history.append([final_result[i][1], final_result[i][2]])
                                self.calc(chess, n - 1)
                                # self.bottom_score.append(final_result[i])
                                chess.human_press_history.pop()

                    # 递归后进行操作
                    if n == self.calc_depth:

                        step = 0
                        length = self.calc_depth
                        while length > 0:
                            if not ((self.calc_depth - length) % 2):
                                temp = []
                                max1 = self.bottom_score[0][0]
                                # TODO has problem if =0
                                for i in range(len(self.bottom_score)):
                                    if self.bottom_score[i][0] > max1:
                                        max1 = self.bottom_score[i][0]
                                        step = i
                                    if not (i + 1) % self.calc_num:
                                        temp.append([max1, step])
                                        max1 = self.bottom_score[0][0]
                                self.bottom_score = temp[:]
                            else:
                                temp = []
                                min1 = self.bottom_score[0][0]
                                for i in range(len(self.bottom_score)):
                                    if self.bottom_score[i][0] < min1:
                                        min1 = self.bottom_score[i][0]
                                        step = i
                                    if not (i + 1) % self.calc_num:
                                        temp.append([min1, step])
                                        min1 = self.bottom_score[0][0]
                                self.bottom_score = temp[:]

                            length -= 1
                            # print(self.bottom_score)

                        # print(self.going_step)

                        self.x = self.going_step[math.floor(pow(step + 1, 1 / self.calc_depth)) - 1][1]
                        self.y = self.going_step[math.floor(pow(step + 1, 1 / self.calc_depth)) - 1][2]

                        self.going_step = []
                        self.bottom_score = []

    def play(self, chess):
        if len(chess.ai_press_object) != 0:
            chess.chess.delete(chess.ai_press_object[-1])
        chess.ai_show_piece(self.x, self.y, self.color)
