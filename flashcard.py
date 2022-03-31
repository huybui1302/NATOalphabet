import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
word_pair = {}

# ---------------------------- CSV DATA ------------------------------- #
try:
    data = pandas.read_csv("./data/to_be_learned.csv").to_dict(orient="records")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
    data.to_csv("./data/to_be_learned.csv", index=False)
    data = pandas.read_csv("./data/to_be_learned.csv").to_dict(orient="records")
# else:
#     data.to_dict(orient="records")


# ---------------------------- TRANSFER DATA ------------------------------- #
def remove():
    global word_pair
    data.remove(word_pair)
    print(len(data))
    new_data = pandas.DataFrame(data)
    new_data.to_csv("./data/to_be_learned.csv", index=False)


# ---------------------------- GENERATE WORD ------------------------------- #
def generate():
    global word_pair, flip_timer
    window.after_cancel(flip_timer)
    word_pair = random.choice(data)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=word_pair["French"], fill="black")
    canvas.itemconfig(image, image=front)
    flip_timer = window.after(2500, flip)


# ---------------------------- FLIP CARD ------------------------------- #
def flip():
    global word_pair
    canvas.itemconfig(image, image=back)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=word_pair["English"], fill="white")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=840, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)
front = PhotoImage(file="./images/card_front.png")
back = PhotoImage(file="./images/card_back.png")
image = canvas.create_image(420, 265, image=front)
canvas.grid(column=0, row=0, columnspan=2)
language = canvas.create_text(420, 150, text="French", font=("Aerial", 40, "italic"))
word = canvas.create_text(420, 265, text="word", font=("Aerial", 60, "bold"))
right = PhotoImage(file="./images/right.png")
right_button = Button(image=right, highlightthickness=0, command=lambda: [generate(), remove()])
right_button.grid(column=0, row=1)
wrong = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=generate)
wrong_button.grid(column=1, row=1)

flip_timer = window.after(2500, flip)
generate()

window.mainloop()
