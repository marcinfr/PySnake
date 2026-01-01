import pygame
from game.boardView import BoardView
from game.snakeView import SnakeView
from game.snake import Snake
from game.controllers.keyboard import Keyboard
from random import randrange
from collections import defaultdict

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.isRunning = False

    def start(self, width, height):
        self.isRunning = True

        self.board = [[0 for _ in range(height)] for _ in range(width)]
        self.fruits = defaultdict(dict)
        screenWidth, screenHeight = self.screen.get_size()
        maxWidth = screenWidth
        maxHeight = screenHeight

        print("Requested board size:", width, "x", height)
        print("Screen size:", screenWidth, "x", screenHeight)

        self.fieldSize = min(maxWidth // width, maxHeight // height)
        surfaceWidth = self.fieldSize * width
        surfaceHeight = self.fieldSize * height

        print("Game initialized with board size:", surfaceWidth, "x", surfaceHeight)

        self.gameSurface = pygame.Surface((surfaceWidth, surfaceHeight))
        self.boardView = BoardView(self.gameSurface, self.fieldSize)
        self.snakeView = SnakeView(self.gameSurface, self.fieldSize)
        self.snake = Snake(1, [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9)])
        self.keyboard = Keyboard(self.snake)
        self.addRandomFruit()

    def update(self):
        if self.snake.life == 1:
            self.snake.move(self)
        elif self.snake.life > 0:
            self.snake.die(self)
        else:
            self.isRunning = False

    def display(self):
        self.boardView.display(self.board)
        self.boardView.displayFruits(self.fruits)
        self.snakeView.display(self.snake)
        posX = (self.screen.get_width() - self.gameSurface.get_width()) // 2
        self.screen.blit(self.gameSurface, (posX, 0))

    def addRandomFruit(self):
        x = randrange(0, len(self.board))
        y = randrange(0, len(self.board[0]))
        print("new fruit:")
        print(x, y)
        if self.board[x][y] == 0:
            self.addFruit(x, y)
        else:
            self.addRandomFruit()

    def addFruit(self, x, y):
        self.fruits[x][y] = 1
        self.board[x][y] = -1

    def removeFruit(self, x, y):
        #if x in self.fruits and y in self.addFruitfruits[x]:
        del self.fruits[x][y]
        self.addRandomFruit()
        self.board[x][y] = 0
        