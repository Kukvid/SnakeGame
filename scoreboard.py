from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")

with open("best_score") as f:
    best = int(f.readline())


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.best = best
        self.color("red")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f"Score: {self.score} Best: {self.best}", align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
        with open("best_score", "w") as f:
            f.write(str(self.best))

    def win(self):
        self.goto(0, 0)
        self.color("gold")
        self.write("YOU WIN!", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        if self.score > self.best:
            self.best = self.score
        self.clear()
        self.update_scoreboard()
