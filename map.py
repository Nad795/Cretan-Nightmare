import pygame
from random import choice
from player import Player
from hint import Hint

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw(self, screen, cell_size):
        x, y = self.x * cell_size, self.y * cell_size
        if self.visited:
            pygame.draw.rect(screen, pygame.Color('black'), (x, y, cell_size, cell_size))
        
        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y), (x + cell_size, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + cell_size, y), (x + cell_size, y + cell_size), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + cell_size, y + cell_size), (x, y + cell_size), 2)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y + cell_size), (x, y), 2)

    def check_neighbors(self, grid_cells, cols, rows):
        neighbors = []
        find_index = lambda x, y: x + y * cols
        directions = [
            (0, -1),  # top
            (1, 0),   # right
            (0, 1),   # bottom
            (-1, 0)   # left
        ]
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                neighbor = grid_cells[find_index(nx, ny)]
                if not neighbor.visited:
                    neighbors.append(neighbor)
        return choice(neighbors) if neighbors else None


def remove_walls(current, next):
    dx = current.x - next.x
    dy = current.y - next.y
    if dx == 1:  # left
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:  # right
        current.walls['right'] = False
        next.walls['left'] = False
    if dy == 1:  # top
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:  # bottom
        current.walls['bottom'] = False
        next.walls['top'] = False


class Map:
    def __init__(self, cols, rows, cell_size):
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
        self.stack = []
        self.current_cell = self.grid_cells[0]

        # Player and hint setup
        self.player = Player(0, 0, cell_size)
        self.hint = Hint(cols - 1, rows - 1, cell_size)
        self.finish_cell = None  # Titik finish yang akan ditentukan saat DFS selesai

    def generate(self):
        self.current_cell.visited = True
        next_cell = self.current_cell.check_neighbors(self.grid_cells, self.cols, self.rows)
        if next_cell:
            next_cell.visited = True
            self.stack.append(self.current_cell)
            remove_walls(self.current_cell, next_cell)
            self.current_cell = next_cell
        elif self.stack:
            self.current_cell = self.stack.pop()

        # Setelah DFS selesai, tentukan titik finish di titik paling dalam DFS
        if not self.stack:
            self.finish_cell = self.current_cell

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player.move("UP", self.grid_cells, self.cols)
            elif event.key == pygame.K_DOWN:
                self.player.move("DOWN", self.grid_cells, self.cols)
            elif event.key == pygame.K_LEFT:
                self.player.move("LEFT", self.grid_cells, self.cols)
            elif event.key == pygame.K_RIGHT:
                self.player.move("RIGHT", self.grid_cells, self.cols)
            elif event.key == pygame.K_h:
                self.hint.activate(self, self.player.x, self.player.y)

    def check_collision_with_finish(self):
        # Jika pemain berada di titik finish, akhiri permainan
        if self.player.x == self.finish_cell.x and self.player.y == self.finish_cell.y:
            pygame.quit()
            quit()

    def render(self, screen):
        # Render cells
        for cell in self.grid_cells:
            cell.draw(screen, self.cell_size)

        # Render player and hint
        self.player.draw(screen)
        self.hint.draw(screen)

        # Render titik finish sebagai kotak hijau
        if self.finish_cell:
            fx, fy = self.finish_cell.x * self.cell_size, self.finish_cell.y * self.cell_size
            pygame.draw.rect(screen, pygame.Color('green'), (fx, fy, self.cell_size, self.cell_size))
