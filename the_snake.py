from random import choice

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTR = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

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
        self.position = [SCREEN_CENTR]
        self.body_color = body_color

    def draw(self):
        """
        Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """

    def draw_cell(self, position, color=None, border=True):
        """Отрисовка ячейки"""
        if color is None:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Содержит координаты яблока и случайным образом
    генерирует новые координаты яблока при его съедании.
    """

    def __init__(self, positions=SCREEN_CENTR, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.positions = positions
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        occupied_cell = set(self.positions)
        free_cells = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in occupied_cell
        ]

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
        self.reset()

    def update_direction(self, direction):
        """Обновляет направление движения змейки."""
        self.direction = direction

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции)."""
        head_x, head_y = self.get_head_position()
        d_x, d_y = self.direction
        new_head_x = (head_x + (d_x * GRID_SIZE)) % SCREEN_WIDTH
        new_head_y = (head_y + (d_y * GRID_SIZE)) % SCREEN_HEIGHT
        self.positions.insert(0, (new_head_x, new_head_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """
        Возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.direction = RIGHT
        self.last = None
        self.positions = [SCREEN_CENTR]

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions:
            self.draw_cell(position)
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR, False)


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    key_to_direction = {
        (pg.K_UP): UP,
        (pg.K_DOWN): DOWN,
        (pg.K_LEFT): LEFT,
        (pg.K_RIGHT): RIGHT,
    }

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            elif key_to_direction.get(event.key) is None:
                return
            elif (
                key_to_direction[event.key][0] != -snake.direction[0]
                and key_to_direction[event.key][1] != -snake.direction[1]
            ):
                snake.update_direction(key_to_direction[event.key])


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
        apple.positions = snake.positions

        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position()

        if head_position in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
