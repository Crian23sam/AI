import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

questions = {
    "easy": [
        {"question": "What is the capital of India?", "answer": "New Delhi", "options": ["New Delhi", "Mumbai", "Kolkata", "Chennai"]},
        {"question": "What is the national animal of India?", "answer": "Tiger", "options": ["Tiger", "Lion", "Elephant", "Horse"]},
        {"question": "What is the national bird of India?", "answer": "Peacock", "options": ["Peacock", "Eagle", "Sparrow", "Parrot"]},
    ],
    "medium": [
        {"question": "Who is the Prime Minister of India?", "answer": "Narendra Modi", "options": ["Narendra Modi", "Rajiv Gandhi", "Manmohan Singh", "Atal Bihari Vajpayee"]},
        {"question": "What is the national flower of India?", "answer": "Lotus", "options": ["Lotus", "Rose", "Lily", "Sunflower"]},
    ],
    "hard": [
        {"question": "Who is known as the Father of the Nation in India?", "answer": "Mahatma Gandhi", "options": ["Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel", "Subhas Chandra Bose"]},
        {"question": "Which city is known as the Pink City of India?", "answer": "Jaipur", "options": ["Jaipur", "Delhi", "Agra", "Bengaluru"]},
    ]
}

class GovindaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Govinda Game")
        self.root.geometry("700x700")
        self.root.config(bg="#f2f2f2")

        original_image = Image.open("matki.png")
        self.matki_image = original_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.matki_photo = ImageTk.PhotoImage(self.matki_image)

        self.player_pyramid_layer = 8
        self.ai_pyramid_layer = 8
        self.current_turn = "player"

        self.difficulty_frame = tk.Frame(root, bg="#f2f2f2")
        self.difficulty_frame.pack(pady=30)

        self.difficulty_var = tk.StringVar(value="easy")

        tk.Label(self.difficulty_frame, text="Select Difficulty", font=("Helvetica", 20, "bold"), bg="#f2f2f2").pack(pady=10)
        
        for level in ["easy", "medium", "hard"]:
            tk.Radiobutton(self.difficulty_frame, text=level.capitalize(), variable=self.difficulty_var, value=level, font=("Helvetica", 14), bg="#f2f2f2").pack(anchor=tk.W, padx=20)

        self.start_button = tk.Button(self.difficulty_frame, text="Start Game", command=self.start_game, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", relief="raised", padx=20, pady=10)
        self.start_button.pack(pady=20)

    def start_game(self):
        self.difficulty = self.difficulty_var.get()
        self.difficulty_frame.pack_forget()

        self.question_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.question_frame.pack(pady=20)

        self.question_label = tk.Label(self.question_frame, text="", font=("Helvetica", 16, "bold"), bg="#f2f2f2")
        self.question_label.pack()

        self.options_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.options_frame.pack(pady=20)

        self.option_vars = tk.StringVar()
        self.option_vars.set(None)

        self.option_buttons = []
        for i in range(4):
            option_button = tk.Radiobutton(self.options_frame, text="", variable=self.option_vars, value="", font=("Helvetica", 14), bg="#f2f2f2", selectcolor="#4CAF50")
            option_button.pack(anchor=tk.W, padx=20)
            self.option_buttons.append(option_button)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_answer, font=("Helvetica", 14, "bold"), bg="#FF6347", fg="white", relief="raised", padx=20, pady=10)
        self.submit_button.pack()

        self.tower_frame = tk.Canvas(self.root, width=600, height=450, bg="#ADD8E6", bd=0, highlightthickness=0)
        self.tower_frame.pack(pady=20)

        self.matki_id = self.tower_frame.create_image(300, 50, anchor=tk.N, image=self.matki_photo)

        self.ask_question()

    def ask_question(self):
        if self.current_turn == "player":
            self.current_question = random.choice(questions[self.difficulty])
            self.question_label.config(text=self.current_question["question"])
            options = self.current_question["options"]
            random.shuffle(options)

            for i, option in enumerate(options):
                self.option_buttons[i].config(text=option, value=option)
        else:
            self.ai_answer()

    def check_answer(self):
        selected_option = self.option_vars.get().strip().lower()
        correct_answer = self.current_question["answer"].strip().lower()

        if selected_option == correct_answer:
            self.player_pyramid_layer -= 1
            self.add_player_layer()
            if self.player_pyramid_layer < 0:
                self.end_game("You won, Broke the Matki!")
        else:
            messagebox.showerror("Wrong Answer", "Incorrect! Try again.")

        self.current_turn = "ai"
        self.ask_question()

    def ai_answer(self):
        if random.choice([True, False]):
            self.ai_pyramid_layer -= 1
            self.add_ai_layer()
            if self.ai_pyramid_layer < 0:
                self.end_game("AI won, Broke the Matki!")
        else:
            messagebox.showinfo("AI Wrong Answer", "AI made a mistake!")

        self.current_turn = "player"
        self.ask_question()

    def add_player_layer(self):
        self.draw_pyramid_layer(self.player_pyramid_layer, "black")

    def add_ai_layer(self):
        self.draw_pyramid_layer(self.ai_pyramid_layer, "red")

    def draw_pyramid_layer(self, layer, color):
        y = 450 - ((8 - layer) * 60)
        num_people = layer
        for i in range(num_people):
            x = (i * 60) + (300 - (num_people * 30))
            self.draw_stick_figure(x, y, color)

    def draw_stick_figure(self, x, y, color):
        figure_size = 30
        
        self.tower_frame.create_oval(x+5, y, x+figure_size, y+figure_size, fill=color, outline="black")
        self.tower_frame.create_line(x + figure_size // 2, y + figure_size, x + figure_size // 2, y + figure_size + 20, fill=color, width=2)
        self.tower_frame.create_line(x + 5, y + 15, x + figure_size - 5, y + 15, fill=color, width=2)
        self.tower_frame.create_line(x + figure_size // 2, y + 20, x + 5, y + 40, fill=color, width=2)
        self.tower_frame.create_line(x + figure_size // 2, y + 20, x + figure_size - 5, y + 40, fill=color, width=2)

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.ask_restart()

    def ask_restart(self):
        restart = messagebox.askyesno("Restart", "Do you want to play again?")
        if restart:
            self.reset_game()
        else:
            self.root.quit()

    def reset_game(self):
        self.tower_frame.delete("all")
        self.tower_frame.create_image(300, 50, anchor=tk.N, image=self.matki_photo)
        self.player_pyramid_layer = 8
        self.ai_pyramid_layer = 8
        self.current_turn = "player"
        self.ask_question()

if __name__ == "__main__":
    root = tk.Tk()
    game = GovindaGame(root)
    root.mainloop()
