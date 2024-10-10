import tkinter as tk
import numpy as np
import random

class PostmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Postman Village Visit Game")

        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        self.add_village_button = tk.Button(self.button_frame, text="Add Village", command=self.add_village)
        self.add_village_button.pack(side=tk.LEFT)

        self.solve_button = tk.Button(self.button_frame, text="Solve TSP", command=self.solve_tsp)
        self.solve_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT)

        self.villages = []
        self.post_office = (300, 300)  # Fixed post office location
        self.distance_matrix = None

        self.draw_post_office()

    def add_village(self):
        x = random.randint(50, 550)
        y = random.randint(50, 550)
        self.villages.append((x, y))
        self.draw_village(x, y)
        self.update_distance_matrix()
        self.display_coordinates(x, y)

    def draw_village(self, x, y):
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue")

    def draw_post_office(self):
        x, y = self.post_office
        self.canvas.create_rectangle(x-10, y-10, x+10, y+10, fill="green")

    def update_distance_matrix(self):
        num_points = len(self.villages) + 1  # Including post office
        self.distance_matrix = np.zeros((num_points, num_points))

        # Calculate distances
        for i, village in enumerate(self.villages):
            self.distance_matrix[0][i + 1] = self.distance(self.post_office, village)
            self.distance_matrix[i + 1][0] = self.distance(village, self.post_office)
            for j in range(i + 1, len(self.villages)):
                self.distance_matrix[i + 1][j + 1] = self.distance(self.villages[i], self.villages[j])
                self.distance_matrix[j + 1][i + 1] = self.distance(self.villages[j], self.villages[i])

    def display_coordinates(self, x, y):
        # Display the coordinates of the added village
        self.canvas.create_text(x, y - 10, text=f"({x}, {y})", fill="black", font=("Arial", 8))

    def solve_tsp(self):
        if len(self.villages) < 1:
            return

        min_cost, best_path, costs = self.nearest_neighbor_tsp()
        self.draw_path([self.post_office] + [self.villages[i] for i in best_path] + [self.post_office], costs)
        print(f"Minimum cost: {min_cost}")
        self.display_cost(min_cost)

    def draw_path(self, path, costs):
        for i in range(len(path) - 1):
            self.canvas.create_line(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1], fill="red", width=2)
            if i < len(costs):  # Display costs between villages
                mid_x = (path[i][0] + path[i + 1][0]) / 2
                mid_y = (path[i][1] + path[i + 1][1]) / 2
                self.canvas.create_text(mid_x, mid_y - 10, text=f"{costs[i]:.2f}", fill="black", font=("Arial", 8))

    def nearest_neighbor_tsp(self):
        num_villages = len(self.villages)
        visited = [False] * num_villages
        current_index = 0  # Start at the post office (index 0)
        total_cost = 0
        path = []
        costs = []

        # Nearest Neighbor algorithm
        for _ in range(num_villages):
            path.append(current_index)
            visited[current_index] = True
            next_index = -1
            next_cost = float('inf')

            for j in range(num_villages):
                if not visited[j] and self.distance_matrix[current_index + 1][j + 1] < next_cost:
                    next_cost = self.distance_matrix[current_index + 1][j + 1]
                    next_index = j

            if next_index != -1:
                costs.append(next_cost)  # Record the cost to the next village
                total_cost += next_cost
                current_index = next_index

        # Return to the post office
        return_cost = self.distance_matrix[current_index + 1][0]
        total_cost += return_cost
        costs.append(return_cost)  # Record the return cost
        path.append(-1)  # Append post office index (-1 represents post office)

        return total_cost, path, costs

    def display_cost(self, cost):
        # Display the minimum cost on the canvas
        self.canvas.create_text(300, 550, text=f"Minimum cost: {cost:.2f}", fill="red", font=("Arial", 12))

    def distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def reset(self):
        self.canvas.delete("all")
        self.villages = []
        self.draw_post_office()
        self.distance_matrix = None

if __name__ == "__main__":
    root = tk.Tk()
    game = PostmanGame(root)
    root.mainloop()
