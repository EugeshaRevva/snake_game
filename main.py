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

# Класс для всех игровых объектов
class GameObject:
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.body_color, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# Класс яблока
class Apple(GameObject):
    def __init__(self):
        # Устанавливаем случайную позицию
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, screen):
        super().draw(screen)

# Класс змейки
class Snake(GameObject):
    def __init__(self):
        self.body_color = GREEN
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # Начальная позиция змейки
        self.length = 1
        self.direction = (GRID_SIZE, 0)  # Начальное движение вправо
        self.next_direction = None  # Для хранения направления после обработки клавиши

    def update_direction(self):
        """Обновляем направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигаем змейку, добавляем новый сегмент головы и удаляем хвост, если не съедаем яблоко"""
        head_x, head_y = self.positions[0]
        direction_x, direction_y = self.direction
        new_head = (head_x + direction_x, head_y + direction_y)

        # Если змейка выходит за границу, появляется с другой стороны
        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, screen):
        """Отрисовываем все сегменты змейки"""
        for segment in self.positions:
            pygame.draw.rect(screen, self.body_color, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасываем змейку после столкновения с собой"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)

# Обработка нажатий клавиш
def handle_keys(snake):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake.direction != (0, GRID_SIZE):
        snake.next_direction = (0, -GRID_SIZE)
    elif keys[pygame.K_DOWN] and snake.direction != (0, -GRID_SIZE):
        snake.next_direction = (0, GRID_SIZE)
    elif keys[pygame.K_LEFT] and snake.direction != (GRID_SIZE, 0):
        snake.next_direction = (-GRID_SIZE, 0)
    elif keys[pygame.K_RIGHT] and snake.direction != (-GRID_SIZE, 0):
        snake.next_direction = (GRID_SIZE, 0)

# Основной игровой цикл
def main():
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
        screen.fill(BLACK)

        # Отрисовываем яблоко и змейку
        apple.draw(screen)
        snake.draw(screen)

        # Обновляем экран
        pygame.display.update()

        # Замедляем игру
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
