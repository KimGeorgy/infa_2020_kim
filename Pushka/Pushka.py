from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)
canv.focus_set()


class Ball:
    def __init__(self, x=-10, y=-10):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.type = rnd(0, 10)
        self.x = x
        self.y = y
        if not self.type:
            self.r = 50
            self.ay = 0
            self.live = 10
            self.time = time.time()
        else:
            self.r = 10
            self.ay = 3
            self.live = 7
            self.time = time.time()
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )
        canv.itemconfig(self.id, fill=self.color)

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        if self.y > self.r:
            self.vy -= self.ay

        if (self.r > self.x and self.vx < 0) or (self.x > 800 - self.r and self.vx > 0):
            self.vx = -self.vx

        if (self.r > self.y and self.vy > 0) or (self.y > 600 - self.r and self.vy < 0):
            self.vy = -self.vy

            if self.type:
                if self.vy > 10:
                    self.vy -= 10
                elif self.vy < -10:
                    self.vy += 10
                else:
                    self.vy = 0

                if self.vy == 0:
                    self.vx = 0
                elif self.vx > 5:
                    self.vx -= 5
                elif self.vx < -5:
                    self.vx += 5
                else:
                    self.vx = 0
        self.set_coords()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2 and self.color != 'black':
            return True
        else:
            return False

    def gunhit(self):
        if (self.x - gun.x)**2 + (self.y - gun.y)**2 < (self.r+10)**2 and self.color == 'black' and gun.live == 1:
            return True
        else:
            return False

    def ophit(self):
        if (self.x - op.x)**2 + (self.y - op.y)**2 < (self.r+10)**2 and self.color != 'black' and op.live == 1:
            return True
        else:
            return False


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.type = 1
        self.an = 1
        self.y = 550
        self.x = 20
        self.vx = 0
        self.live = 1
        self.id_body = canv.create_rectangle(self.x-20, self.y+10, self.x+20, self.y-10, fill='green')
        self.id = canv.create_line(self.x, 450, 50, 420, width=7)

    def move_left(self, event):
        self.vx = -5

    def move_right(self, event):
        self.vx = 5

    def stop(self, event):
        self.vx = 0

    def move(self):
        self.x += self.vx
        if not 0 < self.x < 800:
            self.vx = -self.vx
        canv.coords(self.id_body, self.x-20, self.y+10, self.x+20, self.y-10)
        canv.coords(self.id, self.x, self.y,
                    self.x + max(self.f2_power, 20) * math.cos(self.an),
                    self.y + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        new_ball.y = self.y
        new_ball.x = self.x
        if not self.type:
            new_ball.color = 'black'
            new_ball.ay = -1
        if event and self.type:
            if event.x - self.x > 0:
                self.an = math.atan((event.y - self.y) / (event.x - self.x))
            else:
                self.an = math.pi + math.atan((event.y - self.y) / (event.x - self.x))
        elif not self.type and self.x != gun.x:
            if gun.x - self.x > 0:
                self.an = math.atan((gun.y - self.y) / (gun.x - self.x))
            else:
                self.an = math.pi + math.atan((gun.y - self.y) / (gun.x - self.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event and self.type:
            if event.x-self.x > 0:
                self.an = math.atan((event.y-self.y) / (event.x-self.x))
            else:
                self.an = math.pi + math.atan((event.y - self.y) / (event.x - self.x))
        elif not self.type and self.x != gun.x:
            if gun.x-self.x > 0:
                self.an = math.atan((gun.y-self.y) / (gun.x-self.x))
            else:
                self.an = math.pi + math.atan((gun.y - self.y) / (gun.x - self.x))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, self.x, self.y,
                    self.x + max(self.f2_power, 20) * math.cos(self.an),
                    self.y + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.id_points = canv.create_text(30, 30, text=points, font='28')
        self.new_target()
        self.starttime = 0
        self.cooldown = 3

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(100, 700)
        y = self.y = rnd(100, 500)
        r = self.r = rnd(2, 50)
        vx = self.vx = rnd(0, 10)
        vy = self.vy = rnd(0, 10)
        self.live = 1
        color = self.color = 'red'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if not self.r < self.x < 800 - self.r:
            self.vx = - self.vx
        if not self.r < self.y < 600 - self.r:
            self.vy = - self.vy
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        canv.itemconfig(self.id, fill=self.color)

    def hit(self):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)

    def print(self):
        canv.itemconfig(self.id_points, text=points)


class Bomb:
    def __init__(self):
        self.x = -10
        self.y = -10
        self.vy = 0
        self.ay = 1
        self.color = 'black'
        self.size = 10
        self.id = canv.create_rectangle(self.x - self.size, self.y - self.size,
                                        self.x + self.size, self.y + self.size, fill=self.color)

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size
        )
        canv.itemconfig(self.id, fill=self.color)

    def move(self):
        self.y += self.vy + self.ay/2
        self.vy += self.ay
        self.set_coords()

    def hittest(self):
        if abs(gun.x - self.x) < 2*self.size and abs(gun.y - self.y) < 2*self.size:
            return True
        else:
            return False

    def boom(self):
        self.size *= 2
        self.color = 'orange'
        self.set_coords()


number_of_targets = 3
targets = []
bombs = []
points = 0
screen1 = canv.create_text(400, 300, text='', font='28')
gun = Gun()
bullet = 0
balls = []

op = Gun()
op.type = 0
op.y = 50
op.x = 780
op.vx = 0


def new_game(event=''):
    global gun, op, targets, bombs, points, screen1, balls, bullet
    for i in range(number_of_targets):
        t = Target()
        t.new_target()
        targets.append(t)
    bullet = 0
    balls = []
    canv.bind('<Button-1>', gun.fire2_start)
    canv.bind('<ButtonRelease-1>', gun.fire2_end)
    canv.bind('<Motion>', gun.targetting)
    canv.bind('a', gun.move_left)
    canv.bind('d', gun.move_right)
    canv.bind('<space>', gun.stop)

    canv.bind(',', op.fire2_start)
    canv.bind('.', op.fire2_end)
    canv.bind('<Right>', op.move_right)
    canv.bind('<Left>', op.move_left)

    z = 0.016
    t_live = 1
    gun.live = 1
    op.live = 1
    while t_live and gun.live or balls:
        gun.move()
        op.move()
        for t in targets:
            t.move()
            if abs(t.x - gun.x) < 20 and t.y < 400 and t.starttime + t.cooldown < time.time():
                t.starttime = time.time()
                new_bomb = Bomb()
                new_bomb.x = t.x
                new_bomb.y = t.y
                bombs.append(new_bomb)

        for b in bombs:
            if b.color == 'orange':
                canv.delete(b.id)
                bombs.remove(b)
                break
            b.move()
            if b.hittest():
                b.boom()
                gun.live = 0
                points -= 2
                canv.itemconfig(screen1, text='Вы проиграли')
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')

        for b in balls:
            b.move()

            if b.gunhit():
                gun.live = 0
                points -= 2
                canv.itemconfig(screen1, text='Вы проиграли')
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')

            if b.ophit():
                op.live = 0
                points += 2

            for t in targets:
                if b.hittest(t) and t.live:
                    t.live = 0
                    points += 1
                    t.hit()
                    canv.delete(t.id)
                    canv.delete(t.id_points)
                    targets.remove(t)
            for t in targets:
                t.print()

            t_live = 0
            for t in targets:
                t_live += t.live

            if not t_live:
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')

            if b.time + b.live < time.time() and (b.vx == b.vy == 0 or not b.type):
                canv.delete(b.id)
                balls.remove(b)

        if not gun.live:
            for i in range(len(targets)):
                canv.delete(targets[0].id)
                canv.delete(targets[0].id_points)
                targets.remove(targets[0])
        canv.update()
        time.sleep(0.03)
        gun.targetting()
        gun.power_up()
        op.targetting()
        op.power_up()
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    canv.delete(op)
    root.after(750, new_game)


new_game()

root.mainloop()