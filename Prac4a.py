import tkinter as tk
import heapq

# Define the grid dimensions
GRID_SIZE = 20
CELL_SIZE = 30

# Heuristic function (Manhattan distance)
def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# A* algorithm
def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    heapq.heappush(open_list, (0, start))  # (cost, node)
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_list:
        current = heapq.heappop(open_list)[1]
        
        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Return reversed path
        
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return None

# GUI class
class AStarGame:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Pathfinding Game")
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.start = None
        self.goal = None
        self.canvas = tk.Canvas(self.root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
        self.canvas.pack()
        
        self.draw_grid()
        
        self.canvas.bind("<Button-1>", self.place_cell)
        self.run_button = tk.Button(self.root, text="Run A*", command=self.run_astar)
        self.run_button.pack()
    
    def draw_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = "white"
                if self.grid[i][j] == 1:
                    color = "black"
                self.canvas.create_rectangle(j*CELL_SIZE, i*CELL_SIZE, (j+1)*CELL_SIZE, (i+1)*CELL_SIZE, fill=color, outline="gray")
    
    def place_cell(self, event):
        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        if not self.start:
            self.start = (y, x)
            self.canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill="green", outline="gray")
        elif not self.goal:
            self.goal = (y, x)
            self.canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill="red", outline="gray")
        else:
            if self.grid[y][x] == 0:
                self.grid[y][x] = 1
                self.canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill="black", outline="gray")
    
    def run_astar(self):
        if self.start and self.goal:
            path = a_star(self.grid, self.start, self.goal)
            if path:
                for node in path:
                    y, x = node
                    if node != self.start and node != self.goal:
                        self.canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill="blue", outline="gray")
            else:
                print("No path found!")

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = AStarGame(root)
    root.mainloop()
