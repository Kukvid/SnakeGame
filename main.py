import random
import pygame

pygame.init()  # Инициализируем встроенные в библиотеку модули

# Задаем параметры экрана и игры
# WIDTH, HEIGHT = 720, 480

FPS = 8
RECT_SIZE = 24
RECT_COUNT = 20
MARGIN = 1 # отступ
HEADER_MARGIN = 70
SCREEN_SIZE = [
    RECT_SIZE * RECT_COUNT + 2 * RECT_SIZE + MARGIN * RECT_COUNT,
    RECT_SIZE * RECT_COUNT + 2 * RECT_SIZE + MARGIN * RECT_COUNT + HEADER_MARGIN
]
# MAP_SIZE = [
#     RECT_SIZE * RECT_COUNT + 2 * RECT_SIZE + MARGIN * RECT_COUNT
# ]


screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Snake by Minakov Daniil")

clock = pygame.time.Clock()
with open("best_score","r") as best_f:
    highscore = int(best_f.readline())

pygame.font.init()
font_score = pygame.font.SysFont("Arial", 25)
font_gameover = pygame.font.SysFont("Arial", 45)
font_space = pygame.font.SysFont("Arial", 18)
# Задаем используемые цвета
FRAME_COLOR = (0,255,204)
LIGHT_BLUE = (204, 255, 255)
HEADER_COLOR = (0, 204, 153)
# Задаем начальные параметры змейки и яблока
snake = [((RECT_COUNT // 2) - 2, RECT_COUNT // 2), ((RECT_COUNT // 2) - 1, RECT_COUNT // 2),
         (RECT_COUNT // 2, RECT_COUNT // 2)]
direction = 0
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

apple_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
empty_block_surf = pygame.image.load('images/Empty.png').convert_alpha()
food_surf = pygame.image.load('images/Food.png').convert_alpha()
snake_head_surf = pygame.image.load('images/Head.png').convert_alpha()
snake_body_surf = pygame.image.load('images/Body.png').convert_alpha()
snake_head_up = pygame.transform.scale(snake_head_surf, (RECT_SIZE, RECT_SIZE))
snake_body_surf = pygame.transform.scale(snake_body_surf, (RECT_SIZE, RECT_SIZE))
empty_block_surf = pygame.transform.scale(empty_block_surf, (RECT_SIZE, RECT_SIZE))
food_surf = pygame.transform.scale(food_surf, (RECT_SIZE, RECT_SIZE))
snake_head_right = pygame.transform.rotate(snake_head_up, -90)
snake_head_down = pygame.transform.rotate(snake_head_up, 180)
snake_head_left = pygame.transform.rotate(snake_head_up, 90)
current_snake_head = snake_head_right
def draw_block(surf, column, row):
    screen.blit(surf,[RECT_SIZE + column * RECT_SIZE + MARGIN * (column + 1), HEADER_MARGIN + RECT_SIZE + row * RECT_SIZE + MARGIN * (row + 1), RECT_SIZE,
                      RECT_SIZE])


# Запускаем цикл с игрой
game_active = True
safe_mode = 1
while True:
    # Проверяем все события, которые может создать пользователь
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if game_active:
                # Если игра идет и змейка жива, то отслеживаем нажатие на стрелочки
                if event.key == pygame.K_RIGHT and direction != 2:
                    direction = 0
                    current_snake_head = snake_head_right
                elif event.key == pygame.K_LEFT and direction != 0:
                    direction = 2
                    current_snake_head = snake_head_left
                elif event.key == pygame.K_UP and direction != 1:
                    direction = 3
                    current_snake_head = snake_head_up
                elif event.key == pygame.K_DOWN and direction != 3:
                    direction = 1
                    current_snake_head = snake_head_down
            else:
                # Отслеживаем перезапуск игры и затем перезапускаем игру с начальными параметрами
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snake = [((RECT_COUNT // 2) - 2, RECT_COUNT // 2), ((RECT_COUNT // 2) - 1, RECT_COUNT // 2),
                             (RECT_COUNT // 2, RECT_COUNT // 2)]
                    apple_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
                    direction = 0
                    current_snake_head = snake_head_right
    #Проверка ввода читов
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LCTRL] and keys[pygame.K_4]:
        safe_mode *= -1

    # Заполнение экрана основным цветом и создание заголовка
    screen.fill("#211E2B")
    pygame.draw.rect(screen, HEADER_COLOR, [0,0,SCREEN_SIZE[0],HEADER_MARGIN])

    # отрисовываем поле для змейки
    for row in range(RECT_COUNT):
        for column in range(RECT_COUNT):
            draw_block(empty_block_surf, column, row)
    # Выведем змейку и яблоко на экран
    # [pygame.draw.rect(screen, 'green', (pos[0] * RECT_SIZE + 1, pos[1] * RECT_SIZE + 1, RECT_SIZE, RECT_SIZE)) for pos in snake]
    for pos_i in range(len(snake)):
        if pos_i == len(snake)- 1:
            draw_block(current_snake_head, snake[pos_i][0], snake[pos_i][1])
        else:
            # draw_block('green', snake[pos_i][0], snake[pos_i][1])
            draw_block(snake_body_surf, snake[pos_i][0], snake[pos_i][1])
    # pygame.draw.rect(screen, 'red', (apple_pos[0] * RECT_SIZE, apple_pos[1] * RECT_SIZE, RECT_SIZE, RECT_SIZE))
    # draw_block('red', apple_pos[0],apple_pos[1])
    draw_block(food_surf, apple_pos[0], apple_pos[1])
    # Логика движения змейки, поедания яблока и отслеживания изменения счета
    if game_active:
        new_pos = snake[-1][0] + directions[direction][0], snake[-1][1] + directions[direction][1]
        if not (0 <= new_pos[0] < RECT_COUNT and 0 <= new_pos[1] < RECT_COUNT) or \
                new_pos in snake:
            if safe_mode == 1:
                game_active = False
            with open("best_score", "w") as best_f:
                best_f.write(str(highscore))
        else:
            snake.append(new_pos)
            if new_pos == apple_pos:
                # fps += 1
                while apple_pos in snake:
                    apple_pos = random.randint(0, RECT_COUNT - 1), random.randint(0, RECT_COUNT - 1)
                if len(snake) > highscore:
                    highscore = len(snake)
            else:
                snake.pop(0)
        score_text = font_score.render(f"Score: {len(snake)} Highscore: {highscore}", 1, "red")
        screen.blit(score_text, (5, 5))
    else:
        white_screen = pygame.Surface((SCREEN_SIZE), pygame.SRCALPHA)
        white_screen.fill((255, 255, 255, 128))
        screen.blit(white_screen, (0, 0))

        gameover_text = font_gameover.render("GAME OVER", 1, "black")
        screen.blit(gameover_text, (SCREEN_SIZE[0] // 2 - gameover_text.get_width()//2, SCREEN_SIZE[1] // 2 - 50))
        replay_text = font_space.render("Press SPACE to replay", 1, "black")
        screen.blit(replay_text, (SCREEN_SIZE[0] // 2 - replay_text.get_width()//2, SCREEN_SIZE[1] // 2 + 10))

    pygame.display.update()
    clock.tick(FPS)
