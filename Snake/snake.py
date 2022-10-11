import random
from tkinter import *

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "green" # 00ff00
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"


class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [] # list of coordinates
        self.squares = [] # list of square parts

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0]) # snake will appear in top left corner

        for x, y in self.coordinates: # two values because coordinates is list that houses lists
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag = "snake")
            self.squares.append(square)

class Food:
    
    def __init__(self):

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) -1) * SPACE_SIZE # Create random x coordinate between 0 to game width / ball size * ball size to convert to pixels
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) -1) * SPACE_SIZE

        self.coordinates = [x, y]

        oval = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food") # Define oval shape + start and end of shape by coordinate

def next_turn(snake, food):
    
    x, y = snake.coordinates[0] # Grab coordinates of head of snake

    if direction == "up":
        y -= SPACE_SIZE # go down by space size
    elif direction == "down":
        y += SPACE_SIZE # go up by space size
    elif direction == "left":
        x -= SPACE_SIZE # go left by space size
    elif direction == "right":
        x += SPACE_SIZE # go right by space size

    snake.coordinates.insert(0, (x, y)) # insert new coordinates at head of snake

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag = "snake") # define shape and location of head of snake
    
    snake.squares.insert(0, square) # replace new head to snake list of squares

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score
        score += 1 # update score
        label.config(text = "Score: {}".format(score)) # update score label
        canvas.delete("food") # delete food from canvas
        food = Food() # create new food

    else:
        del snake.coordinates[-1] # Delete coordinates of tail of snake which is last set of coordinates
        canvas.delete(snake.squares[-1]) # Update canvas, delete tail from it
        del snake.squares[-1]

    if check_collision():
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food) # After turn ends, repeat function

def change_direction(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collision():

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        print("GAME OVER MAN")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER MAN")
        return True
    
    for body_part in snake.coordinates[1:]: # everything after head of snake
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER MAN")
            return True
    return False

def game_over():
    
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, text = "GAME OVER MAN", font = ('consolas', 70), fill = "red", tag = "gameover")

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text = "Score: {}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg = BACKGROUND_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width() # Grab current window width, height, screenwidth, and screenheight
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2)) # Convert to int since screen width and height can't be float
y = int((screen_height/16) - (window_height/16))

window.geometry(f"{window_width}x{window_height}+{x}+{y}") # Change width and height of existing window

window.bind('<Left>', lambda event: change_direction('left')) # bind key to change direction function with name of key
window.bind('<Right>', lambda event: change_direction('right'))  
window.bind('<Up>', lambda event: change_direction('up')) 
window.bind('<Down>', lambda event: change_direction('down')) 


snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
