from tkinter import *
import random
import time

# -----------------------------------------------------------------------------------------
# LOGIC
# -----------------------------------------------------------------------------------------

sentences = open('sentences.txt', 'r').read().split('\n')
prev_line = ""
user_line = ""

end_of_typing = False
starting_time = 0
beginning_time = 0
all_speeds = []


def assign_a_line(arr_sentences):
    global prev_line
    line = random.choice(arr_sentences)

    if prev_line == line:
        line = random.choice(arr_sentences)

    prev_line = line
    return line


def start_calculating(event):
    global starting_time, beginning_time
    global end_of_typing, user_line, text_to_display

    if end_of_typing:
        print('Cannot Type Further')
        return

    if starting_time == 0:
        starting_time = time.time()

    if beginning_time == 0:
        beginning_time = time.time()

    if event.keysym == "BackSpace":
        user_line = user_line[0: len(user_line)-1]

    else:

        user_line += event.char
        end_time = time.time()

        # check if user has typed the entire string correctly

        test_line = user_line

        gap = end_time - starting_time

        if len(test_line) == len(text_to_display):
            end_of_typing = True
            is_accu = check_accuracy(test_line, text_to_display)
            if is_accu == "Continue":
                pass
            else:
                length_of_user_line = len(user_line)
                seconds_elapsed = end_time - beginning_time
                chars_per_second = round(length_of_user_line / seconds_elapsed)
                words_per_minute = chars_per_second * (60 / 5)
                end_of_typing = True
                show_result(is_accu, words_per_minute)
                all_speeds.append(words_per_minute)

                window.after(2000, reset_app)

        if gap > 3:
            ending_msg = 'You took too long. End of typing period. Click on Reset button to start again'
            sentence.config(fg='yellow')
            typing_area.config(highlightcolor='red', highlightbackground='red')
            sentence.config(text=ending_msg)
            return

    starting_time = time.time()


def check_accuracy(user_line_, app_line):
    global end_of_typing
    if end_of_typing:
        if user_line_ == app_line:
            return True
        else:
            return False
    else:
        return "Continue"


def show_result(boolean, wpm):
    if boolean:
        typing_area.config(highlightcolor='green', highlightbackground='green')
        speed_result.config(text=f"Your Typing Speed is {wpm} words per minute WITHOUT ERRORS", fg=FG)
    else:
        typing_area.config(highlightcolor='red', highlightbackground='red')
        speed_result.config(text=f"Your Typing Speed is {wpm} words per minute WITH ERRORS", fg='red')


def reset_app():
    global end_of_typing, starting_time, user_line
    global prev_line, text_to_display, beginning_time
    starting_time = 0
    beginning_time = 0
    end_of_typing = False
    user_line = ""
    prev_line = ""
    text_to_display = assign_a_line(sentences)
    sentence.config(text=text_to_display, fg=FG2)
    typing_area.delete('1.0', 'end')
    typing_area.config(highlightcolor=FG, highlightbackground=FG)
    speed_result.config(text="")


def show_overall_speed():
    if len(all_speeds) != 0:
        sum_ = sum(all_speeds)
        avg = sum_/len(all_speeds)
        speed_result.config(text=f"{int(avg)} wpm", fg='yellow')
    else:
        speed_result.config(text="Nothing to Show yet", fg='yellow')


# -----------------------------------------------------------------------------------------
# UI SETUP
# -----------------------------------------------------------------------------------------


BG = "#041C32"
FG = "#ECB365"
FG2 = "#FF8F56"
FG3 = "#F3A871"

FONT_FAMILY1 = 'Calibri'
FONT_FAMILY2 = 'Helvetica'

FONT_SIZE1 = 14
FONT_SIZE2 = 18
FONT_SIZE3 = 24

FONT_STYLE1 = 'normal'
FONT_STYLE2 = 'italic'

PARA_FONT = (FONT_FAMILY1, FONT_SIZE1, FONT_STYLE1)
PARA_FONT2 = (FONT_FAMILY1, 12, FONT_STYLE2)
HEAD_FONT = (FONT_FAMILY2, FONT_SIZE3, FONT_STYLE2)
HEAD2_FONT = (FONT_FAMILY2, FONT_SIZE2, FONT_STYLE1)

heading = "GET YOUR TYPING SPEED TESTED"
text_to_display = assign_a_line(sentences)

instructions = """
1. The test starts the moment you enter your first letter.
2. You can have a pause of only 3 seconds at max.
"""

window = Tk()
window.title('Welcome to Typing Speed Calculator!')
window.config(bg=BG, pady=10, padx=50)

# CREATING UI COMPONENTS
heading = Label(text=heading, font=HEAD_FONT, bg=BG, fg=FG, padx=10, pady=10)
sentence = Label(text=text_to_display, font=HEAD2_FONT, bg=BG, fg=FG2, pady=10, padx=10, wraplength=800)
instruction = Label(text=instructions, font=PARA_FONT2,
                    fg=FG, bg=BG)
typing_area = Text(font=PARA_FONT, bg=BG, fg=FG, width=80, height=10, wrap='w',
                   highlightcolor=FG, highlightthickness=4, highlightbackground=FG,
                   padx=5, pady=5)
typing_area.bind('<KeyPress>', start_calculating)
reset_btn = Button(text='Reset', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=reset_app)
overall_btn = Button(text='Show Avg Speed', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=show_overall_speed)
speed_result = Label(text="", fg=FG, bg=BG, font=PARA_FONT)

# PLACING UI COMPONENTS ON SCREEN
heading.grid(row=0, column=0, columnspan=3)
sentence.grid(row=1, column=0, columnspan=3)
instruction.grid(row=2, column=0, columnspan=3)
typing_area.grid(row=3, column=0, columnspan=3)
reset_btn.grid(row=4, column=0)
speed_result.grid(row=4, column=1)
overall_btn.grid(row=4, column=2)

window.mainloop()
