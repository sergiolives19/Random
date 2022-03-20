from tkinter import *   # import all objects
import random
import numpy as np

play = False

tk = Tk()   # screen
tk.title('Bouncing balls')
tk.resizable(False, False)

WIDTH, HEIGHT = 400, 300
canvas = Canvas(tk, width = WIDTH, height = HEIGHT)   # where the ball bounces
canvas.pack()

class Ball:
    def __init__(self, canvas, xi, yi, size, color, vx, vy, collided=False):
        self.canvas = canvas
        self.xi = xi
        self.yi = yi
        self.size = size
        self.color = color
        self.vx = vx
        self.vy = vy
        self.collided = collided

    def create(self):
        self.oval = self.canvas.create_oval(self.xi, self.yi, self.xi + self.size, self.yi + self.size, fill=self.color)

ball_size = 25
colors = ['red', 'green', 'blue', 'orange', 'purple', 'pink', 'yellow', 'black', 'white']
directions = np.arange(0, 2*np.pi, np.pi/6)
balls = []

def start():
    global play
    if not play:
        play = True
        global balls
        balls = []
        canvas.delete('all')
        N_str = number_balls_input.get()
        speed_str = speed_input.get()
        if N_str == '':
            N = 0
        else:
            N = int(N_str)
        if speed_str == '':
            speed = 0
        else:
            speed = int(speed_str)
        BallsGeneration(N, speed)

start_button = Button(tk, text='start', command=start)
start_button.pack()

def pause():
    global play
    global balls
    if play:
        play = False
    elif len(balls) > 0:
        play = True
        moveBalls()

def delete():
    if len(balls) > 0:
        b = random.choice(range(len(balls)))
        removed_ball = balls.pop(b)
        canvas.delete(removed_ball.oval)

delete_button = Button(tk, text='delete ball', command=delete)
delete_button.pack()

pause_button = Button(tk, text='pause', command=pause)
pause_button.pack()

number_balls_label = Label(text='Number of balls')
number_balls_label.pack()

number_balls_input = Entry(tk)
number_balls_input.pack()

speed_label = Label(text='Speed')
speed_label.pack()

speed_input = Entry(tk)
speed_input.pack()

def BallsGeneration(N, speed):
    for b in range(N):
        x = random.uniform(0, WIDTH - ball_size)
        y = random.uniform(0, HEIGHT - ball_size)
        global colors
        color = random.choice(colors)
        global directions
        dir = random.choice(directions)
        vx = speed*np.cos(dir)
        vy = speed*np.sin(dir)
        ball = Ball(canvas, x, y, ball_size, color, vx, vy)
        ball.create()
        balls.append(ball)
    moveBalls()

def collision(ball):

    def distp1p2(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def scalar_product(v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    def multiplication(value, v2):
        return value * v2[0], value * v2[1]

    def subtract(v1, v2):
        return v1[0] - v2[0], v1[1] - v2[1]

    def add(v1, v2):
        return v1[0] + v2[0], v1[1] + v2[1]

    (x0, y0, x1, y1) = canvas.coords(ball.oval)
    center = (x0 + x1)/2, (y0 + y1)/2
    for ball2 in balls:
        if ball2 is not ball:
            (x0_2, y0_2, x1_2, y1_2) = canvas.coords(ball2.oval)
            center2 = (x0_2 + x1_2)/2, (y0_2 + y0_2)/2
            if distp1p2(center, center2) <= ball_size:
                v = ball.vx, ball.vy
                s = center[0], center[1]
                v2 = ball2.vx, ball2.vy
                s2 = center2[0], center2[1]
                nv = add(v, multiplication(scalar_product(subtract(v2, v), subtract(s2, s))/
                                           (subtract(s2, s)[0]**2 + subtract(s2, s)[1]**2), subtract(s2, s)))
                nv2 = add(v2, multiplication(scalar_product(subtract(v, v2), subtract(s2, s))/
                                             (subtract(s2, s)[0]**2 + subtract(s2, s)[1]**2), subtract(s2, s)))
                ball.vx = nv[0]
                ball.vy = nv[1]
                ball2.vx = nv2[0]
                ball2.vy = nv2[1]

def moveBalls():
    for ball in balls:

        canvas.move(ball.oval, ball.vx, ball.vy)

        (leftPos, bottomPos, rightPos, topPos) = canvas.coords(ball.oval)

        # bounce on screen margins
        if (leftPos <= 0 and ball.vx < 0) or (rightPos >= WIDTH and ball.vx > 0):
            ball.vx = -ball.vx
        if (bottomPos <= 0 and ball.vy < 0) or (topPos >= HEIGHT and ball.vy > 0):
            ball.vy = -ball.vy

        # collisions
        else:
            collision(ball)

    if play:
        canvas.after(30, moveBalls)

if __name__ == "__main__":
    tk.mainloop()   # update screen elements