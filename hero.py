import pygame


class Hero():
    def __init__(self, hero_x=150, hero_y=610, step=12, WIDTH=500):
        self.hero_image = pygame.image.load("Images/AXE CUBE 70x70.png")
        self.WIDTH = WIDTH
        self.rect = self.hero_image.get_rect()
        self.rect.x = hero_x
        self.rect.y = hero_y
        self.step = step

        # Логика топора
        self.axe_images = []
        self.axe_sound = pygame.mixer.Sound('music/axe_throwing.wav')
        for axe_num in range(8):
            self.axe_images.append(pygame.image.load(f'Images/axe{axe_num}.png'))

        self.axe_rect = self.axe_images[0].get_rect()

        self.throwing = False
        self.axe_index = 0

    def blit_me(self, display_surface):
        display_surface.blit(self.hero_image, self.rect)

        if self.throwing == True:
            if self.axe_rect.y >= -1000:
                self.axe_rect.y -= 12
                display_surface.blit(self.axe_images[self.axe_index], self.axe_rect)
                self.axe_index += 1
                if self.axe_index > 7:
                    self.axe_index = 0
            else:
                self.throwing = False

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

    def throw_axe(self):
        self.throwing = True
        self.axe_rect.x = self.rect.x
        self.axe_rect.y = self.rect.y
        self.axe_sound.play()


if __name__ == '__main__':
    hero = Hero(150)
