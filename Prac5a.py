from collections import deque

def water_jug_problem(jug1_capacity, jug2_capacity, target):

    visited = set()
    path = []

    queue = deque([(0, 0)])

    while queue:
        current = queue.popleft()

        if current in visited:
            continue

        visited.add(current)
        path.append(current)

        jug1, jug2 = current
        if jug1 == target or jug2 == target:
            return path

        next_states = [
            (jug1_capacity, jug2),       # Fill jug1
            (jug1, jug2_capacity),       # Fill jug2
            (0, jug2),                   # Empty jug1
            (jug1, 0),                   # Empty jug2
            (min(jug1 + jug2, jug1_capacity), jug2 - (min(jug1 + jug2, jug1_capacity) - jug1)),  # Pour jug2 into jug1
            (jug1 - (min(jug1 + jug2, jug2_capacity) - jug2), min(jug1 + jug2, jug2_capacity)),  # Pour jug1 into jug2
        ]

        for state in next_states:
            if state not in visited:
                queue.append(state)

    return None

jug1_capacity = 5
jug2_capacity = 4
target = 2
solution = water_jug_problem(jug1_capacity, jug2_capacity, target)

if solution:
    print("Solution path:", solution)
else:
    print("No solution found.")
