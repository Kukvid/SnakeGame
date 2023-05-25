import random
import os
import pygame
import pygame_menu
from pygame_menu import themes

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Устанавливаем приложение по центру экрана

pygame.mixer.pre_init(44100, -16, 1, 512)  # Убирает задержку звуков
pygame.init()  # Инициализируем встроенные в библиотеку модули


def get_screen_size(RECT_COUNT):
    """Функция обновляет размеры экрана согласно настройкам игры"""
    SCREEN_SIZE = [
        RECT_SIZE * RECT_COUNT + 2 * RECT_SIZE + MARGIN * RECT_COUNT,
        RECT_SIZE * RECT_COUNT + 2 * RECT_SIZE + MARGIN * RECT_COUNT + HEADER_MARGIN
    ]
    return SCREEN_SIZE


# Задаем настройки игры

FPS = 15
RECT_SIZE = 30
RECT_COUNT = 15
MENU_RECT_COUNT = 18
MARGIN = 1  # отступ
HEADER_MARGIN = 70
SCREEN_SIZE = get_screen_size(MENU_RECT_COUNT)
GAME_MODE = 0
MUSIC_VOLUME = 0.5
SOUND_VOLUME = 0.5
MAP_ID = 0
SOUND_ID = 5
DIFFICULTY_ID = 1
GAME_MODE = 0

# Загрузка звуков
from sounds import sounds, bomb_explosion, eat_apple, hit_barrier, snake_hiss

# Задаем используемые цвета
HEADER_COLOR = (0, 204, 153)

# создаем начальный экран для меню игры и подпись приложения
pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Snake by Minakov Daniil")

# Создаем объект Clock, который используется для отслеживания кадров в секунду
clock = pygame.time.Clock()

from surfaces import *  # импортируем поверхности с картинками змеи, квадратов, из которых состоит поле, еды
from snake import Snake  # Импортируем класс змейки


def draw_block_inside_map(surf, column, row):
    """Функция отображает объекты на поле змейки"""
    screen.blit(surf, [RECT_SIZE + column * RECT_SIZE + MARGIN * (column + 1),
                       HEADER_MARGIN + RECT_SIZE + row * RECT_SIZE + MARGIN * (row + 1), RECT_SIZE,
                       RECT_SIZE])


