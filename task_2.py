"""
Напишіть програму на Python, яка використовує рекурсію для створення фракталу «сніжинка Коха» за умови,
що користувач повинен мати можливість вказати рівень рекурсії.
"""

import turtle
import math


def koch_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in (60, -120, 60, 0):
            koch_curve(t, order - 1, size / 3)
            t.left(angle)


def draw_koch_snowflake(
    order, size=300, pen_width=2, line_color="navy", fill_color=None
):
    screen = turtle.Screen()
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pensize(pen_width)
    t.color(line_color)

    # (необов'язково) пришвидшує отрисовку для великих order
    turtle.tracer(0, 0)

    # Трохи центруємо фігуру
    h = size * math.sqrt(3) / 2
    t.penup()
    t.goto(-size / 2, -h / 3)
    t.pendown()

    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()

    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)

    if fill_color:
        t.end_fill()

    turtle.update()
    turtle.done()


# Приклад виклику
draw_koch_snowflake(order=4, size=360, fill_color=None)
