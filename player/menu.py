import pygame
import settings as st
from image_button import ImageButton

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()

        self.bg = pygame.image.load(st.MENU_BG).convert()
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))

        self.start = ImageButton(screen, 0.5, 0.5, "images/ui/play.bmp", 2.5)

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.start.draw(self.screen)

    def handle_click(self, event):
        if self.start.is_clicked(event):
            return "start"
        return None