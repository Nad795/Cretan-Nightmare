import pygame

PINK = (255, 204, 234)
BLUE = (191, 236, 255)
YELLOW = (255, 187, 70)
WHITE = (250, 250, 250)
BLACK = (5, 5, 5)
NAVY = (0, 54, 119)
GOLD = (255, 165, 0)

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

def draw_button(text, x, y, width, height, screen, font, color=YELLOW, border_color=BLACK, border_thickness=2):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = button_hover(mouse_pos, x, y, width, height)

    if is_hovered:
        scale_factor = 1.05
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        new_x = x - (new_width - width) // 2
        new_y = y - (new_height - height) // 2
        color = GOLD
        new_font_size = int(font.get_height() * scale_factor)  
        font = create_font(new_font_size)  
    else:
        new_width, new_height, new_x, new_y = width, height, x, y
        font_size = font.get_height()
        font = create_font(font_size)

    pygame.draw.rect(screen, color, (new_x, new_y, new_width, new_height))
    pygame.draw.rect(screen, border_color, (new_x, new_y, new_width, new_height), border_thickness)

    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(new_x + new_width // 2, new_y + new_height // 2))
    screen.blit(text_surface, text_rect)

def button_hover(mouse_pos, x, y, width, height):
    return x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y

def create_font(size=40):
    return pygame.font.Font(None, size)

def draw_panel(screen, x, y, width, height, color=BLUE):
    pygame.draw.rect(screen, color, (x, y, width, height))
