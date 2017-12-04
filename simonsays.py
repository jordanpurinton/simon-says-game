import turtle
import random
import time
import tkSimpleDialog
# -*- coding: utf-8 -*-

"""
Simon Says Game
by Jordan Purinton
Data Structures and Algorithms
11/16/15
"""

# Set screen height/width
turtle.setup(width=1400, height=800, startx=None, starty=None)

def show_circle(a_turtle, color):
    """
    This method will draw a circle and its
    color will be based on the color that is passed in
    to the parameters of the method.
    """
    a_turtle.color(color)  # Set the color
    a_turtle.speed(100)  # Set base speed so circles are drawn instantly
    a_turtle.begin_fill()  # Start filling
    a_turtle.circle(150)  # Draw circle
    a_turtle.end_fill()  # Finish filling

def new_game():
    """
    This method will set up a game of simon says.
    The user enters his/her name and their score
    is kept track of. At the end of the game, the
    top scores are displayed. Top scores are stored
    in the scores.txt file.
    """

    # Stores the colors for the circles on easy mode
    simon_colors = ["blue", "green", "red", "yellow"]

    # Game is on easy mode by default
    hard_mode = False

    # Used to display top scores
    scores_turtle = turtle.Turtle()

    # Reads in file, creates dictionary based on text file
    with open('scores.txt', 'r') as file:
        scores = {}
        for line in file:
            name, _, score = line.rpartition(' ')
            scores[name] = int(score)

    # Turtle that draws the circles
    shape_turtle = turtle.Turtle()

    # Loops forever until user enters "Q" at the end
    while True:

        # Clears screen before each new game
        turtle.clearscreen()
        turtle.clear()
        turtle.reset()
        turtle.hideturtle()
        scores_turtle.clear()
        scores_turtle.reset()
        scores_turtle.hideturtle()

        # Prompts user to enter his/her name
        name = tkSimpleDialog.askstring("Simon Says game", "Enter your name and then press OK:")

        turtle.clear()

        # Displays start screen instructions
        turtle.write(
            "Hello " + name + " and welcome to Simon Says!\n\nINSTRUCTIONS:\nA pattern of circles will be displayed on the screen."
                              "\nAfter the pattern is over you will be asked to guess what the pattern was.\n"
                              "Each round the pattern will be displayed at a higher speed.\nEnter your guess in the text box in the following format:"
                              "\n\n-If blue enter b\n-If green enter g\n-If yellow enter y\n-If red enter r\n-If orange enter o (hard mode only)\n-If "
                              "purple enter p (hard mode only)\n\n*Make sure to enter the full pattern!\n*For example, if the pattern is blue red, enter "
                              "br in the textbox\n\nIf you want to play on hard mode, enter ""\"hard\" in the text box in the top left.\nHave fun!\n\n",
            align="center", font=("Arial", 14, "bold"))

        # Asks user if user wants to play on easy or hard mode
        instructions_input = tkSimpleDialog.askstring("Ready to play?", "Please read the instructions\nPress OK to play on easy mode"
                                                                "\n(enter \"hard\" and hit OK for hard mode):")
        instructions_input.strip().lower()

        # If user enters hard in the text box, the game adds two more colors
        if instructions_input.strip() == "hard":
            hard_mode = True
            turtle.clear()
            simon_colors = ["blue", "green", "red", "yellow", "orange", "purple"]
        else:
            hard_mode = False
            turtle.clear()
            simon_colors = ["blue", "green", "red", "yellow"]

        correct = True  # Checks if the answer is correct
        score = 0  # Stores user score
        answer = []  # Stores the correct answer pattern with each color
        answer_string = ""  # Stores the correct answer pattern with each starting letter

        # Keeps going while the answer is correct
        while correct:

            # Random number to determine the color of the circle
            if hard_mode:
                rand = random.randint(0, 5)
            else:
                rand = random.randint(0, 3)

            answer.append(simon_colors[rand])  # Adds the color to the answer list
            answer_string += answer[score][0]  # Adds the first letter of each color to answer_string

            # Draws the sequence of circles
            for i in range(0, len(answer)):
                show_circle(shape_turtle, [answer[i]])

                # Decreases sleep time as score goes up, stops decrementing at .3 when user score is past 11
                if score == 0:
                    time.sleep(1.5)
                elif score < 12:
                    time.sleep(1.5 - (score * .1))
                else:
                    time.sleep(.3)

                shape_turtle.hideturtle()
                shape_turtle.clear()

            # Prompt user to guess the pattern
            if score == 0:
                user_guess = tkSimpleDialog.askstring("What was the pattern?",
                                              "Enter your guess:\n(Remember, if pattern is blue red,\nthen the pattern would be br)")
                try:
                    user_guess = user_guess.strip().lower()
                except(AttributeError):
                    correct = False
            else:
                user_guess = tkSimpleDialog.askstring("What was the pattern?", "Enter your guess:")
                user_guess = user_guess.strip().lower()

            # If user's guess is not equal to the answer_string, game stops, displays user score
            if user_guess != answer_string:
                temp = 0
                top_scores_string = "WRONG! GAME OVER!\n" + name + ", your score was: " + str(
                    score) + "\n\nTOP SCORES:\n"
                correct = False
                scores[name] = score
                scores_sorted = sorted(scores.items(), key=lambda x: x[1],
                                       reverse=True)  # Ordered dictionary of key/value pairs
                for key, val in scores_sorted:
                    if temp < 10:  # Adds only the top 10 scores to the string
                        top_scores_string += "( " + str(temp + 1) + " )   " + str(key) + ": " + str(val) + '\n'
                        temp += 1

                # Writes the top scores on the screen
                scores_turtle.write(top_scores_string, align="center", font=("Arial", 16, "bold"))

                # Writes final scores to text file
                with open('scores.txt', 'w') as file:
                    for name, score in scores_sorted:
                        file.write('%s %s\n' % (name, score))  # Stores the sorted scores in the text file

            # Adds to user score each round user guesses correctly
            else:
                score += 1

        # Asks user if he/she wants to play again
        if not correct:
            continue_option = tkSimpleDialog.askstring("GAME OVER!", "Enter q and hit OK to quit. Otherwise, press OK to play again:")
        # User quits the game, ends loop
        if continue_option.strip() == "q" or continue_option.strip() == "Q":
            break
        else:
            True


# Main game loop
new_game()
