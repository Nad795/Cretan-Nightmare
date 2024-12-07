import pygame

class GameOver:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.message = "Game Over!"
        self.color = pygame.Color('red')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from scenes.menu import Menu
                return Menu()  # Return to menu on Enter key

    def update(self, dt):
        pass  # No updates needed for a static game-over screen

    def render(self, screen):
        screen.fill(pygame.Color('black'))
        text_surface = self.font.render(self.message, True, self.color)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text_surface, text_rect)
