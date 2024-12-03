# generate map pake DFS
import pygame
from random import choice, randrange
from player import Player 
from hint import Hint

RES = WIDTH, HEIGHT = 800, 600
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

hint_timer = 0
hint_active_duration = 5000 

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        
    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))
        
    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))
            
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x, y), 2)
            
    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]
    
    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    
def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []

player = Player(0,0,TILE)
exit_x, exit_y = randrange(cols), randrange(rows)

while exit_x == 0 and exit_y == 0:  # Ensure exit isn't the starting position
    exit_x, exit_y = randrange(cols), randrange(rows)

hint_x, hint_y = randrange(cols), randrange(rows)
while (hint_x, hint_y) in [(0, 0), (exit_x, exit_y)]:  # Exclude player start and exit
    hint_x, hint_y = randrange(cols), randrange(rows)
hint = Hint(hint_x, hint_y, TILE)

while True:
    sc.fill(pygame.Color('darkslategray'))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move("UP", grid_cells, cols)
            elif event.key == pygame.K_RIGHT:
                player.move("RIGHT", grid_cells, cols)
            elif event.key == pygame.K_DOWN:
                player.move("DOWN", grid_cells, cols)
            elif event.key == pygame.K_LEFT:
                player.move("LEFT", grid_cells, cols)
            
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()

    pygame.draw.rect(sc, pygame.Color('green'), (exit_x * TILE + TILE // 4, exit_y * TILE + TILE // 4, TILE // 2, TILE // 2))

    # Draw hint item (drawn before player to ensure player is on top)
    hint.draw(sc)
    if hint.active:
        for hx, hy in hint.path:
            pygame.draw.rect(sc, pygame.Color(0, 255, 255, 128), (hx * TILE + TILE // 4, hy * TILE + TILE // 4, TILE // 2, TILE // 2))

    if player.x == hint_x and player.y == hint_y:
        hint.activate(grid_cells, cols, rows, player.x, player.y, exit_x, exit_y)
        hint_timer = pygame.time.get_ticks()

    # Draw the player last to ensure they are always on top
    player.draw(sc)

    # Check if player reaches the exit
    if player.x == exit_x and player.y == exit_y:
        print("You Win!")
        pygame.time.wait(2000)
        exit()
    
    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()
            
    pygame.display.flip()
    clock.tick(30)