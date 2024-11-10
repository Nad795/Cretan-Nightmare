import pygame
import sys
from scenes.easy import Easy
from scenes.medium import Medium
from scenes.hard import Hard

PINK = (255, 204, 234)
BLUE = (191, 236, 255)
YELLOW = (255, 246, 227)

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 40)
        self.show_panel = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.show_panel:
                if self.button_hover(mouse_pos, 250, 250, 300, 50):
                    print('Easy selected')
                    return Easy()
                if self.button_hover(mouse_pos, 250, 325, 300, 50):
                    print('Medium selected')
                    return Medium()
                if self.button_hover(mouse_pos, 250, 400, 300, 50):
                    print('Hard selected')
                    return Hard()
            else:
                if self.button_hover(mouse_pos, 300, 200, 200, 50):
                    self.show_panel = True
                if self.button_hover(mouse_pos, 300, 300, 200, 50):
                    pygame.quit()
                    sys.exit()
                    
        return None
    
    def update(self):
        pass
    
    def button_hover(self, mouse_pos, x, y, width, height):
        return x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y
    
    def render(self, screen):
        screen.fill(PINK)
        
        if self.show_panel:
            pygame.draw.rect(screen, BLUE, (250, 150, 300, 300))
            
            self.draw_button('Easy', 250, 250, 300, 50, screen)
            self.draw_button('Medium', 250, 325, 300, 50, screen)
            self.draw_button('Hard', 250, 400, 300, 50, screen)
        else:
            self.draw_button('Play', 300, 200, 200, 50, screen)
            self.draw_button('Quit', 300, 300, 200, 50, screen)
            
    def draw_button(self, text, x, y, width, height, screen):
        pygame.draw.rect(screen, YELLOW, (x, y, width, height))
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center = (x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)