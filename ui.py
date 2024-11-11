import pygame

PINK = (255, 204, 234)
BLUE = (191, 236, 255)
YELLOW = (255, 246, 227)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def initialize_screen(width, height, title):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    return screen

def update_display():
    pygame.display.flip()

def create_clock():
    return pygame.time.Clock()

def set_fps(clock, fps):
    clock.tick(fps)

def draw_button(text, x, y, width, height, screen, font, color=YELLOW):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def button_hover(mouse_pos, x, y, width, height):
    return x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y

def create_font(size = 40):
    return pygame.font.Font(None, size)

def draw_panel(screen, x, y, width, height, color = BLUE):
    pygame.draw.rect(screen, color, (x, y, width, height))