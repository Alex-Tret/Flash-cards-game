from tkinter import *
import pandas
from random import *

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
current_card = {}
to_learn = {}
# ------------------------Engine------------------------------------------------------#

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def remove_known_words():
    to_learn.remove(current_card)
    data_to_learn = pandas.DataFrame(to_learn)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)

    next_card()


def next_card():
    global current_card, flip_timer
    screen.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_background, image=card_front)
    canvas.itemconfig(card_title, text="French", fill='black')
    canvas.itemconfig(card_word, text=current_card["French"], fill='black')

    flip_timer = screen.after(3000, flip_card)

# ------------------------Flip card------------------------------------------------------#


def flip_card():
    canvas.itemconfig(card_title, text="English", fill='white')
    canvas.itemconfig(card_word, text=current_card["English"], fill='white')
    canvas.itemconfig(card_background, image=card_back)
# ------------------------UI SETUP------------------------------------------------------#


screen = Tk()
screen.title("Flashy")
screen.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

flip_timer = screen.after(3000, flip_card)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
check_img = PhotoImage(file="images/right.png")
cross_img = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)

known_button = Button(image=check_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=remove_known_words)
known_button.grid(column=0, row=1)

unknown_button = Button(image=cross_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
unknown_button.grid(column=1, row=1)

card_title = canvas.create_text(400, 150, text="", font=LANGUAGE_FONT)
card_word = canvas.create_text(400, 263, text="", font=WORD_FONT)

next_card()

screen.mainloop()
