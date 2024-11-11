import pygame
import sys
from scenes.menu import Menu
import ui

pygame.init()

screen = ui.initialize_screen(800, 600, 'Cretan Nightmare')

clock = ui.create_clock()
FPS = 60

current_scene = Menu()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            next_scene = current_scene.handle_event(event)
            if next_scene:
                current_scene = next_scene

    current_scene.update()
    current_scene.render(screen)
    
    ui.update_display()
    
    ui.set_fps(clock, FPS)
    
pygame.quit()