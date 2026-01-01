import pygame

class SnakeView:

    COLOR_SNAKE = (0, 100, 0)

    def __init__(self, screen, fieldSize):
        self.screen = screen
        self.fieldSize = fieldSize

    def display(self, snake):
        for segment in snake.segments:
            self.drawSegment(self.screen, segment[0], segment[1])

    def drawSegment(self, surface, x, y):
        pygame.draw.rect(surface, self.COLOR_SNAKE, (
            x * self.fieldSize,
            y * self.fieldSize,
            self.fieldSize,
            self.fieldSize,
        ))