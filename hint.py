import pygame
from collections import deque

class Hint:
    def __init__(self, x, y, tile_size):
        self.x, self.y = x, y
        self.tile_size = tile_size
        self.active = False
        self.path = []
        self.activation_time = 0  # Time when the hint is activated

    def draw(self, screen):
        # Draw the hint at the current position
        hx, hy = self.x * self.tile_size + self.tile_size // 4, self.y * self.tile_size + self.tile_size // 4
        pygame.draw.rect(screen, pygame.Color('yellow'), (hx, hy, self.tile_size // 2, self.tile_size // 2))

        # If the hint is active, draw the path
        if self.active:
            for hx, hy in self.path:
                pygame.draw.rect(
                    screen,
                    pygame.Color(0, 255, 255, 128),
                    (hx * self.tile_size + self.tile_size // 4, hy * self.tile_size + self.tile_size // 4, self.tile_size // 2, self.tile_size // 2)
                )

    def bfs(self, grid_cells, cols, rows, start_x, start_y, exit_x, exit_y):
        """Find the shortest path using BFS."""
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # top, right, bottom, left
        queue = deque([(start_x, start_y)])
        visited = set()
        visited.add((start_x, start_y))
        parent = {}

        while queue:
            x, y = queue.popleft()
            if (x, y) == (exit_x, exit_y):
                # Build path from parent dictionary
                path = []
                while (x, y) != (start_x, start_y):
                    path.append((x, y))
                    x, y = parent[(x, y)]
                path.reverse()
                return path[:10]  # Limit path to 10 steps
            current_cell = grid_cells[x + y * cols]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                    neighbor = grid_cells[nx + ny * cols]
                    # Check for walls and only add valid neighbors
                    if (dx, dy) == (0, -1) and not current_cell.walls['top']:  # Moving up
                        queue.append((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        visited.add((nx, ny))
                    elif (dx, dy) == (1, 0) and not current_cell.walls['right']:  # Moving right
                        queue.append((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        visited.add((nx, ny))
                    elif (dx, dy) == (0, 1) and not current_cell.walls['bottom']:  # Moving down
                        queue.append((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        visited.add((nx, ny))
                    elif (dx, dy) == (-1, 0) and not current_cell.walls['left']:  # Moving left
                        queue.append((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        visited.add((nx, ny))
        return []  # No path found

    def activate(self, grid_cells, cols, rows, player_x, player_y, exit_x, exit_y):
        """Activate the hint by calculating the path."""
        self.active = True
        self.path = self.bfs(grid_cells, cols, rows, player_x, player_y, exit_x, exit_y)
        self.activation_time = pygame.time.get_ticks()  # Record the time when the hint was activated

    def deactivate(self):
        """Deactivate the hint after 5 seconds."""
        if self.active and pygame.time.get_ticks() - self.activation_time > 5000:  # 5 seconds
            self.active = False
            self.path = []  # Clear the path when the hint is deactivated
