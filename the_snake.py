from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTR = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Храниться общие свойства игровых объектов."""

    def __init__(self):
        self.position = [SCREEN_CENTR]
        self.body_color = None

    def draw(self):
        """
        Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Содержит координаты яблока и случайным образом
    генерирует новые координаты яблока при его съедании.
    """

    def __init__(self):
        super(Apple, self).__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x_position = randint(0, GRID_WIDTH - 2) * GRID_SIZE
        y_position = randint(0, GRID_HEIGHT - 2) * GRID_SIZE
        self.position = (x_position, y_position)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Представляет змею в игре: хранит тело, направление
    и управляет движением.
    """

    def __init__(self, next_direction=None):
        super(Snake, self).__init__()
        self.lenght = 1
        self.direction = RIGHT
        self.next_direction = next_direction
        self.body_color = (0, 255, 0)
        self.last = None
        self.positions = self.position

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции)."""
        head_x, head_y = self.get_head_position()
        d_x, d_y = self.direction
        new_head_x = (head_x + (d_x * GRID_SIZE)) % SCREEN_WIDTH
        new_head_y = (head_y + (d_y * GRID_SIZE)) % SCREEN_HEIGHT
        new_position_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_position_head)
        if len(self.positions) != self.lenght:
            self.last = self.positions.pop()

    def get_head_position(self):
        """
        Возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.lenght = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None
        self.positions = [SCREEN_CENTR]

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Управляет обновлением всей игры: получает действия пользователя,
    изменяет состояние объектов и обновляет экран
    """
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:

        handle_keys(snake)

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.update_direction()
        snake.move()
        head_position = snake.get_head_position()

        if head_position == apple.position:
            snake.lenght += 1
            apple.randomize_position()

        for position in snake.positions[1:]:
            if head_position == position:
                snake.reset()

        apple.draw()
        snake.draw()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
