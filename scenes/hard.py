import pygame
from map import Map
from enemy import Enemy  # Mengimpor kelas Enemy dari file enemy.py

class Hard:
    def __init__(self):
        self.cell_size = 50  # Ukuran setiap sel dalam piksel
        self.cols, self.rows = 16, 12  # Ukuran grid (16x12)
        self.map = Map(self.cols, self.rows, self.cell_size)  # Inisialisasi Map
        self.enemy = Enemy(self.cols - 1, self.rows - 1)  # Musuh di pojok kanan bawah

        # Flag untuk menentukan apakah peta selesai dibuat
        self.map_generated = False

    def handle_event(self, event):
        # Meneruskan event ke Map dan Enemy
        self.map.handle_input(event)

    def update(self):
        # Generate labirin jika belum selesai
        if not self.map_generated:
            self.map.generate()
            self.map_generated = all(cell.visited for cell in self.map.grid_cells)

        # Update posisi musuh
        player_position = (self.map.player.x, self.map.player.y)  # Posisi pemain
        self.enemy.update(player_position, self.map.grid_cells, self.cols, self.rows)

    def render(self, screen):
        # Mengisi layar dengan warna dasar
        screen.fill(pygame.Color('darkslategray'))

        # Render labirin, pemain, hint, dan musuh
        self.map.render(screen)
        self.enemy.draw(screen, self.cell_size)
