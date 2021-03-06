import sys
import random
import pygame as pg
from pygame.event import Event

from hero import Hero
from enemies.enemies import Enemies
from button import Button
from abilities.axe import Axe


# инициализация модулей pg
pg.init()

# цвета
red = (255, 0, 0)
dark_blue = (0, 13, 119)
pause_bg_color = (0, 0, 0)
transparency = 200

# локации
city = pg.image.load('Images/city_background.png')
reef = pg.image.load('Images/reef_background.png')
forest = pg.image.load('Images/forest_background.png')
mushroom_forest = pg.image.load('Images/mushroom_forest_background.png')
locations = [forest, mushroom_forest, city, reef]
end_loc = len(locations)
background_colour = forest
menu_loc = 0

# создание окна
WIDTH = 500
HEIGHT = 700
DISPLAYSURF = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Falling Cubes')

# FPS
fps = 30
fpsclock = pg.time.Clock()

# создание героя
ability = Axe()
cube_skin = "Images/AXE CUBE 70x70.png"
axe_cube = Hero(ability, cube_skin)
mushroom_cube = Hero(ability, cube_skin)
city_cube = Hero(ability, cube_skin)
cooldown_time = 10  # sec
frame_counter = cooldown_time * fps

# создание врагов
enemies_description = [
    ['reef', 5],
    ['common', 5],
]


enemies = Enemies(enemies_description)

# enemy_speed_step = 12
# enemy_time = 10  # секунды
# enemy_step = 1
# max_enemy_speed= 20
# enemies_rects = []
# enemy_pic = pg.image.load('Images/enemy cube.png')
# step_x = int(1.25 * axe_cube.rect.width)
# for _ in range(10):
#     enemy_rect = enemy_pic.get_rect().copy()
#     enemy_rect.x = random.randrange(0, WIDTH, step_x)
#     enemy_rect.y = random.randrange(-HEIGHT, -enemy_rect.height, enemy_rect.height)
#     enemies_rects.append(enemy_rect)

# Пауза
paused = False
pause_text = pg.image.load('Images/Letters/Paused.png')
pause_path = 'Images/button 400x150.png'

# счёт
score = 0
score_color = red

# кнопки
start_button = Button(200,300,'Images/start_button 50X50.png')
exit_button = Button(100,200,'Images/exit.png')

# шрифты
score_msg = pg.font.SysFont('comicsansms', 50)

# Музыка
pg.mixer.music.load('music/menu.wav')
pg.mixer.music.play(-1)

# циклы
running = True
opening_menu = True
game_over = False

# смена локации
CHANGE_LOCATION = pg.USEREVENT + 1
pg.time.set_timer(CHANGE_LOCATION, 1000)

# меню
while opening_menu:
    for event in pg.event.get():

        # выход
        if event.type == pg.QUIT:
            opening_menu = False
            running = False
            break

        # старт по кнопке
        if event.type == pg.MOUSEBUTTONUP:
            mx, my = event.pos
            if start_button.pressed(mx, my):
                opening_menu = False

        # рандомные цвета
        if event.type == CHANGE_LOCATION:
            if menu_loc < end_loc:
                background_colour = locations[menu_loc]
                menu_loc += 1
            else:
                menu_loc = 0

    # отрисовка
    DISPLAYSURF.blit(background_colour,(0,0))
    start_button.blit(DISPLAYSURF)

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

    # # обработка изменения счёта
    # for enemy_rect in enemies_rects:
    #     if enemy_rect.top >= axe_cube.rect.bottom:
    #         if enemy_rect.top <= axe_cube.rect.bottom + enemy_speed_step:
    #             score += 1

    # обработка движения главного героя
    key = pg.key.get_pressed()
    if key[pg.K_a]: axe_cube.move_left()
    if key[pg.K_d]: axe_cube.move_right()

    enemies.move()

    # # логика падающих кубиков
    # for enemy_rect in enemies_rects:
    #     if enemy_rect.top <= HEIGHT:
    #         enemy_rect.y += enemy_speed_step
    #     else:
    #         enemy_rect.x = random.randrange(0, WIDTH, step_x)
    #         enemy_rect.y = random.randrange(-HEIGHT, -enemy_rect.height, enemy_rect.height)
    #
    # # увеличение скорости врагов и героя
    # if enemy_speed_step < max_enemy_speed:
    #     if seconds_passed % enemy_time == 0:
    #         enemy_speed_step += enemy_step
    #         axe_cube.step += 0.8

    # обработка событий
    for event in pg.event.get():
        # выход
        if event.type == pg.QUIT:
            running = False
            break

        if event.type == pg.KEYDOWN:

            # бросок топора
            if event.key == pg.K_SPACE:
                axe_cube.ability_use()

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
    DISPLAYSURF.blit(background_colour,(0,0))
    axe_cube.blit_me(DISPLAYSURF)
    enemies.blit_enemies(DISPLAYSURF)
    # for enemy_rect in enemies_rects:
    #     DISPLAYSURF.blit(enemy_pic, enemy_rect)
    DISPLAYSURF.blit(score_surf, (30, 30))  # todo убрать координаты в переменную

    # обновление экрана
    pg.display.update()

    # выдержка FPS
    fpsclock.tick(fps)

pg.mixer.music.stop()

while game_over:
    for event in pg.event.get():

        if event.type == pg.MOUSEBUTTONUP:
            mx, my = event.pos
            if exit_button.pressed(mx, my):
                game_over = False
                break
    exit_button.blit(DISPLAYSURF)

    # обновление экрана
    pg.display.update()

    # выдержка FPS
    fpsclock.tick(fps)

pg.quit()
