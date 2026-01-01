import pygame

class BoardView:

    COLOR_LIGHT = (170, 215, 81)
    COLOR_DARK = (162, 209, 73)

    def __init__(self, screen, fieldSize):
        self.screen = screen
        self.fieldSize = fieldSize
        self.background = None

    def display(self, board):
        if (self.background is None):
            width = len(board)
            height = len(board[0])
            self.background = pygame.Surface((self.fieldSize * width, self.fieldSize * height))
            for x, row in enumerate(board):
                for y, value in enumerate(row):
                    self.drawField(self.background, x, y)
        self.screen.blit(self.background, (0, 0))

    def displayFruits(self, fruits):
        for x, inner in fruits.items():
            for y, value in inner.items():
                self.drawFruit(x, y)

    def drawField(self, surface, x, y):
        if x % 2 == y % 2:
            color = self.COLOR_LIGHT
        else:
            color = self.COLOR_DARK
        pygame.draw.rect(surface, color, (
            x * self.fieldSize,
            y * self.fieldSize,
            self.fieldSize,
            self.fieldSize,
        ))

    def drawFruit(self, x, y):
        pygame.draw.circle(
            self.screen,
            (255, 0, 0),
            (
                (self.fieldSize // 2) + (self.fieldSize * x),
                (self.fieldSize // 2) + (self.fieldSize * y)
            ),
            self.fieldSize // 4
        )