import pygame


class Hero():
    def __init__(self, ability, cube_skin, x=150, y=530, step=12, WIDTH=500, ):
        self.hero_image = pygame.image.load(cube_skin)
        self.ability = ability
        self.WIDTH = WIDTH
        self.rect = self.hero_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.step = step

    def ability_use(self):
        self.ability.use(self.rect.centerx, self.rect.centery)

    def blit_me(self, display_surface):
        display_surface.blit(self.hero_image, self.rect)

        self.ability.blit(display_surface)

    def change_step(self, value):
        self.step += value

    def move_left(self):
        self.rect.x -= self.step
        if self.rect.left <= 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.step
        if self.rect.right >= self.WIDTH:
            self.rect.right = self.WIDTH

if __name__ == '__main__':
    hero = Hero(150)
