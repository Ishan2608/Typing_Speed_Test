from tkinter import *
import random
import time

# -----------------------------------------------------------------------------------------
# LOGIC
# -----------------------------------------------------------------------------------------

sentences = open('sentences.txt', 'r').read().split('\n')
prev_line = ""
word = ""


end_of_typing = False
starting_time = 0
beginning_time = 0
user_line_arr = []


def assign_a_line(arr_sentences):
    global prev_line
    line = random.choice(arr_sentences)

    if prev_line == line:
        line = random.choice(arr_sentences)

    prev_line = line
    return line


def start_calculating(event):
    global starting_time, beginning_time
    global end_of_typing, user_line_arr, text_to_display, word

    if end_of_typing:
        print('Cannot Type Further')
        return

    if starting_time == 0:
        starting_time = time.localtime().tm_sec

    if beginning_time == 0:
        beginning_time = time.localtime().tm_sec

    if event.char == " ":
        user_line_arr.append(word)
        word = ""
    else:
        word += event.char
        end_time = time.localtime().tm_sec

        # check if user has typed the entire string correctly

        test_arr = [item for item in user_line_arr]

        test_arr.append(word)
        test_line = " ".join(test_arr)

        gap = round(end_time - starting_time)

        if len(test_line) == len(text_to_display):
            end_of_typing = True
            is_accu = check_accuracy(test_line, text_to_display)
            if is_accu == "Continue":
                pass
            else:
                user_line = " ".join(user_line_arr)
                length_of_user_array = len(user_line)
                seconds_elapsed = end_time - beginning_time
                chars_per_second = round(length_of_user_array / seconds_elapsed)
                words_per_minute = chars_per_second * (60 / 5)

                end_of_typing = True


                show_result(is_accu, words_per_minute)
                return

        if gap > 3:
            ending_msg = 'You took too long, end of typing period. Click on Reset button to start again.'
            typing_area.config(highlightcolor='red', highlightbackground='red')
            sentence.config(text=ending_msg)
            return

    starting_time = time.localtime().tm_sec


def check_accuracy(user_line, app_line):
    global end_of_typing
    if end_of_typing:
        if user_line == app_line:
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
    global end_of_typing, starting_time, user_line_arr, word, prev_line, text_to_display, beginning_time
    starting_time = 0
    beginning_time = 0
    end_of_typing = False
    user_line_arr = []
    word = ""
    prev_line = ""
    text_to_display = assign_a_line(sentences)
    sentence.config(text=text_to_display)
    typing_area.delete('1.0', 'end')
    typing_area.config(highlightcolor=FG, highlightbackground=FG)
    speed_result.config(text="")


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

heading = "GET YOU TYPING SPEED TESTED"
text_to_display = assign_a_line(sentences)
instruction = """
1. The test starts the moment you enter your first letter.
2. If you have entered an incorrect letter, you cannot correct it with backspace, it will remain wrong.
3. You can have a pause of only 3 seconds at max.
"""

window = Tk()
window.minsize(width=1010, height=500)
window.title('Welcome to Typing Speed Calculator!')
window.config(bg=BG)


heading = Label(text=heading, font=HEAD_FONT, bg=BG, fg=FG, padx=10, pady=10)
sentence = Label(text=text_to_display, font=HEAD2_FONT, bg=BG, fg=FG2, pady=10, padx=10, wraplength=800)
instruction = Label(text=instruction, font=PARA_FONT2,
                    fg=FG, bg=BG)
typing_area = Text(font=PARA_FONT, bg=BG, fg=FG, width=80, height=10, wrap='w',
                   highlightcolor=FG, highlightthickness=4, highlightbackground=FG,
                   padx=5, pady=5)
typing_area.bind('<KeyPress>', start_calculating)
reset_btn = Button(text='Reset', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=reset_app)
speed_result = Label(text="", fg=FG, bg=BG, font=PARA_FONT)


heading.pack()
sentence.pack()
instruction.pack()
typing_area.pack()
reset_btn.pack()
speed_result.pack()

window.mainloop()
