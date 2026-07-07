from random import choice

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTR = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

KEY_TO_DIRECTION = {
    (pg.K_UP): UP,
    (pg.K_DOWN): DOWN,
    (pg.K_LEFT): LEFT,
    (pg.K_RIGHT): RIGHT,
    (pg.K_w): UP,
    (pg.K_s): DOWN,
    (pg.K_a): LEFT,
    (pg.K_d): RIGHT,
}

RETURN_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}

BOARD_BACKGROUND_COLOR = (125, 125, 125)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка — для выхода нажмите ESC')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Храниться общие свойства игровых объектов."""

    def __init__(self, body_color=None):
        self.position = SCREEN_CENTR
        self.body_color = body_color

    def draw(self):
        """
        Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """

    def draw_cell(self, position, color=None):
        """Отрисовка ячейки"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        color = color or self.body_color
        pg.draw.rect(screen, color, rect)
        if color == self.body_color:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Содержит координаты яблока и случайным образом
    генерирует новые координаты яблока при его съедании.
    """

    def __init__(self, positions=None, body_color=APPLE_COLOR):
        positions = positions or []
        super().__init__(body_color)
        self.randomize_position(positions)

    def randomize_position(self, positions):
        """Устанавливает случайное положение яблока на игровом поле."""
        free_cells = list(CELLS - set(positions))

        if not free_cells:
            pg.quit()
            raise SystemExit
        self.position = choice(free_cells)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """
    Представляет змею в игре: хранит тело, направление
    и управляет движением.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset(RIGHT)

    def update_direction(self, direction):
        """Обновляет направление движения змейки."""
        if direction != RETURN_DIRECTIONS[self.direction]:
            self.direction = direction

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции)."""
        head_x, head_y = self.get_head_position()
        d_x, d_y = self.direction
        self.positions.insert(0, (
            (head_x + (d_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (d_y * GRID_SIZE)) % SCREEN_HEIGHT))
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def get_head_position(self):
        """
        Возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self, direction=None):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.last = None
        self.positions = [SCREEN_CENTR]
        self.direction = direction or choice((UP, DOWN, LEFT, RIGHT))

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        self.draw_cell(self.get_head_position())
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                     and event.key == pg.K_ESCAPE):
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key not in KEY_TO_DIRECTION:
                return
            snake.update_direction(KEY_TO_DIRECTION[event.key])


def main():
    """
    Управляет обновлением всей игры: получает действия пользователя,
    изменяет состояние объектов и обновляет экран
    """
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:

        handle_keys(snake)
        snake.move()
        head_position = snake.get_head_position()

        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif head_position in snake.positions[3:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
