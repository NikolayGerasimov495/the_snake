from random import choice, randint
import pygame

# Initializing PyGame
pygame.init()

# Constants for determining colors
APPLE_COLOR: tuple = (255, 0, 0)  # It's RED COLOR
SNAKE_COLOR: tuple = (0, 255, 0)  # It's GREEN COLOR
BOARD_BACKGROUND_COLOR: tuple = (0, 0, 0)  # It's BLACK COLOR
AQUAMARINE_CRAYOLA: tuple = (93, 216, 228)

# Constants for sizes
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Directions of movement
UP: tuple = (0, -1)
DOWN: tuple = (0, 1)
LEFT: tuple = (-1, 0)
RIGHT: tuple = (1, 0)

# The speed of the snake's movement
SPEED: int = 15

# Setting up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Title of the playing field window
pygame.display.set_caption("Змейка")

# Time setting
clock = pygame.time.Clock()


class GameObject:
    """Base class for game objects"""

    def __init__(self, body_color=None):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Method to draw a GameObject"""
        raise NotImplementedError(
            'Please implement "draw_cell" method of "GameObject" class.'
        )

    def draw_cell(self, surface, *args):
        """Method for drawing an object. Redefined in the subclasses"""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, AQUAMARINE_CRAYOLA, rect, 1)


class Apple(GameObject):
    """Class for representing an apple"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position()
        self.body_color = body_color

    def randomize_position(self):
        """Sets the random position of the apple"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw_cell(self, surface, *args):
        """Method to draw the Apple object"""
        super().draw_cell(surface)


class Snake(GameObject):
    """A class for representing a snake"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__()
        self.next_direction = None
        self.body_color = body_color
        self.last = None
        self.reset()

    def update_direction(self):
        """# The method of updating the direction after pressing the button"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw_cell(self, surface, *args):
        """Method to draw the Snake object"""
        for self.position in self.positions[:-1]:
            super().draw_cell(surface, self.position)

        """Drawing the snake's head"""
        for self.position in self.positions:
            super().draw_cell(surface, self.position[0])

        """Overwrite the last segment"""
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Method to move a snake"""
        head_snake = self.get_head_position()
        dx, dy = self.direction
        new_position = (
            (head_snake[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_snake[1] + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        if new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def get_head_position(self):
        """Returns the position of the snake's head"""
        return self.positions[0]

    def reset(self):
        """Returns the snake to its original state"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Function to handle user's presses"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
                game_object.update_direction()
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
                game_object.update_direction()
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
                game_object.update_direction()
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
                game_object.update_direction()


def main():
    """Main function"""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        apple.draw_cell(screen)
        snake.draw_cell(screen)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        pygame.display.update()


if __name__ == "__main__":
    main()
