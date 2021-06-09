import sys
import random
import pygame as pg
from pygame.event import Event

from hero import Hero
from button import Button


# инициализация модулей pg
pg.init()

# цвета
city = (230,250,255)
reef = (0,100,100)
forest = (50, 125, 0)
mushroom_forest = (50,10,50)
red = (255, 0, 0)
dark_blue = (0, 13, 119)
background_colour = forest
pause_bg_color = (0, 0, 0)
transparency = 200

# создание окна
WIDTH = 500
HEIGHT = 700
DISPLAYSURF = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Falling Cubes')

# FPS
fps = 30
fpsclock = pg.time.Clock()

# создание героя
hero = Hero()
cooldown_time = 10  # sec
frame_counter = cooldown_time * fps

# создание врагов
enemy_speed_step = 12
enemy_time = 10  # секунды
enemy_step = 1
max_enemy_speed = 20
enemies_rects = []
enemy_pic = pg.image.load('Images/enemy cube.png')
step_x = int(1.25 * hero.rect.width)
for _ in range(10):
    enemy_rect = enemy_pic.get_rect().copy()
    enemy_rect.x = random.randrange(0, WIDTH, step_x)
    enemy_rect.y = random.randrange(-HEIGHT, -enemy_rect.height, enemy_rect.height)
    enemies_rects.append(enemy_rect)

# Пауза
paused = False
pause_text = pg.image.load('Images/Letters/Paused.png')
pause_path = 'Images/button 400x150.png'

# счёт
score = 0
score_color = red

# кнопки

# шрифты
score_msg = pg.font.SysFont('comicsansms', 50)

# Музыка
pg.mixer.music.load('music/menu.wav')
pg.mixer.music.play(-1)

# циклы
running = True
opening_menu = True

# смена локации
CHANGE_LOCATION = pg.USEREVENT + 1
pg.time.set_timer(CHANGE_LOCATION, 5000)

# меню
while opening_menu:
    for event in pg.event.get():

        # выход
        if event.type == pg.QUIT:
            opening_menu = False
            running = False
            break

        if event.type == CHANGE_LOCATION:
            background_colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    # отрисовка
    DISPLAYSURF.fill(background_colour)

    # обновление экрана
    pg.display.update()

    # выдержка FPS
    fpsclock.tick(fps)

# Музыка
pg.mixer.music.load('music/locations_songs/forest.wav')
pg.mixer.music.play(-1)

# Игровой цикл
while running:

    # счетчик кадров
    frame_counter += 1
    seconds_passed = frame_counter / fps

    # todo
    cooldown_left = cooldown_time - seconds_passed
    if cooldown_left <= 0:
        cooldown_text = f'ready!'
    else:
        cooldown_text = f'{cooldown_left:.0f} sec'

    # обработка изменения счёта
    for enemy_rect in enemies_rects:
        if enemy_rect.top >= hero.rect.bottom:
            if enemy_rect.top <= hero.rect.bottom + enemy_speed_step:
                score += 1
            # a = a + 1 ~ a += 1

    # обработка движения главного героя
    key = pg.key.get_pressed()
    if key[pg.K_a]: hero.move_left()
    if key[pg.K_d]: hero.move_right()

    # логика падающих кубиков
    for enemy_rect in enemies_rects:
        if enemy_rect.top <= HEIGHT:
            enemy_rect.y += enemy_speed_step
        else:
            enemy_rect.x = random.randrange(0, WIDTH, step_x)
            enemy_rect.y = random.randrange(-HEIGHT, -enemy_rect.height, enemy_rect.height)

    # увеличение скорости врагов и героя
    if enemy_speed_step < max_enemy_speed:
        if seconds_passed % enemy_time == 0:
            enemy_speed_step += enemy_step
            hero.step += 0.8

    # обработка столкновения топора/героя с врагами
    collided = False
    for enemy_rect in enemies_rects:
        if hero.axe_rect.colliderect(enemy_rect):
            enemy_rect.x = random.randrange(0, WIDTH, step_x)
            enemy_rect.y = random.randrange(-HEIGHT, -enemy_rect.height, enemy_rect.height)
            score += 5
        if hero.rect.colliderect(enemy_rect):
            collided = True
            break
    if collided:
        background_colour = red
    else:
        background_colour = forest

    # обработка событий
    event: Event
    for event in pg.event.get():
        # выход
        if event.type == pg.QUIT:
            running = False
            break

        if event.type == pg.KEYDOWN:

            # бросок топора
            if event.key == pg.K_SPACE:
                if seconds_passed >= cooldown_time:
                    hero.throw_axe()
                    frame_counter = 0

            # pause
            if event.key == pg.K_ESCAPE:
                paused = True
                break

    if paused:

        pause_background = pg.Surface((WIDTH, HEIGHT))
        pause_background.fill(pause_bg_color)
        pause_background.set_alpha(transparency)

        pg.mixer.music.pause()

        # text...

        continue_game = Button(0.5 * WIDTH - 200, 0.5 * HEIGHT, pause_path)

        DISPLAYSURF.blit(pause_background, (0, 0))
        DISPLAYSURF.blit(pause_text, (0.5 * WIDTH - 150, 0.2 * HEIGHT))
        continue_game.blit(DISPLAYSURF)

        pg.display.update()

        while paused:

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    # todo при таком подходе после выхода из паузы произойдёт ещё 1 итерация отрисовки
                    paused = False
                    running = False
                    break

                if event.type == pg.MOUSEBUTTONUP:
                    mx, my = event.pos
                    if continue_game.pressed(mx, my):
                        paused = False
                        pg.mixer.music.unpause()
                        break

    # Рендер текста
    score_surf = score_msg.render(f'{score}', True, score_color)

    # отрисовка
    DISPLAYSURF.fill(background_colour)
    hero.blit_me(DISPLAYSURF)
    for enemy_rect in enemies_rects:
        DISPLAYSURF.blit(enemy_pic, enemy_rect)
    DISPLAYSURF.blit(score_surf, (30, 30))  # todo убрать координаты в переменную

    # обновление экрана
    pg.display.update()

    # выдержка FPS
    fpsclock.tick(fps)

pg.quit()
