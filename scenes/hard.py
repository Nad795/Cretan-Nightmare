import pygame
from map import Map
from enemy import Enemy
from player import Player
from scenes.game_over import GameOver

class Hard:
    def __init__(self):
        self.cell_size = 50  # Ukuran setiap sel dalam piksel
        self.cols, self.rows = 16, 12  # Ukuran grid (16x12)
        self.map = Map(self.cols, self.rows, self.cell_size)  # Inisialisasi Map
        self.enemy = Enemy(0, 0)  # Musuh di pojok kanan bawah

        # Flag untuk menentukan apakah peta selesai dibuat
        self.map_generated = False
        self.enemy_start_time = 0

    def handle_event(self, event):
        # Meneruskan event ke Map dan Enemy
        self.map.handle_input(event)

    def update(self, dt):
        # Generate labirin jika belum selesai
        if not self.map_generated:
            self.map.generate()
            self.map_generated = all(cell.visited for cell in self.map.grid_cells)

        # Update posisi musuh
        self.enemy_start_time += dt
        if self.enemy_start_time > 3000:  # Enemy starts moving after 15 seconds
            player_position = (self.map.player.x, self.map.player.y)  # Player's position
            self.enemy.update(player_position, self.map.grid_cells, self.cols, self.rows, dt)
            if self.player.x == self.enemy.x and self.player.y == self.enemy.y:
                print("GAME OVER")
                return GameOver()

    def render(self, screen):
        # Mengisi layar dengan warna dasar
        screen.fill(pygame.Color('darkslategray'))

        # Render labirin, pemain, hint, dan musuh
        self.map.render(screen)
        if self.enemy_start_time > 3000:
            self.enemy.draw(screen, self.cell_size)
