import pygame as pg
import random

class Enemy:
    def __init__(self, surface, speed, step_x=100, HEIGHT=700, WIDTH=500, step_speed=12, max_speed=20, speed_cooldown=10):
        self.speed = speed
        self.surface = surface
        self.image = pg.image.load('Images/enemy cube.png')
        self.rect = self.image.get_rect()
        self.HEIGHT = HEIGHT
        self.step_x = step_x
        self.step_y = self.rect.height
        self.step_speed = step_speed
        self.max_speed = max_speed
        self.DISPLAY_WIDTH = WIDTH
        self.speed_cooldown = speed_cooldown

    def set_start_pos(self):
        self.rect.x = random.randrange(0, self.DISPLAY_WIDTH, self.step_x)
        self.rect.y = random.randrange(-self.HEIGHT,-self.rect.height, self.step_y)
        # TODO Учесть наложение кубиков

    def move(self):
        if self.rect.top <= self.HEIGHT:
            self.rect.y += self.speed
        else:
            self.set_start_pos()

    def blit(self):
        self.surface.blit(self.image, self.rect)

    def collided_hero(self, hero):
        if hero.rect.colliderect(self.rect):
            return True
        else:
            return False

    def collided_hero_weapon(self, hero):
        if hero.axe_rect.colliderect(self.rect):
            self.set_start_pos()
            return True
        else:
            return False
