import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, depth=0, cost=0):
        self.state = state  # 3x3 matrix as a tuple
        self.parent = parent  # Parent node
        self.move = move  # Move taken to reach this state
        self.depth = depth  # Depth level in search tree
        self.cost = cost  # Cost of reaching this state
        self.blank_pos = state.index(0)  # Find blank (zero) position
    
    def __lt__(self, other):
        return (self.cost + self.heuristic()) < (other.cost + other.heuristic())
    
    def heuristic(self):  # Manhattan distance heuristic
        distance = 0
        goal = {1: (0,0), 2: (0,1), 3: (0,2), 4: (1,0), 5: (1,1), 6: (1,2), 7: (2,0), 8: (2,1), 0: (2,2)}
        for index, value in enumerate(self.state):
            if value != 0:
                x, y = divmod(index, 3)
                goal_x, goal_y = goal[value]
                distance += abs(x - goal_x) + abs(y - goal_y)
        return distance

    def get_neighbors(self):
        neighbors = []
        x, y = divmod(self.blank_pos, 3)
        moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        
        for move, (dx, dy) in moves.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_blank_pos = nx * 3 + ny
                new_state = list(self.state)
                new_state[self.blank_pos], new_state[new_blank_pos] = new_state[new_blank_pos], new_state[self.blank_pos]
                neighbors.append(PuzzleNode(tuple(new_state), self, move, self.depth + 1, self.cost + 1))
        
        return neighbors

def solve_puzzle(start_state):
    priority_queue = []
    heapq.heappush(priority_queue, PuzzleNode(start_state))
    visited = set()
    
    while priority_queue:
        node = heapq.heappop(priority_queue)
        
        if node.state == (1, 2, 3, 4, 5, 6, 7, 8, 0):
            return get_solution_path(node)
        
        visited.add(node.state)
        for neighbor in node.get_neighbors():
            if neighbor.state not in visited:
                heapq.heappush(priority_queue, neighbor)
    
    return None

def get_solution_path(node):
    path = []
    while node.parent:
        path.append(node.move)
        node = node.parent
    return path[::-1]

# Example Usage
initial_state = (1, 2, 3, 4, 0, 5, 6, 7, 8)  # Example starting state
solution = solve_puzzle(initial_state)
print("Solution Steps:", solution)
