import pygame

class SnakeView:

    COLOR_SNAKE = (0, 100, 0)

    def __init__(self, screen, fieldSize):
        self.screen = screen
        self.fieldSize = fieldSize

    def display(self, snake):
        for segment in snake.segments:
            self.drawSegment(self.screen, snake, segment[0], segment[1])

    def drawSegment(self, surface, snake, x, y):
        life = snake.life
        if life > 0:
            pygame.draw.rect(surface, self.COLOR_SNAKE, (
                x * self.fieldSize + (self.fieldSize * (1 - snake.life) // 2),
                y * self.fieldSize + (self.fieldSize * (1 - snake.life) // 2),
                self.fieldSize * snake.life,
                self.fieldSize * snake.life,
            ))