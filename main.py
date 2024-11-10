import pygame
pygame.init()

from scenes.menu import Menu

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Cretan Nightmare')

clock = pygame.time.Clock()
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
    
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()