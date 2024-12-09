import pygame

class Player:
    def __init__(self, x, y, tile_size, image_path):
        self.x, self.y = x, y
        self.tile_size = tile_size
        self.image = pygame.image.load(image_path).convert_alpha()
        
        # Mengatur ukuran gambar agar lebih kecil dari ukuran tile (misalnya 90% dari tile_size)
        scale_factor = 0.7
        new_width = int(tile_size * scale_factor)
        new_height = int(tile_size * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def draw(self, screen):
        # Hitung posisi agar ikon berada di tengah tile
        px = self.x * self.tile_size + (self.tile_size - self.image.get_width()) // 2
        py = self.y * self.tile_size + (self.tile_size - self.image.get_height()) // 2
        screen.blit(self.image, (px, py))

    def move(self, direction, grid_cells, cols):
        current_cell = grid_cells[self.x + self.y * cols]

        if direction == "UP" and not current_cell.walls['top']:
            self.y -= 1
        elif direction == "DOWN" and not current_cell.walls['bottom']:
            self.y += 1
        elif direction == "LEFT" and not current_cell.walls['left']:
            self.x -= 1
        elif direction == "RIGHT" and not current_cell.walls['right']:
            self.x += 1
