import pygame as pg

class Axe():
    def __init__(self, throw_speed = 12, sound = 'music/axe_throwing.wav', cooldown = 10, ):
        self.throwing = False
        self.axe_index = 0
        self.axe_images = []
        self.throw_speed = throw_speed
        self.sound = pg.mixer.Sound(sound)
        self.current_time = pg.time.get_ticks()
        self.basic_time = 0
        for i in range(8):
            self.axe_images.append(pg.image.load(f'Images/axe{i}.png'))
        self.rect = self.axe_images[0].get_rect()


    def use(self, xs, ys):
        self.current_time = pg.time.get_ticks()
        if self.current_time - 1000 >= self.basic_time:
            self.basic_time = pg.time.get_ticks()

            self.sound.play()
            self.throwing = True
            self.rect.x = xs
            self.rect.y = ys

    def blit(self, surface):
        if self.throwing == True:
            surface.blit(self.axe_images[self.axe_index], self.rect)
            if self.rect.y >= -1000:
                self.rect.y -= 12
                self.axe_index += 1
                if self.axe_index > 7:
                    self.axe_index = 0
            else:
                self.throwing = False
    # Логика топора
    '''self.axe_images = []
    self.axe_sound = pygame.mixer.Sound('music/axe_throwing.wav')
    for axe_num in range(8):
        self.axe_images.append(pygame.image.load(f'Images/axe{axe_num}.png'))

    self.axe_rect = self.axe_images[0].get_rect()

    self.throwing = False
    self.axe_index = 0

    if self.throwing == True:
        if self.axe_rect.y >= -1000:
            self.axe_rect.y -= 12
            display_surface.blit(self.axe_images[self.axe_index], self.axe_rect)
            self.axe_index += 1
            if self.axe_index > 7:
                self.axe_index = 0
        else:
            self.throwing = False'''

    '''def throw_axe(self):
            self.throwing = True
            self.axe_rect.x = self.rect.x
            self.axe_rect.y = self.rect.y
            self.axe_sound.play()'''