import tkinter as tk
from operator import itemgetter


class Chess:
    def __init__(self):
        # # param
        self.row, self.col = 15, 15
        self.width, self.height = 900, 900  # window size
        self.width_offset, self.height_offset = 100, 100  # offset between chessboard and window
        self.spacing = int((self.width - 2 * self.width_offset) / (self.col - 1))  # spacing between each line
        self.ai_press_history = []
        self.human_press_history = []
        self.is_human_turn = False  # 先手
        self.human_win = False
        self.ai_win = False
        self.is_close = False

        self.count1 = 1
        self.count2 = 1
        self.count3 = 1
        self.count4 = 1
        self.be_count1 = []
        self.be_count2 = []
        self.be_count3 = []
        self.be_count4 = []

        # # window
        self.window = tk.Tk()
        self.window.title = "Gobang"
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
                                   fill="black", width=4)
            self.chess.create_line(self.width_offset, x,
                                   self.width - self.width_offset, x,
                                   fill="black", width=4)
        # draw the circle
        self.chess.create_oval(self.width_offset + 3 * self.spacing - 5,
                               self.height_offset + 3 * self.spacing - 5,
                               self.width_offset + 3 * self.spacing + 5,
                               self.height_offset + 3 * self.spacing + 5,
                               fill="black")
        self.chess.create_oval(self.width_offset + 7 * self.spacing - 5,
                               self.height_offset + 7 * self.spacing - 5,
                               self.width_offset + 7 * self.spacing + 5,
                               self.height_offset + 7 * self.spacing + 5,
                               fill="black")
        self.chess.create_oval(self.width_offset + 11 * self.spacing - 5,
                               self.height_offset + 3 * self.spacing - 5,
                               self.width_offset + 11 * self.spacing + 5,
                               self.height_offset + 3 * self.spacing + 5,
                               fill="black")
        self.chess.create_oval(self.width_offset + 3 * self.spacing - 5,
                               self.height_offset + 11 * self.spacing - 5,
                               self.width_offset + 3 * self.spacing + 5,
                               self.height_offset + 11 * self.spacing + 5,
                               fill="black")
        self.chess.create_oval(self.width_offset + 11 * self.spacing - 5,
                               self.height_offset + 11 * self.spacing - 5,
                               self.width_offset + 11 * self.spacing + 5,
                               self.height_offset + 11 * self.spacing + 5,
                               fill="black")
        # place
        self.chess.place(x=0, y=0, anchor="nw")

    def human_press_mouse(self, event, color):
        if self.width_offset < event.x < self.width - self.width_offset:
            if self.height_offset < event.y < self.height - self.height_offset:
                x_remainder, y_remainder = event.x % self.spacing, event.y % self.spacing
                x_index, y_index = -1, -1
                if x_remainder < 10:
                    x_index = int(event.x - x_remainder)
                    if y_remainder < 10:
                        y_index = int(event.y - y_remainder)
                    if y_remainder > self.spacing - 10:
                        y_index = int(event.y + (self.spacing - y_remainder))
                if x_remainder > self.spacing - 10:
                    x_index = int(event.x + (self.spacing - x_remainder))
                    if y_remainder < 10:
                        y_index = int(event.y - y_remainder)
                    if y_remainder > self.spacing - 10:
                        y_index = int(event.y + (self.spacing - y_remainder))
                if x_index != -1 and y_index != -1:
                    press = True
                    if not self.check_able_play(x_index, y_index):
                        press = False
                    if press:
                        self.chess.create_oval(x_index - 10, y_index - 10, x_index + 10, y_index + 10, fill=color)
                        self.human_press_history.append([x_index, y_index])
                        self.is_human_turn = False

    def ai_show_piece(self, x, y, color):
        press = True
        if not self.check_able_play(x, y):
            press = False
        if press:
            self.chess.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color)
            self.ai_press_history.append([x, y])
            self.is_human_turn = True

    def check_game_over(self):
        if len(self.ai_press_history) < 5 or len(self.human_press_history) < 5:
            return 0

        if self.is_human_turn:
            for history in self.human_press_history:
                if max(self.count_the_continue(history[0], history[1], self.human_press_history)) >= 5:
                    self.human_win = True
                    return 1
            for history in self.ai_press_history:
                if max(self.count_the_continue(history[0], history[1], self.ai_press_history)) >= 5:
                    self.ai_win = True
                    return 1
        else:
            for history in self.ai_press_history:
                if max(self.count_the_continue(history[0], history[1], self.ai_press_history)) >= 5:
                    self.ai_win = True
                    return 1
            for history in self.human_press_history:
                if max(self.count_the_continue(history[0], history[1], self.human_press_history)) >= 5:
                    self.human_win = True
                    return 1

        return 0

    def count_the_continue(self, x, y, history):
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

    def check_able_play(self, x, y):
        press_history = self.human_press_history + self.ai_press_history
        for history in press_history:
            if x == history[0] and y == history[1]:
                return 0
        return 1

    def show_result(self):
        text = ""
        if self.ai_win:
            text = "AI win"
        elif self.human_win:
            text = "Human win"
        label = tk.Label(self.window, text=text, bg="SlateGray", font=("微软雅黑", 40))
        label.pack()

    def get_score(self, x, y, is_human):
        if is_human:
            own = self.human_press_history[:]
        else:
            own = self.ai_press_history[:]
        line_be_count = {r"--": False,
                         r"||": False,
                         r"\\": False,
                         r"//": False}

        count1, count2, count3, count4 = \
            self.count_the_continue(x, y, own)

        # *代表自己棋子 @代表对方棋子 _代表空位
        # 连五 (*****) √
        active_five = 0

        # 活四 (_****_) √
        active_four = 0

        # 冲四
        # (_****@)√ (*_***)√ (**_**)√
        sleep_four = 0

        # 活三
        # (_***_)√ (_*_**_)√
        active_three = 0

        # 眠三
        # (__***@)√ (_*_**@)√ (_**_*@)√ (*__**)√ (*_*_*)√ (@_***_@)√
        sleep_three = 0

        # 活二
        # (__**__)√(_*_*_)√ (_*__*_)√
        active_two = 0

        # 眠二
        # (___**@)√ (__*_*@)√ (_*__*@)√ (*___*)√
        sleep_two = 0

        # 连续5个
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

        # 连续4个
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

        # 连续3个
        # --
        if not line_be_count[r"--"]:
            if count1 == 3:
                press = self.be_count1[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count3(x, y, press, line_type=r"--", is_human=is_human)[0]
                active3 = self.calc_count3(x, y, press, line_type=r"--", is_human=is_human)[1]
                sleep3 = self.calc_count3(x, y, press, line_type=r"--", is_human=is_human)[2]
                if sleep4 or active3 or sleep3:
                    line_be_count[r"--"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3

        # ||
        if not line_be_count[r"||"]:
            if count2 == 3:
                press = self.be_count2[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[1])
                sleep4 = self.calc_count3(x, y, press, line_type=r"||", is_human=is_human)[0]
                active3 = self.calc_count3(x, y, press, line_type=r"||", is_human=is_human)[1]
                sleep3 = self.calc_count3(x, y, press, line_type=r"||", is_human=is_human)[2]
                if sleep4 or active3 or sleep3:
                    line_be_count[r"||"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3

        # \\
        if not line_be_count[r"\\"]:
            if count3 == 3:
                press = self.be_count3[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count3(x, y, press, line_type=r"\\", is_human=is_human)[0]
                active3 = self.calc_count3(x, y, press, line_type=r"\\", is_human=is_human)[1]
                sleep3 = self.calc_count3(x, y, press, line_type=r"\\", is_human=is_human)[2]
                if sleep4 or active3 or sleep3:
                    line_be_count[r"\\"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3
        # //
        if not line_be_count[r"//"]:
            if count4 == 3:
                press = self.be_count4[:]
                press.append([x, y])
                press = sorted(press, key=lambda s: s[0])
                sleep4 = self.calc_count3(x, y, press, line_type=r"//", is_human=is_human)[0]
                active3 = self.calc_count3(x, y, press, line_type=r"//", is_human=is_human)[1]
                sleep3 = self.calc_count3(x, y, press, line_type=r"//", is_human=is_human)[2]
                if sleep4 or active3 or sleep3:
                    line_be_count[r"//"] = True
                    if sleep4:
                        sleep_four += sleep4
                    elif active3:
                        active_three += active3
                    elif sleep3:
                        sleep_three += sleep3

        # 连续两个
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
                        active_two += active2
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
                        active_two += active2
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
                        active_two += active2
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
                        active_two += active2
                    elif sleep2:
                        sleep_two += sleep2
        # 连续1个
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
                        active_two += active2
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
                        active_two += active2
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
                        active_two += active2
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
                        active_two += active2
                    elif sleep2:
                        sleep_two += sleep2

        score = active_five * 15000 + \
                active_four * 10000 + \
                sleep_four * 2500 + \
                active_three * 2000 + \
                sleep_three * 900 + \
                active_two * 800 + \
                sleep_two * 400

        # return active_five,active_four,sleep_four,active_three,sleep_three,active_two,sleep_two
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

        return sleep_four, active_three, sleep_three

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
        # (*__**)sleep_three
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
