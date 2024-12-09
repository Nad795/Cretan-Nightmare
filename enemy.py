import pygame
import heapq

# Node untuk algoritma A*
class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = float('inf')  # Cost from start to this node
        self.h = float('inf')  # Heuristic from this node to the goal
        self.f = float('inf')  # Total cost (f = g + h)

    def __lt__(self, other):
        return self.f < other.f  # Compare based on f value (for priority queue)

# Algoritma A* untuk mencari jalur
def a_star(start, goal, grid_cells, cols, rows):
    open_list = []
    closed_list = set()
    start_node = Node(start[0], start[1])
    start_node.g = 0
    start_node.h = abs(goal[0] - start[0]) + abs(goal[1] - start[1])
    start_node.f = start_node.g + start_node.h
    heapq.heappush(open_list, start_node)
    
    while open_list:
        current_node = heapq.heappop(open_list)
        
        if (current_node.x, current_node.y) == goal:
            path = []
            while current_node.parent:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            path.reverse()
            return path
        
        closed_list.add((current_node.x, current_node.y))
        
        neighbors = [
            (current_node.x, current_node.y - 1, 'top'),    # up
            (current_node.x + 1, current_node.y, 'right'), # right
            (current_node.x, current_node.y + 1, 'bottom'), # down
            (current_node.x - 1, current_node.y, 'left')   # left
        ]
        
        for nx, ny, direction in neighbors:
            if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in closed_list:
                # Check wall constraints
                cell = grid_cells[current_node.x + current_node.y * cols]
                next_cell = grid_cells[nx + ny * cols]
                if cell.walls[direction] or not next_cell:
                    continue
                
                neighbor_node = Node(nx, ny, current_node)
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = abs(goal[0] - nx) + abs(goal[1] - ny)
                neighbor_node.f = neighbor_node.g + neighbor_node.h
                heapq.heappush(open_list, neighbor_node)
                    
    return []  # Return an empty path if no path exists

# Kelas untuk Enemy
class Enemy:
    def __init__(self, x, y, tile_size, image_path='assets/enemy-icon.png'):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.image = pygame.image.load(image_path).convert_alpha()
        
        # Mengatur ukuran gambar agar lebih kecil dari ukuran tile (misalnya 70% dari tile_size)
        scale_factor = 0.7
        new_width = int(tile_size * scale_factor)
        new_height = int(tile_size * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.move_timer = 0  # Timer untuk pergerakan
        self.path = []  # Jalur yang akan dilalui musuh

    def update(self, player_position, grid_cells, cols, rows, dt):
        # Increment move timer
        self.move_timer += dt
        if self.move_timer < 85:  # Move only every 500 milliseconds
            return

        self.move_timer = 0  # Reset timer
        
        if not self.path or (self.x, self.y) == self.path[0]:
            # Hitung jalur baru jika tidak ada atau target saat ini sudah tercapai
            self.path = a_star((self.x, self.y), player_position, grid_cells, cols, rows)
        
        if self.path:
            next_tile = self.path.pop(0)
            self.x, self.y = next_tile

    def draw(self, screen, tile_size):
        # Hitung posisi agar ikon berada di tengah tile
        rect = self.image.get_rect()
        rect.topleft = (self.x * tile_size + (tile_size - rect.width) // 2,
                        self.y * tile_size + (tile_size - rect.height) // 2)
        screen.blit(self.image, rect.topleft)
