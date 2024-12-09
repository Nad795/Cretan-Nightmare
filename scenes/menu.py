import pygame
import sys
from scenes.easy import Easy
from scenes.hard import Hard
import ui

class Menu:
    def __init__(self):
        self.font = ui.create_font()
        self.show_panel = False
        self.logo = pygame.image.load('assets/big-logo.png')  # Load gambar logo
        self.logo = pygame.transform.scale(self.logo, (500, 187))  # Ubah ukuran logo sesuai kebutuhan
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.show_panel:
                # Update koordinat untuk tombol "Easy", "Hard", dan "Back"
                if ui.button_hover(mouse_pos, 250, 255, 300, 50):  # Tombol "Easy"
                    print('Easy selected')
                    return Easy()
                if ui.button_hover(mouse_pos, 250, 325, 300, 50):  # Tombol "Hard"
                    print('Hard selected')
                    return Hard()
                if ui.button_hover(mouse_pos, 670, 20, 100, 50):  # Koordinat baru untuk tombol "Back"
                    print('Back selected')
                    self.show_panel = False
            else:
                if ui.button_hover(mouse_pos, 300, 330, 200, 50):
                    self.show_panel = True
                if ui.button_hover(mouse_pos, 300, 400, 200, 50):
                    pygame.quit()
                    sys.exit()
                    
        return None
    
    def update(self, dt):
        pass
    
    def render(self, screen):
        screen.fill(ui.NAVY)
        
        if self.show_panel:
            # Tambahkan teks "Choose Your Level" agar lebih berada di tengah
            text = self.font.render('Choose Your Level', True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 215))  # Posisi teks di tengah secara horizontal
            
            screen.blit(text, text_rect)  # Blit teks ke layar dengan posisi tengah
           
            # Update koordinat tombol-tombol
            ui.draw_button('Easy', 250, 255, 300, 50, screen, self.font)
            ui.draw_button('Hard', 250, 325, 300, 50, screen, self.font)
            ui.draw_button('Back', 670, 20, 100, 50, screen, self.font)  # Posisi baru untuk tombol "Back"
        else:
            # Ubah posisi logo agar berada di tengah layar secara horizontal
            logo_x = (800 - 500) // 2  # 800 adalah lebar layar, 600 adalah lebar logo
            screen.blit(self.logo, (logo_x, 100))  # Menampilkan logo di tengah
            
            ui.draw_button('Play', 300, 330, 200, 50, screen, self.font)
            ui.draw_button('Quit', 300, 400, 200, 50, screen, self.font)
