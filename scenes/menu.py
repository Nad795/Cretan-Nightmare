import pygame
import sys
from scenes.easy import Easy
from scenes.hard import Hard
import ui

class Menu:
    def __init__(self):
        self.font = ui.create_font()
        self.show_panel = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.show_panel:
                if ui.button_hover(mouse_pos, 250, 175, 300, 50):
                    print('Easy selected')
                    return Easy()
                if ui.button_hover(mouse_pos, 250, 325, 300, 50):
                    print('Hard selected')
                    return Hard()
            else:
                if ui.button_hover(mouse_pos, 300, 200, 200, 50):
                    self.show_panel = True
                if ui.button_hover(mouse_pos, 300, 300, 200, 50):
                    pygame.quit()
                    sys.exit()
                    
        return None
    
    def update(self, dt):
        pass
    
    def render(self, screen):
        screen.fill(ui.PINK)
        
        if self.show_panel:
            ui.draw_button('Easy', 250, 175, 300, 50, screen, self.font)
            ui.draw_button('Hard', 250, 325, 300, 50, screen, self.font)
        else:
            ui.draw_button('Play', 300, 200, 200, 50, screen, self.font)
            ui.draw_button('Quit', 300, 300, 200, 50, screen, self.font)
