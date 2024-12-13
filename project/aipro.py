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
        self.root.geometry("600x600")

        # Load matki image and resize
        original_image = Image.open("matki.png")
        self.matki_image = original_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.matki_photo = ImageTk.PhotoImage(self.matki_image)

        # Frame for difficulty selection
        self.difficulty_frame = tk.Frame(root)
        self.difficulty_frame.pack(pady=20)

        # Difficulty selection
        self.difficulty_var = tk.StringVar(value="easy")

        tk.Label(self.difficulty_frame, text="Select Difficulty:", font=("Arial", 16)).pack()
        tk.Radiobutton(self.difficulty_frame, text="Easy", variable=self.difficulty_var, value="easy", font=("Arial", 14)).pack()
        tk.Radiobutton(self.difficulty_frame, text="Medium", variable=self.difficulty_var, value="medium", font=("Arial", 14)).pack()
        tk.Radiobutton(self.difficulty_frame, text="Hard", variable=self.difficulty_var, value="hard", font=("Arial", 14)).pack()

        # Start button
        self.start_button = tk.Button(self.difficulty_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

    def start_game(self):
        self.difficulty = self.difficulty_var.get()
        self.difficulty_frame.pack_forget()  # Hide difficulty selection frame

        # Player and AI stats
        self.player_pyramid_layer = 8  # Pyramid starts with 8 layers
        self.ai_pyramid_layer = 8

        self.current_turn = "player"  # Start with the player

        # Frame for the question
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=20)

        # Question label
        self.question_label = tk.Label(self.question_frame, text="", font=("Arial", 16))
        self.question_label.pack()

        # Frame for answer options
        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(pady=20)

        # Initialize radio buttons for answer options
        self.option_vars = tk.StringVar()
        self.option_vars.set(None)

        self.option_buttons = []
        for i in range(4):  # Up to 4 options
            option_button = tk.Radiobutton(self.options_frame, text="", variable=self.option_vars, value="", font=("Arial", 14))
            option_button.pack(anchor=tk.W)
            self.option_buttons.append(option_button)

        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_answer)
        self.submit_button.pack()

        # Frame for the tower (Govinda pyramid)
        self.tower_frame = tk.Canvas(self.root, width=600, height=450, bg="lightblue")
        self.tower_frame.pack(pady=20)

        # Display matki image at the top center of the tower frame
        self.matki_id = self.tower_frame.create_image(300, 50, anchor=tk.N, image=self.matki_photo)

        # Ask first question
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
            # AI's turn to answer the question
            self.ai_answer()

    def check_answer(self):
        selected_option = self.option_vars.get().strip().lower()
        correct_answer = self.current_question["answer"].strip().lower()

        if selected_option == correct_answer:
            self.player_pyramid_layer -= 1
            self.add_player_layer()
            if self.player_pyramid_layer < 0:
                messagebox.showinfo("You Won!", "You won, Broke the Matki!")
                self.reset_game()
        else:
            messagebox.showerror("Wrong Answer", "Incorrect! Try again.")

        # AI's turn next
        self.current_turn = "ai"
        self.ask_question()

    def ai_answer(self):
        # AI will answer the question (simulate with a random correct or incorrect answer)
        if random.choice([True, False]):
            self.ai_pyramid_layer -= 1
            self.add_ai_layer()
            if self.ai_pyramid_layer < 0:
                messagebox.showinfo("AI Won", "AI won, Broke the Matki!")
                self.reset_game()
        else:
            messagebox.showinfo("AI Wrong Answer", "AI made a mistake!")

        # Player's turn next
        self.current_turn = "player"
        self.ask_question()

    def add_player_layer(self):
        self.draw_pyramid_layer(self.player_pyramid_layer, "black")

    def add_ai_layer(self):
        self.draw_pyramid_layer(self.ai_pyramid_layer, "red")

    def draw_pyramid_layer(self, layer, color):
        # Calculate the position for the current layer
        y = 450 - ((8 - layer) * 60)  # Draw from the bottom upwards
        num_people = layer  # Start with 8 people at the base, then decrease
        for i in range(num_people):
            x = (i * 60) + (300 - (num_people * 30))  # Center people in the layer
            self.draw_stick_figure(x, y, color)

    def draw_stick_figure(self, x, y, color):
        # Draw head (circle)
        self.tower_frame.create_oval(x+10, y, x+30, y+20, fill=color)  # Head

        # Draw body
        self.tower_frame.create_line(x+20, y+20, x+20, y+50, fill=color, width=2)  # Body

        # Draw arms
        self.tower_frame.create_line(x+5, y+30, x+35, y+30, fill=color, width=2)  # Arms

        # Draw legs
        self.tower_frame.create_line(x+20, y+50, x+10, y+70, fill=color, width=2)  # Left leg
        self.tower_frame.create_line(x+20, y+50, x+30, y+70, fill=color, width=2)  # Right leg

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
