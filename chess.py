import tkinter as tk


class Chess:
    def __init__(self,version):
        # # param
        self.row, self.col = 15, 15
        self.width, self.height = 900, 900  # window size
        self.width_offset, self.height_offset = 100, 100  # offset between chessboard and window
        self.spacing = int((self.width - 2 * self.width_offset) / (self.col - 1))  # spacing between each line
        self.mouse_press_margin = 10  # the margin of mouse pressing
        self.ai_press_object = []
        self.now_step_score_dict = {"active_five": 50000,
                                    "active_four": 20000,
                                    "sleep_four": 2500,
                                    "active_three": 2000,
                                    "sleep_three": 1200,
                                    "active_two_1": 800,
                                    "active_two_2": 700,
                                    "sleep_two": 400}
        self.global_score_dict = {"active_five": 50000,
                                    "active_four": 20000,
                                    "sleep_four": 2500,
                                    "active_three": 2000,
                                    "sleep_three": 1200,
                                    "active_two_1": 800,
                                    "active_two_2": 700,
                                    "sleep_two": 400}

        self.version = version
        #  0 :Fast Think Current Situation simply
        #  1 :Slow Think Future Situation recursion

        self.ai_press_history = []
        self.human_press_history = []
        self.is_human_turn = True  # whether human play chess first
        self.human_win = False
        self.ai_win = False
        self.is_close = False

        # four types line be count
        self.count1 = 1  # --
        self.count2 = 1  # ||
        self.count3 = 1  # \\
        self.count4 = 1  # //

        # four types line be count history
        self.be_count1 = []  # --
        self.be_count2 = []  # ||
        self.be_count3 = []  # \\
        self.be_count4 = []  # //

        # # window
        self.window = tk.Tk()
        self.window.title("Gobang")
        self.window.geometry(str(self.width) + "x" + str(self.height))

        # # canvas
        # fill the background
        self.chess = tk.Canvas(self.window, bg="#CDC0B0", width=self.width, height=self.height)

        # draw the chessboard
        self.chess.create_rectangle(
            self.width_offset, self.height_offset,
            self.width - self.width_offset, self.height - self.height_offset,
            fill="#CDBA96")

        # draw the line
        width_step = int((self.width - 2 * self.width_offset) / (self.col - 1))
        for x in range(self.width_offset, self.width - self.width_offset + width_step, width_step):
            self.chess.create_line(x, self.height_offset,
                                   x, self.height - self.height_offset,
                                   fill="black", width=2)
            self.chess.create_line(self.width_offset, x,
                                   self.width - self.width_offset, x,
                                   fill="black", width=2)

        # draw the circle
        multiple = [[3, 3], [7, 7], [11, 3], [3, 11], [11, 11]]
        for i in range(len(multiple)):
            self.chess.create_oval(self.width_offset + multiple[i][0] * self.spacing - 5,
                                   self.height_offset + multiple[i][1] * self.spacing - 5,
                                   self.width_offset + multiple[i][0] * self.spacing + 5,
                                   self.height_offset + multiple[i][1] * self.spacing + 5,
                                   fill="black")

        # place
        self.chess.place(x=0, y=0, anchor="nw")

    def human_press_mouse(self, event, color):
        """
            This function be call if human press mouse
            :param event: tk <Button-1>
            :param color: the piece's color
        """
        if self.width_offset < event.x < self.width - self.width_offset:
            if self.height_offset < event.y < self.height - self.height_offset:
                # Leave a margin to press mouse
                x_remainder, y_remainder = event.x % self.spacing, event.y % self.spacing
                x_index, y_index = -1, -1
                # right
                if x_remainder < self.mouse_press_margin:
                    x_index = int(event.x - x_remainder)
                    if y_remainder < self.mouse_press_margin:
                        y_index = int(event.y - y_remainder)
                    if y_remainder > self.spacing - self.mouse_press_margin:
                        y_index = int(event.y + (self.spacing - y_remainder))
                # left
                if x_remainder > self.spacing - self.mouse_press_margin:
                    x_index = int(event.x + (self.spacing - x_remainder))
                    if y_remainder < self.mouse_press_margin:
                        y_index = int(event.y - y_remainder)
                    if y_remainder > self.spacing - self.mouse_press_margin:
                        y_index = int(event.y + (self.spacing - y_remainder))

                # Check to play
                if x_index != -1 and y_index != -1:
                    press = True
                    if not self.check_able_play(x_index, y_index):
                        press = False
                    if press:
                        self.chess.create_oval(x_index - 10, y_index - 10, x_index + 10, y_index + 10, fill=color)
                        self.human_press_history.append([x_index, y_index])
                        self.is_human_turn = False

    def ai_show_piece(self, x, y, color):
        """
            This function be used to show where ai play
            :param x: x index
            :param y: y index
            :param color: press color
        """
        press = True
        if not self.check_able_play(x, y):
            press = False
        if press:
            self.chess.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color)
            self.ai_press_object.append(self.chess.create_oval(x - 12, y - 12, x + 12, y + 12,
                                                                  outline="#A9A9A9", width=6))

            self.ai_press_history.append([x, y])
            self.is_human_turn = True

    def count_the_consequent(self, x, y, history):
        """
            This function be used to count a piece's consequent num
            :param x: x index
            :param y: y index
            :param history: whose history
            :return: the count of four line types
        """

        # "--" line type
        if [x, y] not in self.be_count1:
            self.be_count1 = []
            self.count1 = 1
            for i in range(1, 5, 1):
                if [x + self.spacing * i, y] in history:
                    self.be_count1.append([x + self.spacing * i, y])
                    self.count1 += 1
                else:
                    break
            for i in range(-1, -5, -1):
                if [x + self.spacing * i, y] in history:
                    self.be_count1.append([x + self.spacing * i, y])
                    self.count1 += 1
                else:
                    break

        # "||" line type
        if [x, y] not in self.be_count2:
            self.be_count2 = []
            self.count2 = 1
            for i in range(1, 5, 1):
                if [x, y + self.spacing * i] in history:
                    self.be_count2.append([x, y + self.spacing * i])
                    self.count2 += 1
                else:
                    break
            for i in range(-1, -5, -1):
                if [x, y + self.spacing * i] in history:
                    self.be_count2.append([x, y + self.spacing * i])
                    self.count2 += 1
                else:
                    break

        # "\\" line type
        if [x, y] not in self.be_count3:
            self.be_count3 = []
            self.count3 = 1
            for i in range(1, 5, 1):
                if [x + self.spacing * i, y + self.spacing * i] in history:
                    self.be_count3.append([x + self.spacing * i, y + self.spacing * i])
                    self.count3 += 1
                else:
                    break
            for i in range(-1, -5, -1):
                if [x + self.spacing * i, y + self.spacing * i] in history:
                    self.be_count3.append([x + self.spacing * i, y + self.spacing * i])
                    self.count3 += 1
                else:
                    break

        # "//" line type
        if [x, y] not in self.be_count4:
            self.be_count4 = []
            self.count4 = 1
            for i in range(1, 5, 1):
                if [x - self.spacing * i, y + self.spacing * i] in history:
                    self.be_count4.append([x - self.spacing * i, y + self.spacing * i])
                    self.count4 += 1
                else:
                    break
            for i in range(-1, -5, -1):
                if [x - self.spacing * i, y + self.spacing * i] in history:
                    self.be_count4.append([x - self.spacing * i, y + self.spacing * i])
                    self.count4 += 1
                else:
                    break

        return self.count1, self.count2, self.count3, self.count4

    def check_game_over(self):
        """
            This function be used to check game over
            :return: the result of checking
        """
        if len(self.ai_press_history) < 5 or len(self.human_press_history) < 5:
            return 0

        # if human play first,check human first
        if self.is_human_turn:
            for history in self.human_press_history:
                if max(self.count_the_consequent(history[0], history[1], self.human_press_history)) >= 5:
                    self.human_win = True
                    return 1
            for history in self.ai_press_history:
                if max(self.count_the_consequent(history[0], history[1], self.ai_press_history)) >= 5:
                    self.ai_win = True
                    return 1
        # if ai play first,check ai first
        else:
            for history in self.ai_press_history:
                if max(self.count_the_consequent(history[0], history[1], self.ai_press_history)) >= 5:
                    self.ai_win = True
                    return 1
            for history in self.human_press_history:
                if max(self.count_the_consequent(history[0], history[1], self.human_press_history)) >= 5:
                    self.human_win = True
                    return 1

        return 0

    def check_able_play(self, x, y):
        """
            This function be used to check out of windows or be pressed once
            :return: the result of checking
        """
        press_history = self.human_press_history + self.ai_press_history
        for history in press_history:
            if x == history[0] and y == history[1]:
                return 0
        return 1

    def show_result(self):
        """
            This function be used to show the match result
        """
        text = ""
        if self.ai_win:
            text = "AI win"
        elif self.human_win:
            text = "Human win"
        label = tk.Label(self.window, text=text, bg="SlateGray", font=("微软雅黑", 40))
        label.pack()

    def get_situation(self, x, y, is_human):
        """
            This function be used to calc a piece's score
            :param x: x index
            :param y: y index
            :param is_human: calc human or not
            :return: the result of calcing
        """

        if is_human:
            own = self.human_press_history[:]
        else:
            own = self.ai_press_history[:]

        # If it is calculated, it will not be calculated
        line_be_count = {r"--": False,
                         r"||": False,
                         r"\\": False,
                         r"//": False}

        # calc the consequent
        count1, count2, count3, count4 = \
            self.count_the_consequent(x, y, own)

        # * means own piece
        # @ means opponent piece
        # _ means empty

        # 连五 (*****)
        active_five = 0

        # 活四 (_****_)
        active_four = 0

        # 冲四
        # (_****@) (*_***) (**_**)
        sleep_four = 0

        # 活三
        # (_***_) (_*_**_)
        active_three = 0

        # 眠三
        # (__***@) (_*_**@) (_**_*@) (*__**) (*_*_*) (@_***_@)
        sleep_three = 0

        # 活二
        # (__**__) (_*_*_) (_*__*_)
        active_two_1 = 0
        active_two_2 = 0

        # 眠二
        # (___**@) (__*_*@) (_*__*@) (*___*)
        sleep_two = 0

        # five
        if count1 == 5:
            active_five += 1
            line_be_count[r"--"] = True
        if count2 == 5:
            active_five += 1
            line_be_count[r"||"] = True
        if count3 == 5:
            active_five += 1
            line_be_count[r"\\"] = True
        if count4 == 5:
            active_five += 1
            line_be_count[r"//"] = True

        # four
        # --
        if not line_be_count[r"--"]:
            if count1 == 4:
                press = self.be_count1[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                active4 = self.calc_count4(x, y, press, line_type=r"--", is_human=is_human)[0]
                sleep4 = self.calc_count4(x, y, press, line_type=r"--", is_human=is_human)[1]
                if active4 or sleep4:
                    line_be_count[r"--"] = True
                    if active4:
                        active_four += active4
                    elif sleep4:
                        sleep_four += sleep4
        # ||
        if not line_be_count[r"||"]:
            if count2 == 4:
                press = self.be_count2[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[1])
                active4 = self.calc_count4(x, y, press, line_type=r"||", is_human=is_human)[0]
                sleep4 = self.calc_count4(x, y, press, line_type=r"||", is_human=is_human)[1]
                if active4 or sleep4:
                    line_be_count[r"||"] = True
                    if active4:
                        active_four += active4
                    elif sleep4:
                        sleep_four += sleep4
        # \\
        if not line_be_count[r"\\"]:
            if count3 == 4:
                press = self.be_count3[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                active4 = self.calc_count4(x, y, press, line_type=r"\\", is_human=is_human)[0]
                sleep4 = self.calc_count4(x, y, press, line_type=r"\\", is_human=is_human)[1]
                if active4 or sleep4:
                    line_be_count[r"\\"] = True
                    if active4:
                        active_four += active4
                    elif sleep4:
                        sleep_four += sleep4
        # //
        if not line_be_count[r"//"]:
            if count4 == 4:
                press = self.be_count4[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                active4 = self.calc_count4(x, y, press, line_type=r"//", is_human=is_human)[0]
                sleep4 = self.calc_count4(x, y, press, line_type=r"//", is_human=is_human)[1]
                if active4 or sleep4:
                    line_be_count[r"//"] = True
                    if active4:
                        active_four += active4
                    elif sleep4:
                        sleep_four += sleep4

        # three
        # --
        if not line_be_count[r"--"]:
            if count1 == 3:
                press = self.be_count1[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count3(x, y, press, line_type=r"--", is_human=is_human)[0]
                active3 = self.calc_count3(x, y, press, line_type=r"--", is_human=is_human)[1]
                sleep3 = self.calc_count3(x, y, press, line_type=r"--", is_human=is_human)[2]
                sleep2 = self.calc_count3(x, y, press, line_type=r"--", is_human=is_human)[3]
                if sleep4 or active3 or sleep3 or sleep2:
                    line_be_count[r"--"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif sleep2:
                        sleep_two += sleep2

        # ||
        if not line_be_count[r"||"]:
            if count2 == 3:
                press = self.be_count2[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[1])
                sleep4 = self.calc_count3(x, y, press, line_type=r"||", is_human=is_human)[0]
                active3 = self.calc_count3(x, y, press, line_type=r"||", is_human=is_human)[1]
                sleep3 = self.calc_count3(x, y, press, line_type=r"||", is_human=is_human)[2]
                sleep2 = self.calc_count3(x, y, press, line_type=r"||", is_human=is_human)[3]
                if sleep4 or active3 or sleep3 or sleep2:
                    line_be_count[r"||"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif sleep2:
                        sleep_two += sleep2
        # \\
        if not line_be_count[r"\\"]:
            if count3 == 3:
                press = self.be_count3[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count3(x, y, press, line_type=r"\\", is_human=is_human)[0]
                active3 = self.calc_count3(x, y, press, line_type=r"\\", is_human=is_human)[1]
                sleep3 = self.calc_count3(x, y, press, line_type=r"\\", is_human=is_human)[2]
                sleep2 = self.calc_count3(x, y, press, line_type=r"\\", is_human=is_human)[3]
                if sleep4 or active3 or sleep3 or sleep2:
                    line_be_count[r"\\"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif sleep2:
                        sleep_two += sleep2
        # //
        if not line_be_count[r"//"]:
            if count4 == 3:
                press = self.be_count4[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count3(x, y, press, line_type=r"//", is_human=is_human)[0]
                active3 = self.calc_count3(x, y, press, line_type=r"//", is_human=is_human)[1]
                sleep3 = self.calc_count3(x, y, press, line_type=r"//", is_human=is_human)[2]
                sleep2 = self.calc_count3(x, y, press, line_type=r"//", is_human=is_human)[3]
                if sleep4 or active3 or sleep3 or sleep2:
                    line_be_count[r"//"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif sleep2:
                        sleep_two += sleep2

        # two
        # --
        if not line_be_count[r"--"]:
            if count1 == 2:
                press = self.be_count1[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count2(x, y, press, line_type=r"--", is_human=is_human)[0]
                active3 = self.calc_count2(x, y, press, line_type=r"--", is_human=is_human)[1]
                sleep3 = self.calc_count2(x, y, press, line_type=r"--", is_human=is_human)[2]
                active2 = self.calc_count2(x, y, press, line_type=r"--", is_human=is_human)[3]
                sleep2 = self.calc_count2(x, y, press, line_type=r"--", is_human=is_human)[4]
                if sleep4 or active3 or sleep3 or active2 or sleep2:
                    line_be_count[r"--"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif active2:
                        active_two_1 += active2
                    elif sleep2:
                        sleep_two += sleep2
        # ||
        if not line_be_count[r"||"]:
            if count2 == 2:
                press = self.be_count2[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[1])
                sleep4 = self.calc_count2(x, y, press, line_type=r"||", is_human=is_human)[0]
                active3 = self.calc_count2(x, y, press, line_type=r"||", is_human=is_human)[1]
                sleep3 = self.calc_count2(x, y, press, line_type=r"||", is_human=is_human)[2]
                active2 = self.calc_count2(x, y, press, line_type=r"||", is_human=is_human)[3]
                sleep2 = self.calc_count2(x, y, press, line_type=r"||", is_human=is_human)[4]
                if sleep4 or active3 or sleep3 or active2 or sleep2:
                    line_be_count[r"||"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif active2:
                        active_two_1 += active2
                    elif sleep2:
                        sleep_two += sleep2
        # \\
        if not line_be_count[r"\\"]:
            if count3 == 2:
                press = self.be_count3[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count2(x, y, press, line_type=r"\\", is_human=is_human)[0]
                active3 = self.calc_count2(x, y, press, line_type=r"\\", is_human=is_human)[1]
                sleep3 = self.calc_count2(x, y, press, line_type=r"\\", is_human=is_human)[2]
                active2 = self.calc_count2(x, y, press, line_type=r"\\", is_human=is_human)[3]
                sleep2 = self.calc_count2(x, y, press, line_type=r"\\", is_human=is_human)[4]
                if sleep4 or active3 or sleep3 or active2 or sleep2:
                    line_be_count[r"\\"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif active2:
                        active_two_1 += active2
                    elif sleep2:
                        sleep_two += sleep2
        # //
        if not line_be_count[r"//"]:
            if count4 == 2:
                press = self.be_count4[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count2(x, y, press, line_type=r"//", is_human=is_human)[0]
                active3 = self.calc_count2(x, y, press, line_type=r"//", is_human=is_human)[1]
                sleep3 = self.calc_count2(x, y, press, line_type=r"//", is_human=is_human)[2]
                active2 = self.calc_count2(x, y, press, line_type=r"//", is_human=is_human)[3]
                sleep2 = self.calc_count2(x, y, press, line_type=r"//", is_human=is_human)[4]
                if sleep4 or active3 or sleep3 or active2 or sleep2:
                    line_be_count[r"//"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif active2:
                        active_two_1 += active2
                    elif sleep2:
                        sleep_two += sleep2
        # one
        # --
        if not line_be_count[r"--"]:
            if count1 == 1:
                press = self.be_count1[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count1(x, y, press, line_type=r"--", is_human=is_human)[0]
                active3 = self.calc_count1(x, y, press, line_type=r"--", is_human=is_human)[1]
                sleep3 = self.calc_count1(x, y, press, line_type=r"--", is_human=is_human)[2]
                active2 = self.calc_count1(x, y, press, line_type=r"--", is_human=is_human)[3]
                sleep2 = self.calc_count1(x, y, press, line_type=r"--", is_human=is_human)[4]
                if sleep4 or active3 or sleep3 or active2 or sleep2:
                    line_be_count[r"--"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif active2:
                        active_two_2 += active2
                    elif sleep2:
                        sleep_two += sleep2
        # ||
        if not line_be_count[r"||"]:
            if count2 == 1:
                press = self.be_count2[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[1])
                sleep4 = self.calc_count1(x, y, press, line_type=r"||", is_human=is_human)[0]
                active3 = self.calc_count1(x, y, press, line_type=r"||", is_human=is_human)[1]
                sleep3 = self.calc_count1(x, y, press, line_type=r"||", is_human=is_human)[2]
                active2 = self.calc_count1(x, y, press, line_type=r"||", is_human=is_human)[3]
                sleep2 = self.calc_count1(x, y, press, line_type=r"||", is_human=is_human)[4]
                if sleep4 or active3 or sleep3 or active2 or sleep2:
                    line_be_count[r"||"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif active2:
                        active_two_2 += active2
                    elif sleep2:
                        sleep_two += sleep2
        # \\
        if not line_be_count[r"\\"]:
            if count3 == 1:
                press = self.be_count3[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count1(x, y, press, line_type=r"\\", is_human=is_human)[0]
                active3 = self.calc_count1(x, y, press, line_type=r"\\", is_human=is_human)[1]
                sleep3 = self.calc_count1(x, y, press, line_type=r"\\", is_human=is_human)[2]
                active2 = self.calc_count1(x, y, press, line_type=r"\\", is_human=is_human)[3]
                sleep2 = self.calc_count1(x, y, press, line_type=r"\\", is_human=is_human)[4]
                if sleep4 or active3 or sleep3 or active2 or sleep2:
                    line_be_count[r"\\"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif active2:
                        active_two_2 += active2
                    elif sleep2:
                        sleep_two += sleep2
        # //
        if not line_be_count[r"//"]:
            if count4 == 1:
                press = self.be_count4[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count1(x, y, press, line_type=r"//", is_human=is_human)[0]
                active3 = self.calc_count1(x, y, press, line_type=r"//", is_human=is_human)[1]
                sleep3 = self.calc_count1(x, y, press, line_type=r"//", is_human=is_human)[2]
                active2 = self.calc_count1(x, y, press, line_type=r"//", is_human=is_human)[3]
                sleep2 = self.calc_count1(x, y, press, line_type=r"//", is_human=is_human)[4]
                if sleep4 or active3 or sleep3 or active2 or sleep2:
                    line_be_count[r"//"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
                    elif active2:
                        active_two_2 += active2
                    elif sleep2:
                        sleep_two += sleep2

        return (active_five,
                active_four, sleep_four,
                active_three, sleep_three,
                active_two_1, active_two_2, sleep_two)

        # score = active_five * 50000 + \
        #         active_four * 20000 + \
        #         sleep_four * 2500 + \
        #         active_three * 2000 + \
        #         sleep_three * 1200 + \
        #         active_two_1 * 800 + \
        #         active_two_2 * 700 + \
        #         sleep_two * 400

    def get_now_step_score(self, x, y, is_human):
        situation = self.get_situation(x, y, is_human)
        score = situation[0] * self.now_step_score_dict["active_five"] + \
                situation[1] * self.now_step_score_dict["active_four"] + \
                situation[2] * self.now_step_score_dict["sleep_four"] + \
                situation[3] * self.now_step_score_dict["active_three"] + \
                situation[4] * self.now_step_score_dict["sleep_three"] + \
                situation[5] * self.now_step_score_dict["active_two_1"] + \
                situation[6] * self.now_step_score_dict["active_two_2"] + \
                situation[7] * self.now_step_score_dict["sleep_two"]
        return score

    def get_global_score(self, is_human):

        if is_human:
            own = self.human_press_history[:]
        else:
            own = self.ai_press_history[:]

        active_five = 0
        active_four = 0
        sleep_four = 0
        active_three = 0
        sleep_three = 0
        active_two_1 = 0
        active_two_2 = 0
        sleep_two = 0

        # TODO 重复计数
        for i in range(len(own)):
            situation = self.get_situation(own[i][0], own[i][1], is_human)
            active_five += situation[0]
            active_four += situation[1]
            sleep_four += situation[2]
            active_three += situation[3]
            sleep_three += situation[4]
            active_two_1 += situation[5]
            active_two_2 += situation[6]
            sleep_two += situation[7]



        score = active_five * self.global_score_dict["active_five"] / 5 + \
                active_four * self.global_score_dict["active_four"] / 4 + \
                sleep_four * self.global_score_dict["sleep_four"] / 4 + \
                active_three * self.global_score_dict["active_three"] / 3 + \
                sleep_three * self.global_score_dict["sleep_three"] / 3 + \
                active_two_1 * self.global_score_dict["active_two_1"] / 2 + \
                active_two_2 * self.global_score_dict["active_two_2"] / 2 + \
                sleep_two * self.global_score_dict["sleep_two"] / 2
        # if score ==1100:
        #     print("ai",active_five,active_four,sleep_four,active_three,sleep_three,active_two_1,active_two_2,sleep_two)
        # if score ==2200:
        #     print("human",active_five,active_four,sleep_four,active_three,sleep_three,active_two_1,active_two_2,sleep_two)
        # if score ==1300:
        #     print("ai",active_five,active_four,sleep_four,active_three,sleep_three,active_two_1,active_two_2,sleep_two)
        # if score ==2400:
        #     print("human",active_five,active_four,sleep_four,active_three,sleep_three,active_two_1,active_two_2,sleep_two)

        # # 冲四
        # # (_****@) (*_***) (**_**)
        # sleep_four = 0
        #
        # # 活三
        # # (_***_) (_*_**_)
        # active_three = 0
        #
        # # 眠三
        # # (__***@) (_*_**@) (_**_*@) (*__**) (*_*_*) (@_***_@)
        # sleep_three = 0
        #
        # # 活二
        # # (__**__) (_*_*_) (_*__*_)
        # active_two_1 = 0
        # active_two_2 = 0
        #
        # # 眠二
        # # (___**@) (__*_*@) (_*__*@) (*___*)
        # sleep_two = 0

        return score

    def is_block(self, x, y, history):

        if [x, y] in history:
            return 1
        if x < self.width_offset or x > self.width - self.width_offset:
            return 1
        if y < self.height_offset or y > self.height - self.height_offset:
            return 1
        return 0

    def calc_count4(self, x, y, press, line_type, is_human):
        index_head_first = self.line_type2index(x, y, press, line_type, is_head=True, num=1)
        index_tail_first = self.line_type2index(x, y, press, line_type, is_head=False, num=1)

        active_four = 0
        sleep_four = 0

        if is_human:
            own = self.human_press_history[:]
            opponent = self.ai_press_history[:]
        else:
            own = self.ai_press_history[:]
            opponent = self.human_press_history[:]

        # (_****_)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                active_four += 1

        # (_****@)
        if self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                sleep_four += 1
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                sleep_four += 1

        return active_four, sleep_four

    def calc_count3(self, x, y, press, line_type, is_human):

        index_head_first = self.line_type2index(x, y, press, line_type, is_head=True, num=1)
        index_tail_first = self.line_type2index(x, y, press, line_type, is_head=False, num=1)
        index_head_second = self.line_type2index(x, y, press, line_type, is_head=True, num=2)
        index_tail_second = self.line_type2index(x, y, press, line_type, is_head=False, num=2)

        sleep_four = 0
        active_three = 0
        sleep_three = 0
        sleep_two = 0
        if is_human:
            own = self.human_press_history[:]
            opponent = self.ai_press_history[:]
        else:
            own = self.ai_press_history[:]
            opponent = self.human_press_history[:]

        # (_***_)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                active_three += 1
        # (*_***)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if [index_head_second[0], index_head_second[1]] in own:
                sleep_four += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if [index_tail_second[0], index_tail_second[1]] in own:
                sleep_four += 1
        # (__***@)
        if self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                    sleep_three += 1
        if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                    sleep_three += 1
        # (@_***_@)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if self.is_block(index_head_second[0], index_head_second[1], opponent):
                if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                    if self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                        sleep_three += 1
        # (@_***@)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if self.is_block(index_head_second[0], index_head_second[1], opponent):
                if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                    sleep_two += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                if self.is_block(index_head_first[0], index_head_first[1], opponent):
                    sleep_two += 1
        # (@***@)
        if self.is_block(index_head_first[0], index_head_first[1], opponent):
            if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                sleep_two += 1

        return sleep_four, active_three, sleep_three, sleep_two

    def calc_count2(self, x, y, press, line_type, is_human):
        index_head_first = self.line_type2index(x, y, press, line_type, is_head=True, num=1)
        index_tail_first = self.line_type2index(x, y, press, line_type, is_head=False, num=1)
        index_head_second = self.line_type2index(x, y, press, line_type, is_head=True, num=2)
        index_tail_second = self.line_type2index(x, y, press, line_type, is_head=False, num=2)
        index_head_third = self.line_type2index(x, y, press, line_type, is_head=True, num=3)
        index_tail_third = self.line_type2index(x, y, press, line_type, is_head=False, num=3)

        sleep_four = 0
        active_three = 0
        sleep_three = 0
        active_two = 0
        sleep_two = 0

        if is_human:
            own = self.human_press_history[:]
            opponent = self.ai_press_history[:]
        else:
            own = self.ai_press_history[:]
            opponent = self.human_press_history[:]

        # (**_**)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if [index_head_second[0], index_head_second[1]] in own:
                if [index_head_third[0], index_head_third[1]] in own:
                    sleep_four += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if [index_tail_second[0], index_tail_second[1]] in own:
                if [index_tail_third[0], index_tail_third[1]] in own:
                    sleep_four += 1
        # (_*_**_)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if [index_tail_second[0], index_tail_second[1]] in own:
                    if not self.is_block(index_tail_third[0], index_tail_third[1], opponent):
                        active_three += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if [index_head_second[0], index_head_second[1]] in own:
                    if not self.is_block(index_head_third[0], index_head_third[1], opponent):
                        active_three += 1
        # (_*_**@)
        if self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if [index_tail_second[0], index_tail_second[1]] in own:
                    if not self.is_block(index_tail_third[0], index_tail_third[1], opponent):
                        sleep_three += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if [index_head_second[0], index_head_second[1]] in own:
                    if not self.is_block(index_head_third[0], index_head_third[1], opponent):
                        sleep_three += 1
        # (_**_*@)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if [index_tail_second[0], index_tail_second[1]] in own:
                    if self.is_block(index_tail_third[0], index_tail_third[1], opponent):
                        sleep_three += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if [index_head_second[0], index_head_second[1]] in own:
                    if self.is_block(index_head_third[0], index_head_third[1], opponent):
                        sleep_three += 1
        #  (*__**)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                if [index_head_third[0], index_head_third[1]] in own:
                    sleep_three += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                if [index_tail_third[0], index_tail_third[1]] in own:
                    sleep_three += 1

        # (__**__)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                    if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                        active_two += 1
        # (___**@)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                if not self.is_block(index_head_third[0], index_head_third[1], opponent):
                    if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                        sleep_two += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                if not self.is_block(index_tail_third[0], index_tail_third[1], opponent):
                    if self.is_block(index_head_first[0], index_head_first[1], opponent):
                        sleep_two += 1

        # (__**_@)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                    if self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                        active_two += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                    if self.is_block(index_head_second[0], index_head_second[1], opponent):
                        active_two += 1

        return (sleep_four,
                active_three, sleep_three,
                active_two, sleep_two)

    def calc_count1(self, x, y, press, line_type, is_human):

        index_head_first = self.line_type2index(x, y, press, line_type, is_head=True, num=1)
        index_tail_first = self.line_type2index(x, y, press, line_type, is_head=False, num=1)
        index_head_second = self.line_type2index(x, y, press, line_type, is_head=True, num=2)
        index_tail_second = self.line_type2index(x, y, press, line_type, is_head=False, num=2)
        index_head_third = self.line_type2index(x, y, press, line_type, is_head=True, num=3)
        index_tail_third = self.line_type2index(x, y, press, line_type, is_head=False, num=3)
        index_head_fourth = self.line_type2index(x, y, press, line_type, is_head=True, num=4)
        index_tail_fourth = self.line_type2index(x, y, press, line_type, is_head=False, num=4)

        sleep_four = 0
        active_three = 0
        sleep_three = 0
        active_two = 0
        sleep_two = 0

        if is_human:
            own = self.human_press_history[:]
            opponent = self.ai_press_history[:]
        else:
            own = self.ai_press_history[:]
            opponent = self.human_press_history[:]

        # (*_*_*)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if [index_head_second[0], index_head_second[1]] in own:
                if not self.is_block(index_head_third[0], index_head_third[1], opponent):
                    if [index_head_fourth[0], index_head_fourth[1]] in own:
                        sleep_three += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if [index_tail_second[0], index_tail_second[1]] in own:
                if not self.is_block(index_tail_third[0], index_tail_third[1], opponent):
                    if [index_tail_fourth[0], index_tail_fourth[1]] in own:
                        sleep_three += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if [index_tail_second[0], index_tail_second[1]] in own:
                if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                    if [index_head_second[0], index_head_second[1]] in own:
                        sleep_three += 1

        # (_*_*_)
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if [index_head_second[0], index_head_second[1]] in own:
                    if not self.is_block(index_head_third[0], index_head_third[1], opponent):
                        active_two += 1
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if [index_tail_second[0], index_tail_second[1]] in own:
                    if not self.is_block(index_tail_third[0], index_tail_third[1], opponent):
                        active_two += 1

        # (_*__*_)
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                    if [index_head_third[0], index_head_third[1]] in own:
                        if not self.is_block(index_head_fourth[0], index_head_fourth[1], opponent):
                            active_two += 1
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                    if [index_tail_third[0], index_tail_third[1]] in own:
                        if not self.is_block(index_tail_fourth[0], index_tail_fourth[1], opponent):
                            active_two += 1
        # (__*_*@)
        if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if [index_head_second[0], index_head_second[1]] in own:
                    if not self.is_block(index_head_third[0], index_head_third[1], opponent):
                        if not self.is_block(index_head_fourth[0], index_head_fourth[1], opponent):
                            sleep_two += 1
        if self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if [index_tail_second[0], index_tail_second[1]] in own:
                    if not self.is_block(index_tail_third[0], index_tail_third[1], opponent):
                        if not self.is_block(index_tail_fourth[0], index_tail_fourth[1], opponent):
                            sleep_two += 1
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                    if [index_tail_second[0], index_tail_second[1]] in own:
                        if self.is_block(index_tail_third[0], index_tail_third[1], opponent):
                            sleep_two += 1
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if [index_head_second[0], index_head_second[1]] in own:
                if self.is_block(index_head_third[0], index_head_third[1], opponent):
                    if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                        if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                            sleep_two += 1

        # (_*__*@)
        if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                    if [index_head_third[0], index_head_third[1]] in own:
                        if not self.is_block(index_head_fourth[0], index_head_fourth[1], opponent):
                            sleep_two += 1

        if self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                    if [index_tail_third[0], index_tail_third[1]] in own:
                        if not self.is_block(index_tail_fourth[0], index_tail_fourth[1], opponent):
                            sleep_two += 1
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                    if [index_tail_third[0], index_tail_third[1]] in own:
                        if self.is_block(index_tail_fourth[0], index_tail_fourth[1], opponent):
                            sleep_two += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                    if [index_head_third[0], index_head_third[1]] in own:
                        if self.is_block(index_head_fourth[0], index_head_fourth[1], opponent):
                            sleep_two += 1

        # (*___*)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                if not self.is_block(index_head_third[0], index_head_third[1], opponent):
                    if [index_head_fourth[0], index_head_fourth[1]] in own:
                        sleep_two += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                if not self.is_block(index_tail_third[0], index_tail_third[1], opponent):
                    if [index_tail_fourth[0], index_tail_fourth[1]] in own:
                        sleep_two += 1

        # (*_***)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if [index_head_second[0], index_head_second[1]] in own:
                if [index_head_third[0], index_head_third[1]] in own:
                    if [index_head_fourth[0], index_head_fourth[1]] in own:
                        sleep_four += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if [index_tail_second[0], index_tail_second[1]] in own:
                if [index_tail_third[0], index_tail_third[1]] in own:
                    if [index_tail_fourth[0], index_tail_fourth[1]] in own:
                        sleep_four += 1

        # (_*_**_)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if [index_tail_second[0], index_tail_second[1]] in own:
                    if [index_tail_third[0], index_tail_third[1]] in own:
                        if not self.is_block(index_tail_fourth[0], index_tail_fourth[1], opponent):
                            active_three += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if [index_head_second[0], index_head_second[1]] in own:
                    if [index_head_third[0], index_head_third[1]] in own:
                        if not self.is_block(index_head_fourth[0], index_head_fourth[1], opponent):
                            active_three += 1

        # (_*_**@)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if [index_tail_second[0], index_tail_second[1]] in own:
                    if [index_tail_third[0], index_tail_third[1]] in own:
                        if self.is_block(index_tail_fourth[0], index_tail_fourth[1], opponent):
                            sleep_three += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if [index_head_second[0], index_head_second[1]] in own:
                    if [index_head_third[0], index_head_third[1]] in own:
                        if self.is_block(index_head_fourth[0], index_head_fourth[1], opponent):
                            sleep_three += 1

        # (_**_*@)
        if self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if [index_tail_second[0], index_tail_second[1]] in own:
                    if [index_tail_third[0], index_tail_third[1]] in own:
                        if not self.is_block(index_tail_fourth[0], index_tail_fourth[1], opponent):
                            sleep_three += 1
        if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_head_first[0], index_head_first[1], opponent):
                if [index_head_second[0], index_head_second[1]] in own:
                    if [index_head_third[0], index_head_third[1]] in own:
                        if not self.is_block(index_head_fourth[0], index_head_fourth[1], opponent):
                            sleep_three += 1
        # (*__**)
        if not self.is_block(index_head_first[0], index_head_first[1], opponent):
            if not self.is_block(index_head_second[0], index_head_second[1], opponent):
                if [index_head_third[0], index_head_third[1]] in own:
                    if [index_head_fourth[0], index_head_fourth[1]] in own:
                        sleep_three += 1
        if not self.is_block(index_tail_first[0], index_tail_first[1], opponent):
            if not self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                if [index_tail_third[0], index_tail_third[1]] in own:
                    if [index_tail_fourth[0], index_tail_fourth[1]] in own:
                        sleep_three += 1

        # 由于递归版本考虑到全局 对于对方单子fang shou考虑不全 需要另外添加
        if self.version == 1:
            # (*@)
            if self.is_block(index_head_first[0], index_head_first[1], opponent):
                sleep_two += 1
            if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                sleep_two += 1

            # (*@@)
            if self.is_block(index_head_first[0], index_head_first[1], opponent):
                if self.is_block(index_head_second[0], index_head_second[1], opponent):
                    sleep_two += 1
            if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                    sleep_two += 1

            # (*@@@)
            if self.is_block(index_head_first[0], index_head_first[1], opponent):
                if self.is_block(index_head_second[0], index_head_second[1], opponent):
                    if self.is_block(index_head_third[0], index_head_third[1], opponent):
                        sleep_three += 1
            if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                    if self.is_block(index_tail_third[0], index_tail_third[1], opponent):
                        sleep_three += 1

            # (@*@)
            if self.is_block(index_head_first[0], index_head_first[1], opponent):
                if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                    sleep_two += 1

            # (@*@@)
            if self.is_block(index_head_first[0], index_head_first[1], opponent):
                if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                    if self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                        sleep_three += 1
            if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if self.is_block(index_head_first[0], index_head_first[1], opponent):
                    if self.is_block(index_head_second[0], index_head_second[1], opponent):
                        sleep_three += 1

            # (@@*@@)
            if self.is_block(index_head_first[0], index_head_first[1], opponent):
                if self.is_block(index_head_second[0], index_head_second[1], opponent):
                    if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                        if self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                            sleep_four += 1
            if self.is_block(index_tail_first[0], index_tail_first[1], opponent):
                if self.is_block(index_tail_second[0], index_tail_second[1], opponent):
                    if self.is_block(index_head_first[0], index_head_first[1], opponent):
                        if self.is_block(index_head_second[0], index_head_second[1], opponent):
                            sleep_three += 1


        return (sleep_four,
                active_three, sleep_three,
                active_two, sleep_two)

    def line_type2index(self, x, y, press, line_type, is_head, num):
        index = []
        if line_type == r"--":
            if is_head:
                index = [press[0][0] - num * self.spacing, y]
            else:
                index = [press[-1][0] + num * self.spacing, y]

        if line_type == r"||":
            if is_head:
                index = [x, press[0][1] - num * self.spacing]
            else:
                index = [x, press[-1][1] + num * self.spacing]

        if line_type == r"\\":
            if is_head:
                index = [press[0][0] - num * self.spacing, press[0][1] - num * self.spacing]
            else:
                index = [press[-1][0] + num * self.spacing, press[-1][1] + num * self.spacing]

        if line_type == r"//":
            if is_head:
                index = [press[0][0] - num * self.spacing, press[0][1] + num * self.spacing]
            else:
                index = [press[-1][0] + num * self.spacing, press[-1][1] - num * self.spacing]

        return index
