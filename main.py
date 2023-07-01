"""
Make necessary imports
--- tkinter module  to create our GUI app.
--- random module to randomly pick a sentence from the list of sentences.
--- time module to keep track of time.
"""

from tkinter import *
import random
import time

# ----------------------------------------------------------------------------------------------------------------
# LOGIC
# ----------------------------------------------------------------------------------------------------------------

"""
Global Variables to Hold Values that are needed throughout the file
--- sentences: Holds all the sentences from the text file
--- prev_line: hold the sentence previously used. Used to make sure we don't repeat.
--- user_line: keep track of what user has typed so far.
--- end_of_typing: see if user is allowed to type or not.
--- starting_time: time at which the last keypress was done
--- beginning_time: time at which we started typing the for the firs time.
--- all_speeds: list to hold all our speeds, later used to cal. avg speed.
--- reset_timer: timer that reset the app.
"""

sentences = open('sentences.txt', 'r').read().split('\n')
prev_line = ""
user_line = ""
end_of_typing = False
starting_time = 0
beginning_time = 0
all_speeds = []
reset_timer = 0;

# Function to assign a randomly picked sentence to user

def assign_a_line(arr_sentences):
    # enable function to use previous line's global variable
    global prev_line
    # get a random sentence from the pool of sentences
    line = random.choice(arr_sentences)
    # we don't want to have the same line again.
    if prev_line == line:
        # So if this line is equal to previous line, reassign
        line = random.choice(arr_sentences)
    # store it in prev_line, this will be used next time.
    prev_line = line
    # return this new sentence
    return line


# ---------------------- Function that tracks user's input text and end of typing: START ---------------------


def start_calculating(event):
    """
    :param: event - this holds information of the key that was pressed.
    :return: nothing, since we don't get a value from it to use somewhere.
    :description:
    This function keeps track of time intervals between two consecutive key presses. Keeps track of the time
    when a sentence was started and when was it finished. If reach the end of typing, calculate the speed
    and then show the method that display results
    """

    # get the global variables
    global starting_time, beginning_time, reset_timer
    global end_of_typing, user_line, text_to_display

    """
    if we cannot type, return. This comes in handy when we have reached the end of the current sentence and
    don't want to do anything if the user typs anything.
    """
    if end_of_typing:
        print('Cannot Type Further')
        return

    # If the starting_time and beginning_time variables are not set, set them to current time.

    # we will update it at the end of function, as it is the time when previous key was pressed
    if starting_time == 0:
        starting_time = time.time()

    # this will not be updated since it is the time when the first key was pressed for the sentence
    if beginning_time == 0:
        beginning_time = time.time()

    # we BackSpace was pressed,then remove last character from the user typed string.
    if event.keysym == "BackSpace":
        user_line = user_line[0: len(user_line)-1]
        starting_time = time.time()
        return

    # If all these checkpoints have been passed. Then we update user typed string and calculate result
    else:
        # add current character to user typed string
        user_line += event.char
        # calculate time of current key press.
        end_time = time.time()
        # calculate the gap between prev character and current character's time
        gap = end_time - starting_time
        # if it is greater than 5, User looses.
        if gap > 5:
            ending_msg = 'You took too long. End of typing period. Click on Reset button to start again'
            sentence.config(fg='yellow')
            typing_area.config(highlightcolor='red', highlightbackground='red')
            sentence.config(text=ending_msg)
            return

        # calculate length of user typed string
        text_len = len(user_line)
        """
        if its length is equal to the sentence displayed, it means 
        the user has reach the end and cannot type further
        """
        if text_len == len(text_to_display):
            """
            set end of typing to true, so that if the user pressed another key 
            despite having reaching the end of the sentence, nothing is done
            """
            end_of_typing = True
            # check if the typed string is accurate or not.
            is_accu = check_accuracy(user_line, text_to_display)
            # calculate time elapsed since first key for the current sentence was typed.
            seconds_elapsed = end_time - beginning_time
            # calculate the words per minute using following formula
            chars_per_second = round(text_len / seconds_elapsed)
            words_per_minute = chars_per_second * (60 / 5)
            # call the method that shows results on the UI
            show_result(is_accu, words_per_minute)
            # add the current speed to the list of all speeds
            all_speeds.append(words_per_minute)
            # after 2 seconds, reset the app.
            reset_timer = window.after(2000, reset_app)

    """
    If BackSpace was not typed. If the gap was not greater than 5s and the user has 
    not reached the end of the current sentence's line. Then we update the starting_time to current time, 
    since now after this, another key will be pressed and we are going to need that key's previous key's time, 
    that is the current key's time.
    """
    starting_time = time.time()


# ---------------------- Function that tracks user's input text and end of typing: END ----------------------

# Function to check the accuracy of user typed text


def check_accuracy(user_line_, app_line):
    # if user's line is equal to the text displayed to him
    if user_line_ == app_line:
        # return true
        return True
    # otherwise, he made a mistake in at least 1 character, thus return false
    else:
        return False


