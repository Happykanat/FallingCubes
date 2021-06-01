import pygame as pg


class Button():
    def __init__(self, x, y, path: str):
        self.image = pg.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def blit(self, display_surface):
        display_surface.blit(self.image, self.rect)

    def pressed(self, mx, my):
        if self.rect.collidepoint(mx, my):
            return True
        else:
            return False
