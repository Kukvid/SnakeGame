import pygame
RECT_SIZE = 30

# Создаем поверхности с картинками или с определенными цветами
snake_head_up_surf = pygame.image.load('images/head.png').convert_alpha()
snake_head_dead_up_surf = pygame.image.load('images/dead_head.png').convert_alpha()
snake_body_surf = pygame.image.load('images/body.png').convert_alpha()
snake_body_dead_surf = pygame.image.load('images/dead_body.png').convert_alpha()

empty_block_surf = pygame.image.load('images/empty.png').convert_alpha()
apple_surf = pygame.image.load('images/food.png').convert_alpha()
bomb_surf = pygame.image.load('images/bomb.png').convert_alpha()
wall_surf = pygame.image.load('images/wall.png')

# Масштабируем картинки до нужных размеров
snake_head_up_surf = pygame.transform.scale(snake_head_up_surf, (RECT_SIZE, RECT_SIZE))
snake_head_dead_up_surf = pygame.transform.scale(snake_head_dead_up_surf, (RECT_SIZE, RECT_SIZE))
snake_body_dead_surf = pygame.transform.scale(snake_body_dead_surf, (RECT_SIZE, RECT_SIZE))
snake_body_surf = pygame.transform.scale(snake_body_surf, (RECT_SIZE, RECT_SIZE))

empty_block_surf = pygame.transform.scale(empty_block_surf, (RECT_SIZE, RECT_SIZE))
apple_surf = pygame.transform.scale(apple_surf, (RECT_SIZE, RECT_SIZE))
bomb_surf = pygame.transform.scale(bomb_surf, (RECT_SIZE, RECT_SIZE+5))
wall_surf = pygame.transform.scale(wall_surf, (RECT_SIZE, RECT_SIZE+5))

# Поворачиваем картинку головы змеи на разные углы, чтобы при движении менялось направление её взгляда
snake_head_right_surf = pygame.transform.rotate(snake_head_up_surf, -90)
snake_head_down_surf = pygame.transform.rotate(snake_head_up_surf, 180)
snake_head_left_surf = pygame.transform.rotate(snake_head_up_surf, 90)

snake_head_dead_right_surf = pygame.transform.rotate(snake_head_dead_up_surf, -90)
snake_head_dead_down_surf = pygame.transform.rotate(snake_head_dead_up_surf, 180)
snake_head_dead_left_surf = pygame.transform.rotate(snake_head_dead_up_surf, 90)

# подключаем шрифты
pygame.font.init()
font_score = pygame.font.SysFont("Arial", 36)
font_gameover = font_win = font_welcome = pygame.font.SysFont("Arial", 40)
font_space = pygame.font.SysFont("Arial", 18)
font_escape = pygame.font.SysFont("Arial", 15)
font_rules = pygame.font.SysFont("Arial", 20)


# создаем поверхности с текстом
replay_text = font_space.render("Нажмите SPACE чтобы сыграть снова", 1, "black")
rules_play_text = font_space.render("Нажмите SPACE чтобы сыграть", 1, "black")
escape_text = font_escape.render("Нажмите ESC чтобы вернуться в меню", 1, "black")
win_text = font_win.render("Вы выиграли!", 1, "black")
gameover_text = font_gameover.render("Поражение", 1, "black")
rules_welcome_text = font_welcome.render("Добро пожаловать в Змейку!", 1, "green")
rules_text_1 = font_rules.render("Цель игры - есть красные яблоки.", 1, "black")
rules_text_2 = font_rules.render("Чем больше яблок вы съедите, тем длиннее будет змея.", 1, "black")
rules_text_3 = font_rules.render("Если вы врежетесь в себя или в стену, то змейка погибнет!", 1, "black")
rules_text_4 = font_rules.render("В зависимости от выбранного в настройках режима игры", 1, "black")
rules_text_5 = font_rules.render("могут попадаться препятствия и бомбы, препятствия действуют как", 1, "black")
rules_text_6 = font_rules.render("стены, а бомба уменьшает змейку вдвое.", 1, "black")