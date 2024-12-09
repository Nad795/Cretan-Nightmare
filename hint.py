import pygame
from collections import deque

class Hint:
    def __init__(self, x, y, tile_size):
        self.x, self.y = x, y
        self.tile_size = tile_size
        self.active = False
        self.path = []
        self.activation_time = 0  # Time when the hint is activated

        # Load the hint icon
        self.hint_icon = pygame.image.load('assets/hint-icon.png')
        # Scale the hint icon to fit within the tile
        self.hint_icon = pygame.transform.scale(self.hint_icon, (tile_size // 1.2, tile_size // 1.2))


    def draw(self, screen):
        # Draw the hint icon at the current position
        hx = self.x * self.tile_size + (self.tile_size - self.hint_icon.get_width()) // 2
        hy = self.y * self.tile_size + (self.tile_size - self.hint_icon.get_height()) // 2
        screen.blit(self.hint_icon, (hx, hy))

        # If the hint is active, draw the path as circles
        if self.active:
            for hx, hy in self.path:
                # Calculate the position for the center of the circle
                circle_x = hx * self.tile_size + self.tile_size // 2
                circle_y = hy * self.tile_size + self.tile_size // 2
                # Set the radius of the circle to be smaller
                radius = self.tile_size // 8  # Adjust this value as needed

                pygame.draw.circle(
                    screen,
                    pygame.Color(255, 187, 70, 255),  # Yellow color with transparency
                    (circle_x, circle_y),
                    radius
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
                return path[:15]  # Limit path to 15 steps
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
