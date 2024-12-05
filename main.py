import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 15

# Цвета
WHITE = (255, 255, 255)
BLACK = (21, 21, 21)
GREEN = (0, 102, 0)
RED = (255, 51, 0)

# Константы направления
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

# Цвет фона
BOARD_BACKGROUND_COLOR = (0, 0, 0)


# Класс для всех игровых объектов
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """
        Инициализация игрового объекта.

        :param position: начальная позиция объекта (x, y)
        :param body_color: цвет объекта
        """
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        """Рисует объект на экране."""
        pygame.draw.rect(
            screen,
            self.body_color,
            pygame.Rect(
                self.position[0], self.position[1], GRID_SIZE, GRID_SIZE),
        )


# Класс яблока
class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Создает объект яблока со случайной позицией."""
        super().__init__((0, 0), RED)
        self.randomize_position()

    def randomize_position(self):
        """Случайным образом определяет позицию яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )


# Класс змейки
class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Создает объект змейки."""
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), GREEN)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = (GRID_SIZE, 0)
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку, добавляет сегмент головы и удаляет хвост."""
        head_x, head_y = self.positions[0]
        direction_x, direction_y = self.direction
        new_head = (head_x + direction_x, head_y + direction_y)

        # Если змейка выходит за границу, появляется с другой стороны
        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, screen):
        """Рисование змейки."""
        for segment in self.positions:
            pygame.draw.rect(
                screen,
                self.body_color,
                pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE),
            )

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку после столкновения с собой."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)


# Обработка нажатий клавиш
def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake.direction != (0, GRID_SIZE):
        snake.next_direction = UP
    elif keys[pygame.K_DOWN] and snake.direction != (0, -GRID_SIZE):
        snake.next_direction = DOWN
    elif keys[pygame.K_LEFT] and snake.direction != (GRID_SIZE, 0):
        snake.next_direction = LEFT
    elif keys[pygame.K_RIGHT] and snake.direction != (-GRID_SIZE, 0):
        snake.next_direction = RIGHT


# Основной игровой цикл
def main():
    """
    Основной игровой цикл.

    Инициализирует экран, создает объекты игры и запускает игровой процесс.
    """
    # Инициализация окна и экрана
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()

    # Создаем объекты
    snake = Snake()
    apple = Apple()

    running = True
    while running:
        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обрабатываем нажатия клавиш
        handle_keys(snake)

        # Обновляем направление
        snake.update_direction()

        # Двигаем змейку
        snake.move()

        # Проверка на столкновение с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка на столкновение с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Отображаем всё на экране
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Рисование яблока и змейки
        apple.draw(screen)
        snake.draw(screen)

        # Обновляем экран
        pygame.display.update()

        # Замедляем игру
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
