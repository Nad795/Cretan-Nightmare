import pygame
from map import Map
from player import Player
import time

class Medium:
    def __init__(self):
        self.map = Map(40, 40)
        self.cell_size = 20
        self.player = Player((0, 0), self.cell_size, self.map)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player.move(0, -1)
            elif event.key == pygame.K_DOWN:
                self.player.move(0, 1)
            elif event.key == pygame.K_LEFT:
                self.player.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.player.move(1, 0)

    def update(self):
        if self.show_hint and time.time() - self.hint.last_collected_time > self.hint.cooldown:
            self.show_hint = False
    
    def render(self, screen):
        self.map.render(screen, self.cell_size)
        self.player.render(screen)
        self.hint.render(screen, self.cell_size)
        
        if self.show_hint:
            self.hint.render_hint_path(screen, self.cell_size)
