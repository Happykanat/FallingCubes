import pygame as pg
import random
from enemies.enemy import Enemy


class Enemies:
    def __init__(self, description, HEIGHT = 700, WIDTH = 500, hero_width = 70):
        self.enemies = []
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.hero_width = hero_width
        self.step_x = int(1.25 * self.hero_width)
        self.com_num = description[1][1]
        self.com_enemy = description[1][0]
        self.loc_num = description[0][1]
        self.loc_enemy = description[0][0]

        for i in range(self.loc_num):
            enemy = Enemy(self.loc_enemy, 12)
            self.enemies.append(enemy)

        for i in range(self.com_num):
            enemy = Enemy(self.com_enemy, 12)
            self.enemies.append(enemy)

        for enemy in self.enemies:
            enemy.set_start_pos()

    def blit_enemies(self, surface):
        for i in range(len(self.enemies)):
            surface.blit(self.enemies[i].image, self.enemies[i].rect)

    def blit_abilities(self, surface):
        pass

    def use_abilities(self):
        pass

    def move(self):
        for i in range(len(self.enemies)):
            self.enemies[i].move()

    def up(self):
        pass

    def collided_hero(self, hero):
        pass

    def collided_weapon(self, hero):
        pass

    def change_speed(self):
        pass

    def score(self, hero):
        pass