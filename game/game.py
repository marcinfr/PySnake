import pygame
from game.boardView import BoardView
from game.snakeView import SnakeView
from game.snake import Snake

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        screenWidth, screenHeight = self.screen.get_size()
        maxWidth = screenWidth
        maxHeight = screenHeight
        self.fieldSize = min(maxWidth // width, maxHeight // height)
        surfaceWidth = self.fieldSize * width
        surfaceHeight = self.fieldSize * height
        self.gameSurface = pygame.Surface((surfaceWidth, surfaceHeight))
        self.boardView = BoardView(self.gameSurface, self.fieldSize)
        self.snakeView = SnakeView(self.gameSurface, self.fieldSize)
        self.snake = Snake([(5, 5), (5, 6), (5, 7)])

    def update(self, events):
        pass

    def display(self):
        self.boardView.display(self.board)
        self.snakeView.display(self.snake)
        posX = (self.screen.get_width() - self.gameSurface.get_width()) // 2
        self.screen.blit(self.gameSurface, (posX, 0))
