# Move cube from Origin (0,0) to get cube at A (2,2) and then get to B(4,4). 3+ obstacles are in the way, sometimes you cannot reach it. 5x5 grid

# BFS from track start towards (2,2), and obstacles are simply not added to the stack, so an immediate path is taken. Robot moves through this path, reaches the cube and picks it up (a flag will be switched on), then reruns BFS to reach (4,4)
#ideal grid/situation where robot is aware of everything. In an actual physical robot has sensors to detect where it is and what's next to it, and learns the layout of the grid as it runs, requiring several reruns of BFS using updated information to reach the goal.
# certain tracks are impossible, if the target is completely closed off by obstacles. this will be shown by BFS returning no path.

import random
from collections import deque

#Setup initial grid
grid = [ ['X' for _ in range(5)] for _ in range(5)]
grid[2][2] = 'A'
grid[4][4] = 'B' 

obstacleAmount = 4
forbidden = {(0,0), (2,2), (4,4)} #Cells that cannot have obstacles
possibleObstacles = [
   (r, c) for r in range(5) for c in range(5) if (r, c) not in forbidden
   ] #All cells that COULD have obstacles
obstacles = random.sample(possibleObstacles, obstacleAmount) #Pick a certain amount of these cells at random.
      
for obstacle in obstacles: #Put these obstacles into the grid, setup is complete
   grid[obstacle[0]][obstacle[1]] = 'O'
   
print("=== Initial grid ===")
for row in grid:
    print(" ".join(f"{cell:>3}" for cell in row)) 
    #This is just pretty printing. Don't worry about it
    
print()

def bfs_path(start, goal, obstacle_set): #We actually don't need the grid for pathfinding! I only have it for visualization in the console
    queue = deque([[start]]) #Deque used for O(1) popping from the queue
    visited = {start}

    while queue:
        path = queue.popleft()
        r, c = path[-1]

        if (r, c) == goal:
            return path

        # Check adjacent neighbors (Up, Down, Left, Right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            # Within grid, not an obstacle, and not yet visited
            if 0 <= nr < 5 and 0 <= nc < 5:
                if neighbor not in obstacle_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

    return None  # Target unreachable
   
path_to_A = bfs_path((0, 0), (2, 2), obstacles)

if path_to_A is None:
    print("Failed: No path to Point A is available.")
else:
    print("Path to A:", path_to_A)

    # 2. Path from Point A to Point B
    path_to_B = bfs_path((2, 2), (4, 4), obstacles)

    if path_to_B is None:
        print("Failed: No path from Point A to Point B is available.")
    else:
        print("Path to B:", path_to_B)
        
        # Combine routes, excluding the repeated (2, 2)
        full_route = path_to_A + path_to_B[1:]
        for step, (r, c) in enumerate(full_route):
            grid[r][c] = f"{grid[r][c]}{step}"
        print("Full combined route:", full_route)
        print()
        print("=== Grid with Route ===")
        for row in grid:
            print(" ".join(f"{cell:>3}" for cell in row)) #This is just pretty printing. Don't worry about it
