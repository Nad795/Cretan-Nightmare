import pygame
import sys
from map import Map
from enemy import Enemy
from scenes.game_over import GameOver

class Hard:
    def __init__(self):
        self.cell_size = 50
        self.cols, self.rows = 16, 12
        self.map = Map(self.cols, self.rows, self.cell_size)
        self.enemy = Enemy(0, 0)
        self.map_generated = False
        self.enemy_start_time = 0
        self.game_over = False
        self.game_over_timer = 0

    def handle_event(self, event):
        self.map.handle_input(event)

    def update(self, dt):
        if self.game_over:
            self.game_over_timer += dt
            if self.game_over_timer >= 10:
                pygame.quit()
                sys.exit()
            return

        if not self.map_generated:
            self.map.generate()
            self.map_generated = all(cell.visited for cell in self.map.grid_cells)

        self.enemy_start_time += dt
        if self.enemy_start_time > 3000:
            player_position = (self.map.player.x, self.map.player.y)
            self.enemy.update(player_position, self.map.grid_cells, self.cols, self.rows, dt)

            if self.map.player.x == self.enemy.x and self.map.player.y == self.enemy.y:
                print("GAME OVER")
                self.game_over = True

    def render(self, screen):
        screen.fill(pygame.Color('darkslategray'))
        self.map.render(screen)
        if self.enemy_start_time > 3000:
            self.enemy.draw(screen, self.cell_size)
