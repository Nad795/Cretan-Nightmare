import pygame
from random import choice, randrange
from player import Player
from hint import Hint
from finish import Fin

RES = WIDTH, HEIGHT = 800, 600
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE

hint_timer = 0
hint_active_duration = 5000 

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

        # Player setup
        self.player = Player(0, 0, cell_size)

        # Finish setup
        self.finish = Fin(cols, rows, self.grid_cells)

        # Hint setup
        self.hint = self.setup_hint()
        self.hint_active_time = None

    def setup_hint(self):
        while True:
            hint_x, hint_y = randrange(self.cols), randrange(self.rows)
            if (hint_x, hint_y) != (0, 0) and (hint_x, hint_y) != (self.finish.finish_cell.x, self.finish.finish_cell.y):  # Ensure hint is not at start or finish
                return Hint(hint_x, hint_y, self.cell_size)

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

        if not self.stack and not self.finish.finish_cell:
            self.finish.finish_cell = max(
                self.grid_cells,
                key=lambda cell: abs(cell.x - 0) + abs(cell.y - 0)
            )

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

    def render(self, screen):
        for cell in self.grid_cells:
            cell.draw(screen, self.cell_size)

        # Render the hint
        self.hint.draw(screen)
        if self.hint.active:
            for hx, hy in self.hint.path:
                pygame.draw.rect(
                    screen, 
                    pygame.Color(0, 255, 255, 128), 
                    (hx * TILE + TILE // 4, hy * TILE + TILE // 4, TILE // 2, TILE // 2)
                )

        # Render the finish
        if self.finish.finish_cell:
            ex, ey = self.finish.finish_cell.x * self.cell_size, self.finish.finish_cell.y * self.cell_size
            pygame.draw.rect(screen, pygame.Color('green'), (ex, ey, self.cell_size, self.cell_size))

        # Render the hint
        if self.player.x == self.hint.x and self.player.y == self.hint.y:
            self.hint.activate(
                self.grid_cells, self.cols, self.rows, 
                self.player.x, self.player.y, 
                self.finish.finish_cell.x, self.finish.finish_cell.y
            )
            self.hint_active_time = pygame.time.get_ticks()
        
        if self.hint_active_time and pygame.time.get_ticks() - self.hint_active_time > hint_active_duration:
            self.hint.deactivate()

        # Render the player
        self.player.draw(screen)

    def check_collision_with_finish(self):
        player_cell_x = self.player.x // self.cell_size  # Convert pixel position to grid cell index
        player_cell_y = self.player.y // self.cell_size  # Convert pixel position to grid cell index

        if player_cell_x == self.finish.finish_cell.x and player_cell_y == self.finish.finish_cell.y:
            print("Player reached the finish!")
            pygame.quit()
            quit()
