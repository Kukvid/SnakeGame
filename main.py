import winsound
from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.title("Змейка от Даниила Минакова")
screen.colormode(255)
screen.bgcolor(194, 178, 128)
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")
WIN_SCORE = 25


# Экран-заставка
# character_pen = Character
def game():
    winsound.PlaySound("Electro-Light.wav",winsound.SND_NODEFAULT|winsound.SND_ASYNC|winsound.SND_LOOP)
    game_is_on = True
    # Запускаем процесс игры
    while game_is_on:
        # snake.move()
        time.sleep(0.16)
        if scoreboard.score == WIN_SCORE:
            game_is_on = False
            scoreboard.win()
        # Detect collision with food.
        if snake.head.distance(food) < 15:
            snake.extend()
            scoreboard.increase_score()
            if game_is_on:
                food.refresh()
            else: food.delete()

        # Detect collision with wall.
        if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
            game_is_on = False
            snake.dead_snake(screen)
            scoreboard.game_over()

        # Detect collision with tail.
        for segment in snake.segments:
            if segment == snake.head:
                pass
            elif snake.head.distance(segment) < 10:
                game_is_on = False
                snake.dead_snake(screen)
                scoreboard.game_over()
        screen.update()
        if game_is_on:
            snake.move()


game()
# screen.exitonclick()
screen.mainloop()