def message_to_screen(message, y):
    screen.blit(message, [screen.get_width() // 2 - message.get_width() // 2, y])


def render_snake(snake, game_active):
    """Функция отрисовывает змейку на экран"""
    if game_active:
        for pos_i in range(len(snake.segments)):
            if pos_i == len(snake.segments) - 1:
                draw_block_inside_map(snake.current_snake_head, snake.segments[pos_i][0], snake.segments[pos_i][1])
            else:
                draw_block_inside_map(snake.current_snake_body, snake.segments[pos_i][0], snake.segments[pos_i][1])
    else:
        for pos_i in range(len(snake.segments) - 1, -1, -1):
            if pos_i == len(snake.segments) - 1:
                draw_block_inside_map(snake.current_snake_head, snake.segments[pos_i][0], snake.segments[pos_i][1])
            else:
                draw_block_inside_map(snake.current_snake_body, snake.segments[pos_i][0], snake.segments[pos_i][1])

def spawn_apple(GAME_MODE, snake, bomb_pos=None, walls=None):
    """Функция возвращает случайные координаты еды для змейки"""
    apple_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    if GAME_MODE == 3:
        while apple_pos in snake.segments or apple_pos in walls or apple_pos == bomb_pos:
            apple_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    elif GAME_MODE == 0:
        while apple_pos in snake.segments:
            apple_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    elif GAME_MODE == 1:
        while apple_pos in snake.segments or apple_pos == bomb_pos:
            apple_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    else:
        while apple_pos in snake.segments or apple_pos in walls:
            apple_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    return apple_pos

def spawn_bomb(GAME_MODE, snake, apple_pos, walls):
    """Функция возвращает случайные координаты бомбы для змейки"""
    bomb_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    if GAME_MODE == 3:
        while bomb_pos in snake.segments or bomb_pos == apple_pos or bomb_pos in walls:
            bomb_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    elif GAME_MODE == 1:
        while bomb_pos in snake.segments or bomb_pos == apple_pos:
            bomb_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    return bomb_pos

def spawn_wall(GAME_MODE, snake, apple_pos, bomb_pos, walls):
    """Функция возвращает случайные координаты бомбы для змейки"""
    wall_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    if GAME_MODE == 3:
        while wall_pos in snake.segments or wall_pos == apple_pos or wall_pos == bomb_pos or wall_pos in walls:
            wall_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    elif GAME_MODE == 2:
        while wall_pos in snake.segments or wall_pos == apple_pos or wall_pos in walls:
            wall_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
    return wall_pos


def write_highscore_in_file(highscore):
    with open("best_score", "w") as best_f:
        best_f.write(str(highscore))


def start_the_game():
    global screen, clock
    # Останавливаем музыку из меню
    pygame.mixer.music.pause()

    def intro():
        """Функция, выводящая текст с правилами игры"""
        intro = True
        while intro:
            screen.fill('white')
            message_to_screen(welcome_text, screen.get_height() // 2 - 220)
            message_to_screen(rules_text_1, screen.get_height() // 2 - 170)
            message_to_screen(rules_text_2, screen.get_height() // 2 - 130)
            message_to_screen(rules_text_3, screen.get_height() // 2 - 90)
            message_to_screen(rules_text_4, screen.get_height() // 2 - 50)
            message_to_screen(rules_text_5, screen.get_height() // 2 - 10)
            message_to_screen(rules_text_6, screen.get_height() // 2 + 30)
            message_to_screen(rules_play_text, screen.get_height() - 100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        intro = False

            pygame.display.update()
            clock.tick(5)

    # Запускаем экран с правилами
    intro()

    # создаем основной экран игры и подпись
    screen = pygame.display.set_mode(get_screen_size(RECT_COUNT))
    SCREEN_SIZE = get_screen_size(RECT_COUNT)

    #  Создаем полупрозрачный белый экран
    white_screen = pygame.Surface((SCREEN_SIZE), pygame.SRCALPHA)
    white_screen.fill((255, 255, 255, 128))

    # Считываем предыдущий рекорд пользователя
    with open("best_score", "r") as best_f:
        highscore = int(best_f.readline())

    # Задаем начальные параметры змейки, яблока, бомбы и препядствий
    snake = Snake(RECT_COUNT)

    bomb_pos = (-100, -100)
    walls = []
    apple_pos = spawn_apple(GAME_MODE, snake, bomb_pos, walls)
    if GAME_MODE in [1, 3]:
        bomb_pos = spawn_bomb(GAME_MODE, snake, apple_pos, walls)

    # Создаем таймер по которому будет шипеть змея
    hiss = pygame.USEREVENT + 1
    pygame.time.set_timer(hiss, 5000)

    # Запускаем цикл с игрой
    is_alive = True  # Если змейка жива, то равно True, если мертва или заполнила всю карту, то False
    is_playing = True  # Если включена игра, то равно True, иначе False
    cheats = -1

    while is_playing:
        # Проверяем все события, которые может создать пользователь
        changed_direction = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    cheats *= -1
                if is_alive:
                    # Если игра идет и змейка жива, то отслеживаем нажатие на стрелочки
                    if not changed_direction:
                        if event.key == pygame.K_RIGHT and snake.direction != 2:
                            snake.right()
                            changed_direction = True
                        elif event.key == pygame.K_LEFT and snake.direction not in [4, 0]:
                            snake.left()
                            changed_direction = True
                        elif event.key == pygame.K_UP and snake.direction != 1:
                            snake.up()
                            changed_direction = True
                        elif event.key == pygame.K_DOWN and snake.direction != 3:
                            snake.down()
                            changed_direction = True
                else:
                    # Отслеживаем перезапуск игры и затем перезапускаем игру с начальными параметрами
                    if event.key == pygame.K_SPACE:
                        is_alive = True
                        snake.spawn_snake(RECT_COUNT)
                        bomb_pos = (-100, -100)
                        walls = []
                        apple_pos = spawn_apple(GAME_MODE, snake, bomb_pos, walls)
                        if GAME_MODE in [1, 3]:
                            bomb_pos = spawn_bomb(GAME_MODE, snake, apple_pos, walls)
                        pygame.mixer.music.unpause()
                    # Отслеживаем выход в меню в конце игры
                    if event.key == pygame.K_ESCAPE:
                        is_playing = False
                        pygame.mixer.music.pause()
                        main_menu()
            # Отслеживаем шипение змеи
            if event.type == hiss and is_alive:
                snake_hiss.play()

        # Заполнение экрана основным цветом и создание заголовка
        screen.fill("#211E2B")
        pygame.draw.rect(screen, '#00ADB5', [0, 0, SCREEN_SIZE[0], HEADER_MARGIN])
        score_text = font_score.render(f"Score: {len(snake.segments)}", 1, "white")
        highscore_text = font_score.render(f"Highscore: {highscore}", 1, "white")
        screen.blit(score_text, (5, 5))
        screen.blit(highscore_text, (screen.get_width() - highscore_text.get_width() - RECT_SIZE, 5))

        # отрисовываем поле для змейки
        for row in range(RECT_COUNT):
            for column in range(RECT_COUNT):
                draw_block_inside_map(empty_block_surf, column, row)

        # Выведем еду, змейку, препятствия и бомбу на экран в зависимости от режима игры
        draw_block_inside_map(apple_surf, apple_pos[0], apple_pos[1])
        render_snake(snake, is_alive)
        if GAME_MODE in [1, 3]:
            draw_block_inside_map(bomb_surf, bomb_pos[0], bomb_pos[1])
        if GAME_MODE in [2, 3]:
            for wall in walls:
                draw_block_inside_map(wall_surf, wall[0], wall[1])

        # Логика движения змейки, поедания яблока, врезания в препятствие, поедания бомбы и отслеживание изменения счета, поражения и победы
        if is_alive:
            new_pos = snake.segments[-1][0] + snake.directions[snake.direction][0], snake.segments[-1][1] + \
                      snake.directions[snake.direction][1]
            if not snake.is_inside(new_pos, RECT_COUNT) or snake.is_collide_with_wall(new_pos, walls) or snake.is_collide_with_body(new_pos):
                if cheats == -1:
                    is_alive = False
                    hit_barrier.play()
                    snake.die()
                    # Если змейка врезалась в стену сохраняем рекордное значение её длины
                    write_highscore_in_file(highscore)
            else:
                if snake.direction != 4:  # Если змейка не стоит на месте
                    # Логика поедания яблока и создания препядствий
                    if new_pos == apple_pos:
                        snake.extend()
                        # Проверка на победу
                        if len(snake.segments) == RECT_COUNT * RECT_COUNT - 1 - len(walls) and GAME_MODE in [3, 1] or \
                                len(snake.segments) == RECT_COUNT * RECT_COUNT - len(walls) and GAME_MODE in [2, 0]:
                            is_alive = False
                        else:
                            # Логика создания препятствий
                            if (len(snake.segments) - 3) // 2 > len(walls) and GAME_MODE in [2, 3]:
                                walls.append(spawn_wall(GAME_MODE, snake, apple_pos, bomb_pos, walls))
                            eat_apple.play()
                            apple_pos = spawn_apple(GAME_MODE, snake, bomb_pos, walls)
                        # Если текущая длина змеи больше рекордной, то меняем рекордную длину
                        if len(snake.segments) > highscore:
                            highscore = len(snake.segments)
                    else:
                        snake.move()
                    # Логика взаимодействия с бомбой
                    if new_pos == bomb_pos and GAME_MODE in [1, 3]:
                        if len(snake.segments[(len(snake.segments) + 1) // 2:]) == 0:
                            if cheats == -1:
                                is_alive = False
                                snake.die()
                                write_highscore_in_file(highscore)
                        else:
                            snake.segments = snake.segments[(len(snake.segments) + 1) // 2:]
                        bomb_explosion.play()
                        bomb_pos = spawn_bomb(GAME_MODE, snake, apple_pos, walls)
        else:
            # Отображаем полупрозрачный белый экран
            screen.blit(white_screen, (0, 0))
            message_to_screen(replay_text, SCREEN_SIZE[1] // 2 + 10)
            message_to_screen(escape_text, SCREEN_SIZE[1] // 2 + 40)
            # Если игра выиграна, то вывести надпись о победе, если проиграна, то отобразить надпись о проигрыше
            if len(snake.segments) == RECT_COUNT * RECT_COUNT - 1 - len(walls) and GAME_MODE in [3, 1] or len(
                    snake.segments) == RECT_COUNT * RECT_COUNT - len(walls):
                message_to_screen(win_text, SCREEN_SIZE[1] // 2 - 50)
            else:
                message_to_screen(gameover_text, SCREEN_SIZE[1] // 2 - 50)

        pygame.display.update()
        clock.tick(FPS)


# Далее идет код главного меню
def set_difficulty(difficulty, value):
    global FPS, DIFFICULTY_ID
    DIFFICULTY_ID = value
    if value == 2:
        FPS = 30
    elif value == 1:
        FPS = 15
    elif value == 0:
        FPS = 8


def set_map_size(size, value):
    global RECT_COUNT, MAP_ID
    MAP_ID = value
    if value == 1:
        RECT_COUNT = 20
    elif value == 0:
        RECT_COUNT = 15
    else:
        RECT_COUNT = 10


def set_sound_volume(volume, value):
    global SOUND_ID, sounds
    for sound_i in range(len(sounds)):
        sounds[sound_i].set_volume(value/10)
    SOUND_ID = value


def set_game_mode(game_mode, value):
    global GAME_MODE
    GAME_MODE = value


def main_menu():
    """Функция, отвечающая за главное меню"""
    global screen

    def settings_menu():
        #  Создаем подменю с выбором настроек игры
        menu._open(settings)

    def mode_menu():
        #  Создаем подменю с выбором режима игры
        menu._open(mode)

    # Обновляем размер экрана для вывода главного меню
    screen = pygame.display.set_mode(get_screen_size(MENU_RECT_COUNT))

    menu = pygame_menu.Menu('Welcome', screen.get_width(), screen.get_height(),
                            theme=pygame_menu.themes.THEME_BLUE, )

    # Создаем кнопки для меню
    menu.add.button('Играть', start_the_game)
    menu.add.button('Выбрать режим', mode_menu)
    menu.add.button('Настройки', settings_menu)
    menu.add.button('Выйти', pygame_menu.events.EXIT)

    #  Создаем подменю с выбором режима игры
    mode = pygame_menu.Menu('Выбрать режим игры', screen.get_width(), screen.get_height(), theme=themes.THEME_BLUE)
    mode.add.selector('Режим: ', [('Без бомб и препятствий', 0), ('С бомбами', 1), ('С препятствиями', 2),
                                  ('С бомбами и препятствиями', 3)], onchange=set_game_mode, default=GAME_MODE)

    #  Создаем подменю с выбором настроек игры
    settings = pygame_menu.Menu('Настройки', screen.get_width(), screen.get_height(), theme=themes.THEME_BLUE)
    settings.add.selector('Сложность: ', [('Легкая', 0), ('Средняя', 1), ('Тяжелая', 2)], onchange=set_difficulty,
                          default=DIFFICULTY_ID)
    settings.add.selector('Размер карты: ', [('Средняя(15x15)', 0), ('Большая(20x20)', 1), ('Маленькая(10x10)', 2)],
                          onchange=set_map_size, default=MAP_ID)
    settings.add.selector('Громкость звуков: ',
                          [('0%', 0),
                           ('10%', 1), ('20%', 2), ('30%', 3), ('40%', 4), ('50%', 5), ('60%', 6), ('70%', 7),
                           ('80%', 8), ('90%', 9), ('100%', 10)],
                          onchange=set_sound_volume, default=SOUND_ID)

    # Отслеживание действий пользователя и отрисовка меню
    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            # Добавим возможность с помощью кнопки ESCAPE возращаться к предыдущему меню
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.get_current().reset(1)

        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)
        pygame.display.update()
        clock.tick(20)


if __name__ == "__main__":
    main_menu()
