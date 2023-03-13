import pygame as pg
import random
import time
import math
import numpy as np

# every edge of grid = 2.5km
grid_size = 50

cars = []
BS_list = []
# BS_list_actual = []
frequency = 1
car_number = 0


def possion(n, t, lamda=1 / 12):
    temp = (lamda * t) ** n
    temp = temp * math.exp(-lamda * t)
    ans = temp / math.factorial(n)
    return ans


class Window():
    def __init__(self):
        self.width, self.height = 20 + grid_size * 10 + 20 + 200, 20 + grid_size * 10 + 20

        # self.window_init()

    def window_init(self, ):
        # pygame init
        pg.init()

        # 設定視窗
        self.screen = pg.display.set_mode((int(self.width), int(self.height)))
        pg.display.set_caption("Internet HW")

        # 建立畫布bg map
        self.bg = pg.Surface(self.screen.get_size())
        self.bg = self.bg.convert()

        # text
        score_font = pg.font.Font(None, 50)

        # cars.append(Car(0, 0))
        # display

        self.screen.blit(self.bg, (0, 0))
        pg.display.update()
        running = True
        min = 0
        best = 0
        entropy = 0
        myself = 0
        sys_time = 0
        while running:
            # hand off times
            call_number = 0

            self.bg.fill((0, 0, 0))  # white
            self.draw_line()
            self.draw_BS()
            self.create_car()
            for c in cars:
                # print(c.position_show)
                # print(c.position_actual)
                c.move()
                c.is_call()
                # c.path_loss()
                pg.draw.circle(self.bg, c.color, c.position_show, 3, 3)
                if c.position_actual[0] < 0 or c.position_actual[0] > 25 or c.position_actual[1] < 0 or \
                        c.position_actual[1] > 25:
                    cars.remove(c)
                m, n, o, p = c.handoff()
                min += m
                best += n
                entropy += o
                myself += p
                if c.call_mode == "call":
                    call_number += 1

            # handoff text

            self.screen.blit(self.bg, (0, 0))
            self.show_text('sys_time: {0}: {1}'.format(sys_time // 60, int(sys_time % 60)), [550, 75])
            self.show_text('handoff:', [550, 100])
            self.show_text('Minium:{0}'.format(str(min)), [550, 125])
            self.show_text('Best_effort:{0}'.format(str(best)), [550, 150])
            self.show_text('Entropy:{0}'.format(str(entropy)), [550, 175])
            self.show_text('My :{0}'.format(str(myself)), [550, 200])
            self.show_text('call_number:{0}'.format(str(call_number)), [550, 250])
            self.show_text('car_number:{0}'.format(len(cars)), [550, 400])

            pg.display.update()
            # t += 20

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
            sys_time += 1
            time.sleep(0.1)

    def draw_BS(self):
        bias = 10
        actual_posittion = []
        for bs in BS_list:
            x = bs.position_show[0]
            y = bs.position_show[1]
            if bs.direction == 0:
                actual_posittion.append((1.25 + 2.5 * x + 0.1, 1.25 + 2.5 * y))
                pg.draw.circle(self.bg, bs.color, (45 + x * grid_size + bias, 45 + y * grid_size), 3, 5)
            elif bs.direction == 1:
                actual_posittion.append((1.25 + 2.5 * x, 1.25 + 2.5 * y - 0.1))
                pg.draw.circle(self.bg, bs.color, (45 + x * grid_size, 45 + y * grid_size - bias), 3, 5)
            elif bs.direction == 2:
                actual_posittion.append((1.25 + 2.5 * x - 0.1, 1.25 + 2.5 * y))
                pg.draw.circle(self.bg, bs.color, (45 + x * grid_size - bias, 45 + y * grid_size), 3, 5)
            elif bs.direction == 3:
                actual_posittion.append((1.25 + 2.5 * x, 1.25 + 2.5 * y + 0.1))
                pg.draw.circle(self.bg, bs.color, (45 + x * grid_size, 45 + y * grid_size + bias), 3, 5)
            # print(x, y, dir)
        # print(actual_posittion)
        return

    def add_car(self):
        p = possion(1, 1)
        for i in range(4):
            for j in range(9):
                ran = random.random()
                if (ran <= p):
                    temp = Car(i, j)
                    cars.append(temp)

    def draw_line(self):
        for i in range(11):
            pg.draw.line(self.bg, (255, 255, 255), (20 + grid_size * i, 20), (20 + grid_size * i, 520), 5)
        for i in range(11):
            pg.draw.line(self.bg, (255, 255, 255), (20, 20 + grid_size * i), (520, 20 + grid_size * i), 5)

    def create_car(self):
        for i in range(4):
            for j in range(9):
                if random.random() < possion(1, 1):
                    if i == 0:
                        x = 0
                        y = j + 1
                        dir = 0
                        cars.append(Car(x, y, dir))
                    elif i == 1:
                        x = j + 1
                        y = 0
                        dir = 3
                        cars.append(Car(x, y, dir))
                    elif i == 2:
                        x = 10
                        y = j + 1
                        dir = 2
                        cars.append(Car(x, y, dir))
                    elif i == 3:
                        x = j + 1
                        y = 10
                        dir = 1
                        cars.append(Car(x, y, dir))

    def show_text(self, text, position, color=(0, 255, 255), font_size=30):
        font = pg.font.SysFont('宋體', font_size)
        text_message = font.render(text, True, color)
        # text_handoff_surf = score_font.render('handoff:{0}'.format(str(t)), True, (0, 255, 255))
        # text_handoff_pos = [550, 350]
        self.screen.blit(text_message, position)


def create_BS():
    global frequency
    t = 0
    count = 0
    color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (150, 0, 0),
             (0, 150, 0), (0, 0, 150), (150, 150, 0)]
    for i in range(10):
        for j in range(10):
            p = random.randint(0, 9)
            if p == 0:
                direction = random.randint(0, 3)
                BS_list.append(BS(j, i, direction, color[count % len(color)]))
                frequency += 1
                count += 1
                if frequency > 10:
                    frequency = 1
    # print(BS_list)
    return


class Car():
    def __init__(self, x, y, direction):
        self.speed_actual = 0.02
        self.speed_show = 0.4
        self.position_actual = [2.5 * x, 2.5 * y]
        self.position_show = [20 + 50 * x, 20 + 50 * y]
        # self.position_actual = (0, 0)
        # self.position_show = (0, 0)
        self.direction = direction
        # 0-> right 1->up 2->left 3->down
        # self.power = []
        self.connect_BS_min = 0
        self.connect_BS_best = 0
        self.connect_BS_entropy = 0
        self.connect_BS_myself = 0
        self.myself_last_power = 0
        self.myself_decrease_time = 0
        self.color = (100, 100, 255)
        self.connect = 100
        self.call_mode = "release"
        self.call_time = 0
        self.call_stop_time = 0
        self.connect_BS = 100
        self.call_counts = 0
        self.in_sys_time = 0

    def move(self):

        # self.in_sys_time += 1
        if self.direction == 0:
            self.position_actual[0] += self.speed_actual
            self.position_show[0] += self.speed_show
        elif self.direction == 1:
            self.position_actual[1] -= self.speed_actual
            self.position_show[1] -= self.speed_show
        elif self.direction == 2:
            self.position_actual[0] -= self.speed_actual
            self.position_show[0] -= self.speed_show
        elif self.direction == 3:
            self.position_actual[1] += self.speed_actual
            self.position_show[1] += self.speed_show
        self.position_show[0] = round(self.position_show[0], 1)
        self.position_show[1] = round(self.position_show[1], 1)
        self.position_actual[0] = round(self.position_actual[0], 2)
        self.position_actual[1] = round(self.position_actual[1], 2)
        if self.position_actual[0] % 2.5 == 0 and self.position_actual[1] % 2.5 == 0:
            # print("in")
            dir_probability = random.randint(1, 32)
            if (17 <= dir_probability < 19):  # reverse
                if self.direction == 0:
                    self.direction = 2
                elif self.direction == 1:
                    self.direction = 3
                elif self.direction == 2:
                    self.direction = 0
                elif self.direction == 3:
                    self.direction = 1
            elif (19 <= dir_probability < 26):  # turn right
                self.direction -= 1
                if self.direction < 0:
                    self.direction = 3
            elif (26 <= dir_probability < 33):  # turn left
                self.direction += 1
                if self.direction > 3:
                    self.direction = 0

    def path_loss(self):
        n = 0
        # temp is used to record the Pr
        temp = [0 for i in range(len(BS_list))]

        # print("-------------------")
        for bs in BS_list:
            distance = math.dist(self.position_actual, bs.position_actual)
            Path_Loss = 32.45 + (20 * math.log(bs.frequency, 10)) + (20 * math.log(distance, 10))  # unit : dB
            # print(distance,bs.frequency,Path_Loss)
            Path_Loss /= 10
            Path_Loss = 10 ** Path_Loss

            # ans is path loss  unit:wt(?)
            Pt = 10 ** (120 / 10)
            Pr = Pt / Path_Loss  # unit : wt
            Pr = 10 * math.log(Pr)  # unit : dB

            # print(bs.frequency,distance,ans)
            temp[n] = Pr
            n += 1
            # if len(self.power) != len(BS_list):
            #     self.power.append(ans)
            # else:
            #     self.power[n] = ans
            #     n += 1
        # print(temp,temp.index(max(temp)),BS_list[temp.index(max(temp))].position_actual,self.position_actual)
        # self.connect_BS = temp.index(max(temp))
        # self.color = BS_list[temp.index(max(temp))].color
        # self.power = sorted(self.power, reverse=True)
        return temp

    def is_call(self):
        temp = self.path_loss()
        # if self.in_sys_time % 3600 == 0:
        #     self.call_counts = int(np.random.normal(2))
        #     if self.call_counts < 0:
        #         self.call_counts = 0
        # if self.call_counts > 0 and self.call_mode == "release" :
        if random.random() < 2 / 3600 and self.call_mode == "release":
            self.call_time = 0
            self.call_stop_time = int(np.random.normal(180))
            self.call_mode = "call"
            self.connect_BS_min = temp.index(max(temp))
            self.connect_BS_best = temp.index(max(temp))
            self.connect_BS_entropy = temp.index(max(temp))
            self.connect_BS_myself = temp.index(max(temp))
            self.myself_last_power = max(temp)
            self.call_counts -= 1
        elif self.call_mode == "call":
            self.call_time += 1
            if self.call_time > self.call_stop_time:
                self.call_mode = "release"

    def handoff(self):
        minimum_threshold = 0
        Best_effort = 0
        entropy = 0
        myself = 0
        temp = self.path_loss()
        # print(temp)
        if (self.call_mode == "call"):
            # Minimum
            Pmin = 50
            if temp[self.connect_BS_min] < Pmin and max(temp) > temp[self.connect_BS_min]:
                #   print(temp[self.connect_BS_min])
                self.connect_BS_min = temp.index(max(temp))
                minimum_threshold = 1


            # Best
            if max(temp) > temp[self.connect_BS_best]:
                self.connect_BS_best = temp.index(max(temp))
                Best_effort = 1

            # entopy
            E = 25
            if max(temp) - temp[self.connect_BS_entropy] > E:
                self.connect_BS_entropy = temp.index(max(temp))
                entropy = 1

            # myself
            Pmyself = 10
            # if max(temp) - temp[self.connect_BS_myself] > Emyself and max(temp) > temp[self.connect_BS_myself]:
            #     self.connect_BS_myself = temp.index(max(temp))
            #     myself = 1
            if max(temp) > temp[self.connect_BS_myself] and temp[self.connect_BS_myself] < self.myself_last_power:
                if self.myself_decrease_time < 15:
                    self.myself_decrease_time += 1
                    self.myself_last_power = temp[self.connect_BS_myself]
                    #print(self.myself_decrease_time)
                else:
                    self.myself_last_power = max(temp)
                    self.connect_BS_myself = temp.index(max(temp))
                    self.myself_decrease_time = 0
                    myself = 1
            else:
                self.myself_decrease_time = 0


            # show calling color
            self.myself_last_power = temp[self.connect_BS_myself]
            self.color = BS_list[self.connect_BS_min].color
        else:
            self.color = (100, 100, 255)
        # print(minimum_threshold,car_number,entropy,myself)
        return minimum_threshold, Best_effort, entropy, myself


class BS():
    def __init__(self, x, y, direction, color):
        self.direction = direction
        self.position_show = [x, y]
        self.position_actual = [1.25 + 2.5 * x, 1.25 + 2.5 * y]
        if (direction == 0):
            self.position_actual[0] += 0.1
        elif (direction == 1):
            self.position_actual[1] -= 0.1
        elif (direction == 2):
            self.position_actual[0] -= 0.1
        elif (direction == 3):
            self.position_actual[1] += 0.1
        self.frequency = frequency * 100
        self.power = 120  # (dB)
        self.color = color
        for i in range(len(self.color)):
            if (self.color[i] > 255):
                self.color[i] = 255


if __name__ == '__main__':
    # create BS
    # ans = possion(1, 1)
    # print(ans)
    create_BS()
    ui = Window()
    ui.window_init()
