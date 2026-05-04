import pygame

class ImageButton:
    def __init__(self, screen, x_ratio, y_ratio, image_path, scale):
        self.screen = screen
        self.screen_w, self.screen_h = screen.get_size()

        self.image = pygame.image.load(image_path).convert_alpha()

        w = int(self.image.get_width() * scale)
        h = int(self.image.get_height() * scale)

        self.image = pygame.transform.scale(self.image, (w, h))

        self.rect = self.image.get_rect()
        self.rect.center = (
            int(self.screen_w * x_ratio),
            int(self.screen_h * y_ratio)
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False