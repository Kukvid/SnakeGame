import pygame
import pygame_menu
from pygame_menu import themes

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
    global SOUND_VOLUME, SOUND_ID
    SOUND_ID = value
    pygame.mixer.music.set_volume(SOUND_VOLUME)


def set_game_mode(game_mode, value):
    global GAME_MODE
    GAME_MODE = value


def show_main_menu(start_the_game, game_settings=None):
    """Функция, отвечающая за главное меню"""

    if game_settings is not None:
        SOUND_VOLUME, SOUND_ID, MAP_ID, DIFFICULTY_ID, RECT_COUNT, FPS, GAME_MODE = game_settings
    else:
        RECT_COUNT = 15
        MENU_RECT_COUNT = 18
        RECT_SIZE = 30
        MARGIN = 1  # отступ
        HEADER_MARGIN = 70
        MENU_SCREEN_SIZE = [
            RECT_SIZE * MENU_RECT_COUNT + 2 * RECT_SIZE + MARGIN * MENU_RECT_COUNT,
            RECT_SIZE * MENU_RECT_COUNT + 2 * RECT_SIZE + MARGIN * MENU_RECT_COUNT + HEADER_MARGIN
        ]
        SOUND_VOLUME = 0.5
        MAP_ID = 0
        SOUND_ID = 5
        DIFFICULTY_ID = 1
        GAME_MODE = 0

    def settings_menu():
        #  Создаем подменю с выбором настроек игры
        menu._open(settings)

    def mode_menu():
        #  Создаем подменю с выбором режима игры
        menu._open(mode)

    # Обновляем размер экрана для вывода главного меню
    screen = pygame.display.set_mode(MENU_SCREEN_SIZE)

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

