import pygame

class ClassicBoardView:

    COLOR_LIGHT = (170, 215, 81)
    COLOR_DARK = (162, 209, 73)

    def init(self, screen, fieldSize):
        self.screen = screen
        self.fieldSize = fieldSize
        self.background = None
        self.topLayer = None

    def display(self, board):
        self.screen.blit(self.getBackground(board), (0, 0))
        self.screen.blit(self.getTopLayer(board), (0, 0))

    def getBackground(self, board):
        if (self.background is None):
            width = len(board)
            height = len(board[0])
            self.background = pygame.Surface((self.fieldSize * width, self.fieldSize * height))
            self.drawBackground(board)
        return self.background
    
    def getTopLayer(self, board):
        if (self.topLayer is None):
            width = len(board)
            height = len(board[0])
            self.topLayer = pygame.Surface((self.fieldSize * width, self.fieldSize * height), pygame.SRCALPHA)
            self.drawTopLayer(board)
        return self.topLayer
    
    def drawTopLayer(self, board):
        for x, row in enumerate(board):
            for y, value in enumerate(row):
                if (value == 2):
                    self.drawWall(self.topLayer, x, y)

    def drawBackground(self, board):
        for x, row in enumerate(board):
                for y, value in enumerate(row):
                    self.drawField(self.background, x, y)

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

    def drawWall(self, surface, x, y):
        pygame.draw.polygon(surface, "white", 
            [
                (x * self.fieldSize, y * self.fieldSize),
                (x * self.fieldSize + self.fieldSize, y * self.fieldSize),
                (x * self.fieldSize, y * self.fieldSize + self.fieldSize),
            ]
        )
        pygame.draw.polygon(surface, (20,20,20), 
            [
                (x * self.fieldSize + self.fieldSize, y * self.fieldSize + self.fieldSize),
                (x * self.fieldSize + self.fieldSize, y * self.fieldSize),
                (x * self.fieldSize, y * self.fieldSize + self.fieldSize),
            ]
        )
        pygame.draw.rect(surface, (150,150,150), (
            x * self.fieldSize + self.fieldSize * 0.2,
            y * self.fieldSize + self.fieldSize * 0.2,
            self.fieldSize - self.fieldSize * 0.2 * 2,
            self.fieldSize - self.fieldSize * 0.2 * 2,
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