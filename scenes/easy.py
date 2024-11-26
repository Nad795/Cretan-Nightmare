import pygame
from map import Map

class Easy:
    def __init__(self):
        self.map = Map(30, 40)
        self.cell_size = 20
        
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def render(self, screen):
        self.map.render(screen, self.cell_size)