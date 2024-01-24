from tkinter import *
from pygame import mixer

# Initialise mixer
mixer.init()

# Define constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#379B46"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 24
SHORT_BREAK_MIN = 4
LONG_BREAK_MIN = 14
SECS = 59
COUNTER = 0

# Instantiate window
root = Tk()
root.config(
    padx=50, pady=60,
    bg=YELLOW
)


# Create a function to trigger alarm
def alarm():
    mixer.music.load("buzzer alarm.mp3")
    mixer.music.play()


# Create a function to trigger notifications
def notify(num):
    win1 = Toplevel(width=200, height=400)
    win1.config(padx=50, pady=100, bg=YELLOW)
    lb1 = Label(
        win1, text="",
        font=(FONT_NAME, 20, "bold"),
        bg=YELLOW, fg=GREEN
    )
    if num == 1:
        lb1.config(text="5 MINUTES\nBREAK!")
    elif num == 2:
        lb1.config(text="15 MINUTES\nBREAK!")
    elif num == 3:
        lb1.config(text="GET BACK TO\nWORK!", fg=RED)
    lb1.grid(padx=20, pady=20)
    alarm()


# Define local variables
counter = COUNTER
repetitions = 0
secs = SECS
pomodoro = "pomodoro"
pomodoro_count = 0
counting = True
mins = WORK_MIN
mins2 = SHORT_BREAK_MIN
mins3 = LONG_BREAK_MIN


# A function to countdown work time
def decrease_work():
    global secs, mins, counter, repetitions, pomodoro_count, pomodoro
    if mins > -1:
        if secs > 0:
            secs -= 1
        else:
            mins -= 1
            secs = SECS
    if mins < 0 and counter < 8:
        mins = WORK_MIN
        counter += 1
        notify(1)
    elif mins < 0 and counter >= 8:
        mins = WORK_MIN
        repetitions += 1
        if counter == 8 and repetitions == 1:
            pomodoro_count = 0
            pomodoro = "pomodoro"
            l2.config(text=f"")
            clear_frame(f3)
        notify(2)
    update_displayed_time(1)


# A function to countdown short break time
def decrease_short_break():
    global secs, mins2, counter, pomodoro, pomodoro_count
    if mins2 > -1:
        if secs > 0:
            secs -= 1
        else:
            mins2 -= 1
            secs = SECS
    if mins2 < 0:
        notify(3)
        mins2 = SHORT_BREAK_MIN
        counter += 1
        pomodoro_count += 1
        if pomodoro_count > 1:
            pomodoro = "pomodoros"
        l2.config(text=f"{pomodoro_count} short {pomodoro} completed")
        insert_label(pomodoro_count)
    update_displayed_time(2)


# A function to countdown long break time
def decrease_long_break():
    global secs, counter, repetitions, pomodoro, pomodoro_count, mins3
    if mins3 > -1:
        if secs > 0:
            secs -= 1
        else:
            mins3 -= 1
            secs = SECS
    if mins3 < 0:
        mins3 = LONG_BREAK_MIN
        repetitions += 1
        pomodoro_count += 1
        if pomodoro_count > 1:
            pomodoro = "pomodoros"
        l2.config(text=f"{pomodoro_count} long {pomodoro} completed")
        insert_label(pomodoro_count)
        if pomodoro_count < 4:
            notify(3)
    update_displayed_time(3)


# A function to update the timer during countdown
def update_timer():
    if counting:
        if counter < 8:
            if counter % 2 != 0:
                decrease_short_break()
            elif counter % 2 == 0:
                decrease_work()
        else:
            if repetitions < 8:
                if repetitions % 2 == 0:
                    decrease_work()
                elif repetitions % 2 != 0:
                    decrease_long_break()
            else:
                update_displayed_time(0)

        root.after(1000, update_timer)


# A function to start the timer/countdown
def start_timer():
    global counting, counter, repetitions, pomodoro_count, pomodoro, secs, mins

    counting = True
    mins = WORK_MIN
    counter = COUNTER
    repetitions = 0
    pomodoro_count = 0
    pomodoro = "pomodoro"
    secs = SECS

    b1.config(state="disabled")  # Disable the start button once countdown starts

    update_timer()


# A function to control the refresh button
def refresh():
    global counting, mins, secs, counter, repetitions, pomodoro_count, pomodoro

    counting = False  # Stop the countdown
    mins = WORK_MIN
    secs = SECS
    counter = COUNTER
    repetitions = 0
    pomodoro_count = 0
    pomodoro = "pomodoro"

    update_displayed_time(0)  # Update displayed time on the canvas
    b1.config(state="active")  # Reactivate the start button

    l2.config(text="")
    clear_frame(f3)


# A function to update the displayed time on the canvas
def update_displayed_time(fig):
    if fig == 1:
        canvas.itemconfig(
            2,
            text=f"{mins:02d}:{secs:02d}"
        )
    elif fig == 2:
        canvas.itemconfig(
            2,
            text=f"{mins2:02d}:{secs:02d}"
        )
    elif fig == 3:
        canvas.itemconfig(
            2,
            text=f"{mins3:02d}:{secs:02d}"
        )
    elif fig == 0:
        canvas.itemconfig(
            2,
            text=f"{mins:02d}:{secs:02d}"
        )


# Create a pomodoro label
l1 = Label(
    text="Pomodoro",
    bg=YELLOW,
    fg=GREEN,
    font=(FONT_NAME, 30, "italic")
)
l1.grid(row=0, column=1, sticky="N")

# Create a canvas for a tomato image
f1 = Frame(root)
f1.grid(row=1, column=1)

tomato = PhotoImage(file="tomato.png")
canvas = Canvas(
    f1,
    width=204, height=228,
    highlightthickness=0,
    bg=YELLOW
)

canvas.create_image(100, 112, image=tomato)  # Add image to canvas
canvas.create_text(
    102, 130,
    font=(FONT_NAME, 35, "bold"),
    text=f"{mins:2d}:{secs:2d}",
    justify="center",
    fill="#ffffff"
)  # Add text to canvas
canvas.grid(row=1, column=1)

# Create start and refresh buttons
f2 = Frame(root)
f2.grid(row=2, column=1, pady=10)

b1 = Button(
    f2,
    text="Start",
    fg=RED, width=8,
    activebackground="gray",
    font=(FONT_NAME,10, "bold"),
    command=start_timer
)
b2 = Button(
    f2,
    text="Reset",
    fg=RED, width=8,
    activebackground="gray",
    font=(FONT_NAME,10, "bold"),
    command=refresh
)

b1.grid(row=0, column=0)
b2.grid(row=0, column=1)

l2 = Label(
    text="",
    bg=YELLOW,
    fg=GREEN,
    font=(FONT_NAME, 18, "bold")
)
l2.grid(row=3, column=1, pady=10)

# Create a frame to hold checkmarks
f3 = Frame(root)
f3.config(bg=YELLOW)
f3.grid(row=4, column=1)


# Create a function to insert checkmarks with each pomodoro
def insert_label(digit):
    lab = Label(
        f3,
        text="✔",
        bg=YELLOW,
        fg=GREEN,
        font=(FONT_NAME, 20, "bold")
    )
    lab.grid(row=0, column=digit)


# Create a function to destroy the checkmarks
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# Loop the window
root.mainloop()
