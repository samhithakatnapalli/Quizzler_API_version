import html
from tkinter import *
from attributes import Attributes
from data import fetch_questions

BG_COLOR = '#FBDDBD'
FONT = 'georgia'

class QuizInterface:
    def __init__(self):
        self.window = Tk()
        self.window.minsize(700,500)
        self.window.config(bg=BG_COLOR, padx=30, pady=30)
        self.window.title("Quizzler")

        self.values = Attributes(0, 0)
        self.question_bank = fetch_questions()

        with open('highscore.txt') as file:
            self.highscore = int(file.read())

        self.question = ''
        self.answers = ''

        self.BG = PhotoImage(file='images/bg.png')
        self.RIGHT_BG = PhotoImage(file='images/right_ans_bg.png')
        self.WRONG_BG = PhotoImage(file='images/wrong_ans_bg.png')
        self.RIGHT_TICK = PhotoImage(file='images/right.png')
        self.WRONG_TICK = PhotoImage(file='images/wrong.png')
        self.START_BUTTON = PhotoImage(file='images/click_to_start.png')
        self.RESTART_BUTTON = PhotoImage(file='images/restart.png')

        self.score_text = Label(self.window,
                                text=f"Score: {self.values.score} | Question {self.values.question_number}/{len(self.question_bank)}"
                                 f" | High Score: {self.highscore}",
                                font=(FONT, 15, "bold"), bg=BG_COLOR)
        self.score_text.grid(row=0, column=0, padx=50, columnspan=3, sticky=W + E)

        self.canvas = Canvas(self.window, width=664, height=423, bg=BG_COLOR, highlightthickness=0)
        self.bg = self.canvas.create_image(332, 211, image=self.BG)

        self.start_button = Button(self.window, image=self.START_BUTTON, command=self.next_question, bg='white',
                                   borderwidth=0,
                                   highlightthickness=0)
        self.start_quiz = self.canvas.create_window(332, 212, window=self.start_button)

        self.question_text = self.canvas.create_text(332, 211, font=("georgia", 20), width=300, justify='center')
        self.canvas.grid(row=1, column=0, columnspan=3, sticky=W + E, pady=15)

        self.right_button = Button(self.window, image=self.RIGHT_TICK, bg=BG_COLOR, state='disabled',
                                   command=lambda: self.is_right_answer("True"), borderwidth=0, highlightthickness=0)
        self.right_button.grid(row=2, column=0)
        self.restart_button = Button(self.window, image=self.RESTART_BUTTON, state='disabled', command=self.restart,
                                     bg=BG_COLOR,
                                     borderwidth=0, highlightthickness=0)
        self.restart_button.grid(row=2, column=1)
        self.wrong_button = Button(self.window, image=self.WRONG_TICK, bg=BG_COLOR, state='disabled',
                                   command=lambda: self.is_right_answer("False"), borderwidth=0, highlightthickness=0)
        self.wrong_button.grid(row=2, column=2)

        self.window.mainloop()

    def next_question(self):
        self.canvas.itemconfig(self.bg, image=self.BG)
        self.canvas.itemconfig(self.start_quiz, state='hidden')
        self.right_button.config(state='normal')
        self.wrong_button.config(state='normal')
        self.restart_button.config(state='normal')

        if self.values.question_number < len(self.question_bank):
            self.question = html.unescape(self.question_bank[self.values.question_number]['question'])
            self.answers = self.question_bank[self.values.question_number]['correct_answer'].title()

            self.canvas.itemconfig(self.question_text, text=self.question)
            self.values.question_number += 1
            self.score_text.config(text=f"Score: {self.values.score} | Question {self.values.question_number}/{len(self.question_bank)}"
                                        f" | High Score: {self.highscore}")
        else:
            self.canvas.itemconfig(self.question_text, text=f"Yay! You've finished the quiz.")
            self.right_button.config(state='disabled')
            self.wrong_button.config(state='disabled')

            if self.highscore < self.values.score:
                self.highscore = self.values.score

                with open('highscore.txt', 'w') as file:
                    file.write(str(self.highscore))

    def is_right_answer(self,user_answer):
        if user_answer == self.answers:
            self.canvas.itemconfig(self.bg, image=self.RIGHT_BG)
            self.update_score()
        else:
            self.canvas.itemconfig(self.bg, image=self.WRONG_BG)

        self.window.after(500, self.next_question)

    def update_score(self):
        self.values.score += 1
        self.score_text.config(text=f"Score: {self.values.score} | Question {self.values.question_number}/{len(self.question_bank)}"
                                    f" | High Score: {self.highscore}")

    def restart(self):
        self.canvas.itemconfig(self.start_quiz, state='normal')
        self.values.score = 0
        self.values.question_number = 0
        self.score_text.config(text=f"Score: {self.values.score} | Question {self.values.question_number}/{len(self.question_bank)}"
                                    f" | High Score: {self.highscore}")
        self.canvas.itemconfig(self.question_text, text='')
        self.right_button.config(state='disabled')
        self.wrong_button.config(state='disabled')