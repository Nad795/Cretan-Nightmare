import pygame
from map import Map

class Easy:
    def __init__(self):
        self.cell_size = 50  # Ukuran setiap sel dalam piksel
        self.cols, self.rows = 16, 12  # Ukuran grid (16x12)
        self.map = Map(self.cols, self.rows, self.cell_size)  # Inisialisasi Map

        # Flag untuk menentukan apakah peta selesai dibuat
        self.map_generated = False

    def handle_event(self, event):
        # Meneruskan event ke Map
        self.map.handle_input(event)

    def update(self, dt):
        # Generate labirin jika belum selesai
        if not self.map_generated:
            self.map.generate()
            self.map_generated = all(cell.visited for cell in self.map.grid_cells)

    def render(self, screen):
        # Mengisi layar dengan warna dasar
        screen.fill(pygame.Color('darkslategray'))

        # Render labirin, pemain, dan hint
        self.map.render(screen)