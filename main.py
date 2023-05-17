import random

import pygame

pygame.init()  # Инициализируем встроенные в библиотеку модули

# Задаем параметры экрана и игры
WIDTH, HEIGHT = 720, 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake by Minakov Daniil")

fps = 5
RECT_SIZE = 30
MAP_SIZE = WIDTH // RECT_SIZE, HEIGHT // RECT_SIZE
clock = pygame.time.Clock()

pygame.font.init()
font_score = pygame.font.SysFont("Arial", 25)
font_gameover = pygame.font.SysFont("Arial", 45)
font_space = pygame.font.SysFont("Arial", 18)

# Задаем начальные параметры змейки и яблока
snake = [((MAP_SIZE[0] // 2) - 2, MAP_SIZE[1] // 2), ((MAP_SIZE[0] // 2) - 1, MAP_SIZE[1] // 2),
         (MAP_SIZE[0] // 2, MAP_SIZE[1] // 2)]

direction = 0
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

apple_pos = random.randint(0, MAP_SIZE[0] - 1), random.randint(0, MAP_SIZE[1] - 1)

# Запускаем цикл с игрой
game_active = True
while True:
    screen.fill('#e1bf92')  # Заполняем экран цветом

    # Проверяем все события, которые может создать пользователь
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and direction != 2:
                direction = 0
            if event.key == pygame.K_LEFT and direction != 0:
                direction = 2
            if event.key == pygame.K_UP and direction != 1:
                direction = 3
            if event.key == pygame.K_DOWN and direction != 3:
                direction = 1
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                snake = [((MAP_SIZE[0] // 2) - 2, MAP_SIZE[1] // 2), ((MAP_SIZE[0] // 2) - 1, MAP_SIZE[1] // 2),
                         (MAP_SIZE[0] // 2, MAP_SIZE[1] // 2)]
                apple_pos = random.randint(0, MAP_SIZE[0] - 1), random.randint(0, MAP_SIZE[1] - 1)
                direction = 0
                fps = 5

    # Выведем змейку и яблоко на экран
    [pygame.draw.rect(screen, 'green', (pos[0] * RECT_SIZE, pos[1] * RECT_SIZE, RECT_SIZE, RECT_SIZE)) for pos in snake]
    pygame.draw.rect(screen, 'red', (apple_pos[0] * RECT_SIZE, apple_pos[1] * RECT_SIZE, RECT_SIZE, RECT_SIZE))

    # Логика движения змейки
    if game_active:
        new_pos = snake[-1][0] + directions[direction][0], snake[-1][1] + directions[direction][1]
        if not (0 <= new_pos[0] < MAP_SIZE[0] and 0 <= new_pos[1] < MAP_SIZE[1]) or \
                new_pos in snake:
            game_active = False
        else:
            snake.append(new_pos)
            if new_pos == apple_pos:
                fps += 1
                while apple_pos in snake:
                    apple_pos = random.randint(0, MAP_SIZE[0] - 1), random.randint(0, MAP_SIZE[1] - 1)
            else:
                snake.pop(0)
    else:
        white_screen = pygame.Surface((720, 480), pygame.SRCALPHA)
        white_screen.fill((255, 255, 255, 128))
        screen.blit(white_screen, (0, 0))

        gameover_text = font_gameover.render(f"GAME OVER", 1, "black")
        screen.blit(gameover_text, (WIDTH // 2 - gameover_text.get_width() // 2, HEIGHT // 2 - 50))
        replay_text = font_space.render("Press SPACE to replay", 1, "black")
        screen.blit(replay_text, (WIDTH // 2 - replay_text.get_width() // 2, HEIGHT // 2 + 10))

    score_text = font_score.render(f"Score: {len(snake)}", 1, "red")
    screen.blit(score_text, (5, 5))
    pygame.display.update()
    clock.tick(fps)
