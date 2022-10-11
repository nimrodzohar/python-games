# Simple pong in python for beginners

import turtle
import pygame
from pygame import mixer
pygame.mixer.init()

wn = turtle.Screen()
wn.title("Pong by Nimrod")
wn.bgcolor("black") #background color
wn.setup(width=800, height=600) #width and height of terminal
wn.tracer(0)

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0) #speed of animation, 0 is maximum speed
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1) #stretch multiples original wid by 5, so 20*5 = 100 pixels
paddle_a.penup() #so turtle does not draw line while moving
paddle_a.goto(-350,0) #starting position

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0) #speed of animation, 0 is maximum speed
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1) #stretch multiples original wid by 5, so 20*5 = 100 pixels
paddle_b.penup() #so turtle does not draw line while moving
paddle_b.goto(350,0) #starting position

# Ball
ball = turtle.Turtle()
ball.speed(0) #speed of animation, 0 is maximum speed
ball.shape("square")
ball.color("white")
ball.penup() #so turtle does not draw line while moving
ball.goto(0,0) #starting position
ball.dx = 0.15 # Changes ball position in the x coordinate every time ball moves
ball.dy = 0.15 # Changes ball position in the y coordinate every time ball moves

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Player A: 0  Player B: 0", align = "center", font = ("Courier", 24, "normal"))


# Function
# We want to create movement for paddles
def paddle_a_up():
    y = paddle_a.ycor() # ycor returns y coordinate
    y += 20 # add 20 pixels to y coordinate
    paddle_a.sety(y) # define position of paddle to new y value

def paddle_a_down():
    y = paddle_a.ycor() # ycor returns y coordinate
    y -= 20 # add 20 pixels to y coordinate
    paddle_a.sety(y) # define position of paddle to new y value

def paddle_b_up():
    y = paddle_b.ycor() # ycor returns y coordinate
    y += 20 # add 20 pixels to y coordinate
    paddle_b.sety(y) # define position of paddle to new y value

def paddle_b_down():
    y = paddle_b.ycor() # ycor returns y coordinate
    y -= 20 # add 20 pixels to y coordinate
    paddle_b.sety(y) # define position of paddle to new y value

# Keyboard binding
wn.listen() # Listen for keyboard input
wn.onkeypress(paddle_a_up, "w") # When user presses w, call upon paddle_a_up function
wn.onkeypress(paddle_a_down, "s") # When user presses s, call upon paddle_a_down function
wn.onkeypress(paddle_b_up, "Up") # When user presses Up arrow, call upon paddle_b_up function
wn.onkeypress(paddle_b_down, "Down") # When user presses Down arrow, call upon paddle_b_down function

# Main game loop
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border check
    if ball.ycor() > 290: # Half of screen in y direction is 300, minus 10 for top ball height (ball height is 20 pixels)
        ball.sety(290)
        ball.dy *= -1 # Reverses direction if ball hits border
        mixer.Sound("Pong\\bounce.wav").play()
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1 # Reverses direction if ball hits border
        mixer.Sound("Pong\\bounce.wav").play()
    if ball.xcor() > 390:
        ball.goto(0, 0)
        score_a += 1
        ball.dx *= -1 # Reverses direction if ball hits border
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align = "center", font = ("Courier", 24, "normal"))
    if ball.xcor() < -390:
        ball.goto(0, 0)
        score_b += 1
        ball.dx *= -1 # Reverses direction if ball hits border
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align = "center", font = ("Courier", 24, "normal"))

    # Paddle and ball collision
    if ball.xcor() > 340 and ball.xcor() < 350 and ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40:
        ball.setx(340)
        ball.dx *= -1
        mixer.Sound(r"C:\Users\nimro\OneDrive - ort braude college of engineering\Documents\Coding projects yada yada\Pong\bounce.wav").play()
    if ball.xcor() < - 340 and ball.xcor() > - 350 and ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40:
        ball.setx(-340)
        ball.dx *= -1
        mixer.Sound(r"C:\Users\nimro\OneDrive - ort braude college of engineering\Documents\Coding projects yada yada\Pong\bounce.wav").play()
