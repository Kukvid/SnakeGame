import pygame
from surfaces import snake_body_surf, snake_head_up_surf, snake_head_left_surf, snake_head_right_surf, snake_head_down_surf, snake_head_dead_left_surf, snake_body_dead_surf, snake_head_dead_right_surf, snake_head_dead_down_surf, snake_head_dead_up_surf


class Snake:
    def __init__(self, RECT_COUNT):
        self.segments = [((RECT_COUNT // 2) - 2, RECT_COUNT // 2), ((RECT_COUNT // 2) - 1, RECT_COUNT // 2),
                 (RECT_COUNT // 2, RECT_COUNT // 2)]
        self.current_snake_head = snake_head_right_surf # изначально змейка движется вправо, поэтому картинка головы должна быть направлена в ту же сторону
        self.current_snake_body = snake_body_surf
        self.direction = 4
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]


    def spawn_snake(self, RECT_COUNT):
        # Задаем начальные параметры змейки
        self.segments = [((RECT_COUNT // 2) - 2, RECT_COUNT // 2), ((RECT_COUNT // 2) - 1, RECT_COUNT // 2),
                 (RECT_COUNT // 2, RECT_COUNT // 2)]
        self.current_snake_head = snake_head_right_surf
        self.current_snake_body = snake_body_surf
        self.direction = 4
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]

    def is_inside(self, new_pos, RECT_COUNT):
        if 0 <= new_pos[0] < RECT_COUNT and 0 <= new_pos[1] < RECT_COUNT:
                return True
        return False

    def is_collide_with_wall(self, new_pos, walls):
        if new_pos in walls:
            return True
        return False


    def is_collide_with_bomb(self, new_pos, bombs):
        if new_pos in bombs:
            return True
        return False


    def is_collide_with_body(self, new_pos):
        if new_pos in self.segments and self.direction != 4:
            return True
        return False


    def extend(self):
        head_pos = self.segments[-1]
        self.segments.append((head_pos[0] + self.directions[self.direction][0],
                              head_pos[1] + self.directions[self.direction][1]))


    def move(self):
        head_pos = self.segments[-1]
        self.segments.append((head_pos[0] + self.directions[self.direction][0],
                         head_pos[1] + self.directions[self.direction][1]))
        self.segments.pop(0)


    def get_head_of_dead_snake(self):
        """Функция возвращает соответствующие картинки головы мертвой змейки"""
        if self.current_snake_head == snake_head_up_surf:
            self.current_snake_head = snake_head_dead_up_surf
        elif self.current_snake_head == snake_head_right_surf:
            self.current_snake_head = snake_head_dead_right_surf
        elif self.current_snake_head == snake_head_left_surf:
            self.current_snake_head = snake_head_dead_left_surf
        else:
            self.current_snake_head = snake_head_dead_down_surf
        return self.current_snake_head


    def die(self):
        self.current_snake_head = self.get_head_of_dead_snake()
        self.current_snake_body = snake_body_dead_surf


    def up(self):
        self.direction = 3
        self.current_snake_head = snake_head_up_surf

    def down(self):
        self.direction = 1
        self.current_snake_head = snake_head_down_surf

    def left(self):
        self.direction = 2
        self.current_snake_head = snake_head_left_surf

    def right(self):
        self.direction = 0
        self.current_snake_head = snake_head_right_surf
