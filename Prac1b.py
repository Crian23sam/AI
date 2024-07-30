import tkinter as tk
from tkinter import simpledialog, messagebox
from collections import deque

class GraphVisualization(tk.Tk):
    def __init__(self, graph):
        super().__init__()
        self.title("Breadth First Search Visualization")
        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")
        self.canvas.pack()
        self.graph = graph
        self.node_positions = {}
        self.visited = set()
        self.paths = []  # To store all paths to the goal node
        self.goal_node = None

        # Adding Entry for goal node input
        self.goal_label = tk.Label(self, text="Enter Goal Node:")
        self.goal_label.pack(pady=5)
        self.goal_entry = tk.Entry(self)
        self.goal_entry.pack(pady=5)
        self.start_button = tk.Button(self, text="Start BFS", command=self.start_bfs)
        self.start_button.pack(pady=5)

        self.setup_graph()

    def setup_graph(self):
        # Predefined node positions for simplicity
        self.node_positions = {
            'A': (300, 50),
            'B': (150, 150),
            'C': (450, 150),
            'D': (100, 250),
            'E': (200, 250),
            'F': (400, 250)
        }

        # Draw nodes
        for node, position in self.node_positions.items():
            x, y = position
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue", tags=node)
            self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))

        # Draw edges
        for node, neighbors in self.graph.items():
            x1, y1 = self.node_positions[node]
            for neighbor in neighbors:
                x2, y2 = self.node_positions[neighbor]
                self.canvas.create_line(x1, y1, x2, y2, tags=f"{node}-{neighbor}")

    def start_bfs(self):
        self.goal_node = self.goal_entry.get().strip().upper()
        if self.goal_node not in self.graph:
            messagebox.showerror("Error", f"Goal node '{self.goal_node}' not found in graph!")
            return

        self.visited.clear()
        self.paths.clear()
        self.canvas.delete("highlight")
        self.bfs('A')

        if not self.paths:
            messagebox.showinfo("Result", f"No path found to goal node '{self.goal_node}'")
        else:
            paths_str = "\n".join([" -> ".join(path) for path in self.paths])
            messagebox.showinfo("Result", f"Paths to goal node '{self.goal_node}':\n{paths_str}")

    def bfs(self, start_node):
        queue = deque([(start_node, [start_node])])
        self.visited.add(start_node)
        x, y = self.node_positions[start_node]
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightgreen", tags="highlight")
        self.update()
        self.after(500)

        while queue:
            node, path = queue.popleft()
            if node == self.goal_node:
                self.paths.append(path)
                continue

            for neighbor in self.graph[node]:
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
                    x1, y1 = self.node_positions[node]
                    x2, y2 = self.node_positions[neighbor]
                    self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags="highlight")
                    self.update()
                    self.after(500)
                    x, y = self.node_positions[neighbor]
                    self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightgreen", tags="highlight")
                    self.update()
                    self.after(500)

if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B','F'],
        'F': ['C','E']
    }

    app = GraphVisualization(graph)
    app.mainloop()
