import _tkinter


class Human:
    def __init__(self):
        self.color = "black" # color of chess

    def play(self, chess):
        """
            This function be used to play the chess
            :param chess: the chess
        """
        # catch the exception when the window be closed
        try:
            chess.chess.bind("<Button-1>", lambda event: chess.human_press_mouse(event, color=self.color))

        except _tkinter.TclError:
            chess.is_close = True


class AI:
    def __init__(self, depth):
        self.color = "white"
        self.x = 0
        self.y = 0
        self.calc_depth = depth if (depth % 2 == 1) else (depth - 1)  # the calculate depth
        self.going_step = []
        self.bottom_score = []
        self.calc_num = 3  # the calculate step

    def calc(self, chess, n):
        """
            This function be used to calculate where to play
            :param chess: the chess
            :param n: recursive variable
        """

        # version 0
        if chess.version == 0:
            # if ai first press the center
            if len(chess.human_press_history) == 0:
                self.x = 450
                self.y = 450
            else:
                # calculate the sum of the scores of the now step for own and the opponent
                result = []
                for col in range(chess.width_offset, chess.width - chess.width_offset + chess.spacing, chess.spacing):
                    for row in range(chess.height_offset, chess.height - chess.height_offset + chess.spacing,
                                     chess.spacing):
                        if [col, row] not in chess.human_press_history:
                            if [col, row] not in chess.ai_press_history:
                                ai_score = chess.get_now_step_score(col, row, False)
                                human_score = chess.get_now_step_score(col, row, True)
                                result.append([ai_score + human_score, col, row])
                # print("ai:", result)
                ai_result = max(result, key=lambda s: s[0])

                self.x = ai_result[1]
                self.y = ai_result[2]

        # version 1
        elif chess.version == 1:
            # if ai first press the center
            if len(chess.human_press_history) == 0:
                self.x = 450
                self.y = 450
            else:
                # if the first press,press the upper left corner
                if len(chess.ai_press_history) == 0:
                    self.x = chess.human_press_history[0][0] - 50
                    self.y = chess.human_press_history[0][1] - 50
                else:
                    if n > 0:
                        final_result = []
                        # if calculate ai
                        if not ((self.calc_depth - n) % 2):
                            ai_result = []
                            for col in range(chess.width_offset, chess.width - chess.width_offset + chess.spacing,
                                             chess.spacing):
                                for row in range(chess.height_offset,
                                                 chess.height - chess.height_offset + chess.spacing,
                                                 chess.spacing):
                                    if [col, row] not in chess.human_press_history:
                                        if [col, row] not in chess.ai_press_history:
                                            # append and calc then pop
                                            chess.ai_press_history.append([col, row])
                                            ai_score_future = chess.get_global_score(False)
                                            human_score_future = chess.get_global_score(True)
                                            chess.ai_press_history.pop()

                                            # calculate the score according to a certain percentage
                                            ai_result.append([ai_score_future - 5 * human_score_future,
                                                              col, row])
                            ai_result = sorted(ai_result, key=lambda s: s[0], reverse=True)

                            # get the required number of points
                            cnt = 0
                            for i in range(len(ai_result)):
                                final_result.append(ai_result[i])
                                cnt += 1
                                if cnt >= self.calc_num:
                                    break
                            print("ai:", final_result)

                            # append and recursion then pop
                            for i in range(len(final_result)):
                                chess.ai_press_history.append([final_result[i][1], final_result[i][2]])
                                self.calc(chess, n - 1)

                                # record the going step
                                if n == self.calc_depth:
                                    self.going_step.append(final_result[i])
                                # record the bottom data
                                if n == 1:
                                    self.bottom_score.append(final_result[i])

                                chess.ai_press_history.pop()

                        # if calculate human
                        else:
                            human_result = []
                            for col in range(chess.width_offset, chess.width - chess.width_offset + chess.spacing,
                                             chess.spacing):
                                for row in range(chess.height_offset,
                                                 chess.height - chess.height_offset + chess.spacing,
                                                 chess.spacing):
                                    if [col, row] not in chess.human_press_history:
                                        if [col, row] not in chess.ai_press_history:
                                            # append and calc then pop
                                            chess.human_press_history.append([col, row])
                                            ai_score_future = chess.get_global_score(False)
                                            human_score_future = chess.get_global_score(True)
                                            chess.human_press_history.pop()

                                            # calculate the score according to a certain percentage
                                            human_result.append([5 * ai_score_future - human_score_future,
                                                                 col, row])
                            human_result = sorted(human_result, key=lambda s: s[0], reverse=False)

                            # get the required number of points
                            cnt = 0
                            for i in range(len(human_result)):
                                final_result.append(human_result[i])
                                cnt += 1
                                if cnt >= self.calc_num:
                                    break
                            print("human:", final_result)

                            # append and recursion then pop
                            for i in range(len(final_result)):
                                chess.human_press_history.append([final_result[i][1], final_result[i][2]])
                                self.calc(chess, n - 1)
                                chess.human_press_history.pop()

                    # process the data after recursion
                    if n == self.calc_depth:
                        step = 0
                        length = self.calc_depth
                        # Minimax
                        while length > 0:
                            # max
                            if not ((self.calc_depth - length) % 2):
                                temp = []
                                max1 = float("-inf")
                                for i in range(len(self.bottom_score)):
                                    if self.bottom_score[i][0] > max1:
                                        max1 = self.bottom_score[i][0]
                                        step = i
                                    if not (i + 1) % self.calc_num:
                                        temp.append([max1, step])
                                        max1 = float("-inf")
                                self.bottom_score = temp[:]

                            # min
                            else:
                                temp = []
                                min1 = float("inf")
                                for i in range(len(self.bottom_score)):
                                    if self.bottom_score[i][0] < min1:
                                        min1 = self.bottom_score[i][0]
                                        step = i
                                    if not (i + 1) % self.calc_num:
                                        temp.append([min1, step])
                                        min1 = float("inf")
                                self.bottom_score = temp[:]

                            length -= 1

                        self.x = self.going_step[step][1]
                        self.y = self.going_step[step][2]

                        self.going_step = []
                        self.bottom_score = []

    def play(self, chess):
        """
            This function be used to play chess
            :param chess: the chess
        """

        # show the current chess
        if len(chess.ai_press_object) != 0:
            chess.chess.delete(chess.ai_press_object[-1])
        chess.ai_show_piece(self.x, self.y, self.color)
