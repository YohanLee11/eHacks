import tkinter as tk
from tkinter import messagebox, Label, Button,Entry
import random


class WordBasketGame:
    def __init__(self, master):
        self.master = master
        master.title("Word Basket Game")

        self.baskets = [[] for _ in range(5)]  # Five baskets
        self.basket_labels = [Label(master, text="", width=20, height=5, bg="light grey", font=(
            'Helvetica', 16)) for _ in range(5)]
        for i, lbl in enumerate(self.basket_labels):
            lbl.grid(row=1, column=i, padx=5, pady=5)

        self.basket_buttons = [Button(
            master, text=f"Place in Basket {i+1}", command=lambda i=i: self.place_ball_in_basket(i), font=('Helvetica', 12)) for i in range(5)]
        for i, btn in enumerate(self.basket_buttons):
            btn.grid(row=3, column=i, padx=5, pady=5)

        self.score = 0
        self.score_label = Label(
            master, text="Score: 0", font=('Helvetica', 16))
        self.score_label.grid(row=0, column=0, columnspan=5)

        self.highscore = 0
        self.highscore_label = Label(
            master, text="Highest Score: 0", font=('Helvetica', 16))
        self.highscore_label.grid(row=0, column = 3, columnspan=5)

        self.next_letter = self.generate_alphabet_ball()  # Next letter to be placed
        self.next_letter_label = Label(
            master, text=f"Next Letter: {self.next_letter}", font=('Helvetica', 16), fg="blue")
        self.next_letter_label.grid(row=2, column=0, columnspan=5)

        self.duration_label = Label(
            master, text="Set time (seconds): ", font=('Helvetica',16))
        self.duration_label.grid(row=4, column = 0, columnspan = 1)
        self.duration_entry = Entry(master, font=('helvetica', 16))
        self.duration_entry.grid(row=4, column= 1, columnspan=1)


        self.time_left = 0  # To be set by player
        self.timer_label = Label(
            master, text="Time: 00:00", font=('Helvetica', 16))
        self.timer_label.grid(row=4, column=0, columnspan=5)

        self.game_running = False

        # Start game button
        self.start_button = Button(
            master, text="Start Game", command=lambda: self.start_game(60), font=('Helvetica', 16))
        self.start_button.grid(row=5, column=0, columnspan=5)

    def start_game(self, duration):

        try:
            duration = int(self.duration_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number for the duration.")
            return

        self.time_left = duration
        if(self.highscore < self.score):
            self.highscore = self.score
        self.score = 0
        self.game_running = True
        # Generate a new letter for the start
        self.next_letter = self.generate_alphabet_ball()
        for basket in self.baskets:
            basket.clear()
        self.update_game()
        self.update_display()

    def place_ball_in_basket(self, basket_index):
        if self.game_running and len(self.baskets[basket_index]) < 5:
            self.baskets[basket_index].append(self.next_letter)
            self.check_for_word(basket_index)
            # Generate a new letter after placing
            self.next_letter = self.generate_alphabet_ball()
            self.update_display()

    def generate_alphabet_ball(self):
        letters = "aeiou" * 2 + "bcdfghjklmnpqrstvwxyz"
        return random.choice(letters)

    def check_for_word(self, basket_index):
        if len(self.baskets[basket_index]) == 5:
            word = ''.join(self.baskets[basket_index])
            if self.is_valid_word(word):
                self.score += 1
                self.baskets[basket_index] = []  # Reset basket
            else:
                self.score -= 1
                self.baskets[basket_index] = []
        if len(self.baskets[basket_index]) == 3:
            word = ''.join(self.baskets[basket_index])
            if self.is_valid_word(word):
                self.score += 1
                self.baskets[basket_index] = []  
        if len(self.baskets[basket_index]) == 4:
            word = ''.join(self.baskets[basket_index])
            if self.is_valid_word(word):
                self.score += 1
                self.baskets[basket_index] = []  
            

    def is_valid_word(self, word):
        try:
            with open('words.txt', 'r') as file:
                valid_words = set(file.read().lower().split())
            return word.lower() in valid_words
        except FileNotFoundError:
            messagebox.showwarning("File Not Found", "The words file was not found. Please ensure it exists.")
            return False
        except Exception as e:
            messagebox.showwarning("Error", f"An error occurred: {str(e)}")
            return False

    def update_display(self):
        for i, basket in enumerate(self.baskets):
            self.basket_labels[i]["text"] = "\n".join(
                basket)  # Update basket labels
        self.score_label["text"] = f"Score: {self.score}"  # Update score
        self.highscore_label["text"] = f"Highest Score {self.highscore}"
        # Show the next letter to be placed
        self.next_letter_label["text"] = f"Next Letter: {self.next_letter}"
        minutes, seconds = divmod(self.time_left, 60)
        # Update timer
        self.timer_label["text"] = f"Time: {minutes:02d}:{seconds:02d}"

    def update_game(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            self.master.after(1000, self.update_game)  # Update every second
        else:
            self.game_running = False
            messagebox.showinfo(
                "Time's up!", f"Game over! Your score: {self.score}")


root = tk.Tk()
game = WordBasketGame(root)
root.mainloop()
