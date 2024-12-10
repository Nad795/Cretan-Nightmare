import pygame
import sys
from scenes.menu import Menu
import ui
from pygame import mixer

pygame.init()

screen = ui.initialize_screen(800, 600, 'The Deadliners')

icon = pygame.image.load('assets/logo-icon.png') 
pygame.display.set_icon(icon)

clock = ui.create_clock()
FPS = 60

mixer.music.load("assets/bg-music.mp3")
mixer.music.play(-1)

current_scene = Menu()

running = True
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            next_scene = current_scene.handle_event(event)
            if next_scene:
                current_scene = next_scene

    current_scene.update(dt)
    current_scene.render(screen)
    
    ui.update_display()
    
    ui.set_fps(clock, FPS)
    
pygame.quit()