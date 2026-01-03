import pygame
from game.boardView import BoardView
from game.snakeView import SnakeView
from game.snake import Snake
from game.controllers.keyboard import Keyboard
from game.controllers.pad import Pad
from random import randrange
from collections import defaultdict
from helpers.events import Events

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.isRunning = False
        Events.addEventListener("game-esc", "key_down_" + str(pygame.K_ESCAPE), self.pause)

    def start(self, width, height, players = None):
        self.players = players
        self.width = width
        self.height = height
        self.snakes = []
        self.isRunning = True
        self.isEndGame = False
        self.board = [[0 for _ in range(height)] for _ in range(width)]
        self.fruits = defaultdict(dict)
        screenWidth, screenHeight = self.screen.get_size()
        maxWidth = screenWidth
        maxHeight = screenHeight

        playersCounter = 1
        self.addSnake((playersCounter * 3, 1), 3, Keyboard())
        for player in self.players.values():
            if player['type'] == 'joystick':
                joystick = player['joystick']
                self.addSnake((playersCounter * 3,playersCounter * 3), 3, Pad(joystick))
                playersCounter += 1

        print("Requested board size:", width, "x", height)
        print("Screen size:", screenWidth, "x", screenHeight)

        self.fieldSize = min(maxWidth // width, maxHeight // height)
        surfaceWidth = self.fieldSize * width
        surfaceHeight = self.fieldSize * height

        print("Game initialized with board size:", surfaceWidth, "x", surfaceHeight)

        self.gameSurface = pygame.Surface((surfaceWidth, surfaceHeight))
        self.boardView = BoardView(self.gameSurface, self.fieldSize)
        self.snakeView = SnakeView(self.gameSurface, self.fieldSize)
        #self.snake = Snake(1, [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9)])
        #self.keyboard = Keyboard()
        #self.keyboard.setSnake(self.snake)
        self.addRandomFruit()
    
    def addSnake(self, headPosition, length, controller):
        segments = [(headPosition[0], headPosition[1] + i) for i in range(length)]
        snake = Snake(len(self.snakes), segments)
        if controller:
            controller.setSnake(snake)
        self.snakes.append(snake)

    def update(self):
        isAliveSnake = False
        for snake in self.snakes:
            if snake.life > 0:
                isAliveSnake = True
            if snake.life == 1:
                snake.move(self)
            elif snake.life > 0:
                snake.die(self)

        if not isAliveSnake:
            #self.start(self.width, self.height, self.players)
            self.stop()

    def stop(self):
        self.isRunning = False
        self.isEndGame = True

    def pause(self):
        self.isRunning = False

    def unPause(self):
        self.isRunning = True

    def display(self):
        self.screen.fill((0, 0, 0))
        self.boardView.display(self.board)
        self.boardView.displayFruits(self.fruits)
        for snake in self.snakes:
            self.snakeView.display(snake)
        posX = (self.screen.get_width() - self.gameSurface.get_width()) // 2
        self.screen.blit(self.gameSurface, (posX, 0))

    def addRandomFruit(self):
        x = randrange(0, len(self.board))
        y = randrange(0, len(self.board[0]))
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
        