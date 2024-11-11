# generate map pake DFS

import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
class Map:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.end = (rows - 1, cols - 1)
        self.generate_maze()
        
    def generate_maze(self):
        stack = [self.start]
        visited = set()
        visited.add(self.start)
        self.grid[self.start[0]][self.start[1]] = 0
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while stack:
            current = stack[-1]
            neighbors = []
            
            for direction in directions:
                nx, ny = current[0] + direction[0] * 2, current[1] + direction[1] * 2
                if 0 <= nx < self.rows and 0 <= ny < self.cols and (nx, ny) not in visited:
                    neighbors.append((nx, ny))
                    
            if neighbors:
                next_cell = random.choice(neighbors)
                stack.append(next_cell)
                visited.add(next_cell)
                
                wall_x = (current[0] + next_cell[0]) // 2
                wall_y = (current[1] + next_cell[1]) // 2
                self.grid[wall_x][wall_y] = 0
                self.grid[next_cell[0]][next_cell[1]] = 0
            else:
                stack.pop()
                
    def render(self, screen, cell_size):
        screen_width, screen_height = screen.get_size()
        
        map_width = self.cols * cell_size
        map_height = self.rows * cell_size
        
        offset_x = (screen_width - map_width) // 2
        offset_y = (screen_height - map_height) // 2
        
        for row in range(self.rows):
            for col in range(self.cols):
                color = BLACK if self.grid[row][col] == 1 else WHITE
                pygame.draw.rect(screen, color, (offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size))