import pygame
from map import Map

WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Player:
    def __init__(self, start_position, cell_size, game_map):
        self.x, self.y = start_position
        self.cell_size = cell_size
        self.map = game_map
        self.position_history = []
        
    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        
        if self.is_valid_move(new_x, new_y):
            self.position_history.append((self.x, self.y))  # save position
            self.x = new_x
            self.y = new_y

    def is_valid_move(self, x, y):
        if 0 <= x < self.map.cols and 0 <= y < self.map.rows:
            if self.map.grid[y][x] == 0:  # check if cell walkable
                return True
        return False
    
    def render(self, screen):
        pygame.draw.rect(screen, RED, (self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size))
