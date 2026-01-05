import pygame

class SpaceBoardView:

    COLOR_LIGHT = (170, 215, 81)
    COLOR_DARK = (162, 209, 73)

    def init(self, screen, fieldSize):
        self.screen = screen
        self.fieldSize = fieldSize
        self.background = None
        self.stars = []

    def display(self, board):
        if (self.background is None):
            width = len(board)
            height = len(board[0])
            self.background = pygame.Surface((self.fieldSize * width, self.fieldSize * height))
            self.background.fill("black")
        self.screen.blit(self.background, (0, 0))
    
    def displayFruits(self, fruits):
        for x, inner in fruits.items():
            for y, value in inner.items():
                self.drawFruit(x, y)

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