# Function that display the result on the UI


def show_result(boolean, wpm):
    # if the user typed text passed the accuracy check
    if boolean:
        # we display the user his speed and tell him he did not make errors
        typing_area.config(highlightcolor='green', highlightbackground='green')
        sentence.config(text=f" Speed: {wpm} wpm WITHOUT ERRORS", fg='green')
    else:
        # otherwise we display the user his speed and tell him he made errors
        typing_area.config(highlightcolor='red', highlightbackground='red')
        sentence.config(text=f" Speed: {wpm} wpm WITH ERRORS", fg='red')


# Function to reset the app, i.e., reinitialize the variables and start again


def reset_app():
    # Get all global variables and widgets and set them to their initial values
    global end_of_typing, starting_time, user_line, reset_timer
    global prev_line, text_to_display, beginning_time

    window.after_cancel(reset_timer)
    starting_time = 0
    beginning_time = 0
    reset_timer = 0
    end_of_typing = False
    user_line = ""
    prev_line = ""
    # geta a new sentence to display
    text_to_display = assign_a_line(sentences)
    # show that sentence
    sentence.config(text=text_to_display, fg=FG2)
    # clear the text of typing area
    typing_area.delete('1.0', 'end')
    # clear the styling of typing area.
    typing_area.config(highlightcolor=FG, highlightbackground=FG)


# Show a user's overall average speed


def show_overall_speed():
    # cancel the reset timer so that result does not disappear suddenlty.
    global reset_timer
    window.after_cancel(reset_timer)
    # if the length of the list is not zero.
    if len(all_speeds) != 0:
        # calculate the average
        sum_ = sum(all_speeds)
        avg = sum_/len(all_speeds)
        # display the average
        sentence.config(text=f"{int(avg)} wpm", fg='yellow')
    # if the list was empty, show the user that there is nothing to display
    else:
        sentence.config(text="Nothing to Show yet", fg='yellow')


# ----------------------------------------------------------------------------------------------------------------
# UI SETUP
# ----------------------------------------------------------------------------------------------------------------

# Variables to hold colors
BG = "#041C32"
FG = "#ECB365"
FG2 = "#FF8F56"
FG3 = "#F3A871"

# Variables to hold font families
FONT_FAMILY1 = 'Calibri'
FONT_FAMILY2 = 'Helvetica'

# Variables to hold font sizes
FONT_SIZE1 = 14
FONT_SIZE2 = 18
FONT_SIZE3 = 24

# Variables to hold font styles
FONT_STYLE1 = 'normal'
FONT_STYLE2 = 'italic'

# variables to hold overall font styling
PARA_FONT = (FONT_FAMILY1, FONT_SIZE1, FONT_STYLE1)
PARA_FONT2 = (FONT_FAMILY1, 12, FONT_STYLE2)
HEAD_FONT = (FONT_FAMILY2, FONT_SIZE3, FONT_STYLE2)
HEAD2_FONT = (FONT_FAMILY2, FONT_SIZE2, FONT_STYLE1)

# heading to show at top of the window
heading = "GET YOUR TYPING SPEED TESTED"
# sentence to display to the user for the firs time.
text_to_display = assign_a_line(sentences)
# The instructions to show to user
instructions = """
1. The test starts the moment you enter your first letter.
2. You can have a pause of only 5 seconds at max.
"""

# create the object of our app's window
window = Tk()
# give it title, padding and background color
window.title('Welcome to Typing Speed Calculator!')
window.config(bg=BG, pady=10, padx=50)

# CREATING UI COMPONENTS
heading = Label(text=heading, font=HEAD_FONT, bg=BG, fg=FG, padx=10, pady=10)
sentence = Label(text=text_to_display, font=HEAD2_FONT, bg=BG, fg=FG2, pady=10, padx=10, wraplength=800)
instruction = Label(text=instructions, font=PARA_FONT2, fg=FG, bg=BG)

typing_area = Text(font=PARA_FONT, bg=BG, fg=FG, width=80, height=10, wrap='w',
                   highlightcolor=FG, highlightthickness=4, highlightbackground=FG,
                   padx=5, pady=5)
typing_area.bind('<KeyPress>', start_calculating)

reset_btn = Button(text='Reset Application', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=reset_app)
overall_btn = Button(text='Show Average Speed', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=show_overall_speed)

# PLACING UI COMPONENTS ON SCREEN
heading.grid(row=0, column=0, columnspan=2)
sentence.grid(row=1, column=0, columnspan=2)
instruction.grid(row=2, column=0, columnspan=2)
typing_area.grid(row=3, column=0, columnspan=2)
reset_btn.grid(row=4, column=0, sticky='ew')
overall_btn.grid(row=4, column=1, sticky='ew')

window.mainloop()

# ----------------------------------------------------------------------------------------------------------------
# THE END
# ----------------------------------------------------------------------------------------------------------------
