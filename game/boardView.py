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
            width = len(board[0])
            height = len(board)
            self.background = pygame.Surface((self.fieldSize * width, self.fieldSize * height))
            for y, row in enumerate(board):
                for x, value in enumerate(row):
                    self.drawField(self.background, x, y)
        self.screen.blit(self.background, (0, 0))

    def drawField(self, surface, x, y):
        if x % 2 == y % 2:
            color = self.COLOR_LIGHT
            dots_color = self.COLOR_DARK
        else:
            color = self.COLOR_DARK
            dots_color = self.COLOR_LIGHT
        pygame.draw.rect(surface, color, (
            x * self.fieldSize,
            y * self.fieldSize,
            self.fieldSize,
            self.fieldSize,
        ))