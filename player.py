import pygame

class Player:
    def __init__(self, x, y, tile_size):
        self.x, self.y = x, y
        self.tile_size = tile_size  # Store the tile size

    def draw(self, screen):
        px, py = self.x * self.tile_size + self.tile_size // 2, self.y * self.tile_size + self.tile_size // 2
        pygame.draw.circle(screen, pygame.Color('blue'), (px, py), self.tile_size // 4)

    def move(self, direction, grid_cells, cols):
        # Locate current cell
        current_cell = grid_cells[self.x + self.y * cols]

        # Check if the move is valid
        if direction == "UP" and not current_cell.walls['top']:
            self.y -= 1
        elif direction == "RIGHT" and not current_cell.walls['right']:
            self.x += 1
        elif direction == "DOWN" and not current_cell.walls['bottom']:
            self.y += 1
        elif direction == "LEFT" and not current_cell.walls['left']:
            self.x -= 1
