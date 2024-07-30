import tkinter as tk
from collections import deque
from tkinter import messagebox

class WaterJugProblem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Water Jug Problem")
        self.geometry("600x400")

        self.label_jug1 = tk.Label(self, text="Jug 1 Capacity:")
        self.label_jug1.pack(pady=5)
        self.entry_jug1 = tk.Entry(self)
        self.entry_jug1.pack(pady=5)

        self.label_jug2 = tk.Label(self, text="Jug 2 Capacity:")
        self.label_jug2.pack(pady=5)
        self.entry_jug2 = tk.Entry(self)
        self.entry_jug2.pack(pady=5)

        self.label_target = tk.Label(self, text="Target Amount:")
        self.label_target.pack(pady=5)
        self.entry_target = tk.Entry(self)
        self.entry_target.pack(pady=5)

        self.solve_button = tk.Button(self, text="Solve", command=self.solve_problem)
        self.solve_button.pack(pady=20)

        self.canvas = tk.Canvas(self, width=400, height=200, bg="white")
        self.canvas.pack(pady=20)

        self.result_label = tk.Label(self, text="", wraplength=500)
        self.result_label.pack(pady=10)

    def solve_problem(self):
        try:
            jug1_capacity = int(self.entry_jug1.get())
            jug2_capacity = int(self.entry_jug2.get())
            target = int(self.entry_target.get())

            solution = self.water_jug_problem(jug1_capacity, jug2_capacity, target)

            if solution:
                result_text = "Solution path: " + " -> ".join([f"({x},{y})" for x, y in solution])
                self.visualize_solution(solution, jug1_capacity, jug2_capacity)
            else:
                result_text = "No solution found."
                self.clear_canvas()

            self.result_label.config(text=result_text)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid integer values for the capacities and target amount.")

    def water_jug_problem(self, jug1_capacity, jug2_capacity, target):
        visited = set()
        path = []

        queue = deque([(0, 0)])  # Initial state: both jugs are empty

        while queue:
            current = queue.popleft()

            if current in visited:
                continue

            visited.add(current)
            path.append(current)

            jug1, jug2 = current
            if jug1 == target or jug2 == target:
                return path

            # Define all possible next states
            next_states = [
                (jug1_capacity, jug2),  # Fill jug1
                (jug1, jug2_capacity),  # Fill jug2
                (0, jug2),              # Empty jug1
                (jug1, 0),              # Empty jug2
                (min(jug1 + jug2, jug1_capacity), jug2 - (min(jug1_capacity - jug1, jug2))),  # Pour jug2 into jug1
                (jug1 - (min(jug2_capacity - jug2, jug1)), min(jug1 + jug2, jug2_capacity))   # Pour jug1 into jug2
            ]

            for state in next_states:
                if state not in visited:
                    queue.append(state)

        return None

    def visualize_solution(self, solution, jug1_capacity, jug2_capacity):
        self.clear_canvas()
        jug1_x, jug1_y = 100, 50
        jug2_x, jug2_y = 300, 50
        jug_width, jug_height = 80, 150

        for jug1, jug2 in solution:
            self.canvas.create_rectangle(jug1_x, jug1_y, jug1_x + jug_width, jug1_y + jug_height, outline="blue", width=2)
            self.canvas.create_rectangle(jug2_x, jug2_y, jug2_x + jug_width, jug2_y + jug_height, outline="blue", width=2)

            jug1_water_height = jug_height * jug1 / jug1_capacity
            jug2_water_height = jug_height * jug2 / jug2_capacity

            self.canvas.create_rectangle(jug1_x, jug1_y + jug_height - jug1_water_height, jug1_x + jug_width, jug1_y + jug_height, fill="blue")
            self.canvas.create_rectangle(jug2_x, jug2_y + jug_height - jug2_water_height, jug2_x + jug_width, jug2_y + jug_height, fill="blue")

            self.canvas.create_text(jug1_x + jug_width / 2, jug1_y + jug_height + 20, text=f"Jug 1: {jug1}/{jug1_capacity}")
            self.canvas.create_text(jug2_x + jug_width / 2, jug2_y + jug_height + 20, text=f"Jug 2: {jug2}/{jug2_capacity}")

            self.update()
            self.after(1000)

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    app = WaterJugProblem()
    app.mainloop()
