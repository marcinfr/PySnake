import pygame
from game.boardView import BoardView
from game.snakeView import SnakeView
from game.snake import Snake
from game.controllers.keyboard import Keyboard
from game.controllers.pad import Pad
from random import randrange
from collections import defaultdict
from helpers.events import Events
from helpers.timer import Timer
import math

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.isRunning = False
        Events.addEventListener("game-esc", "key_down_" + str(pygame.K_ESCAPE), self.pause)

    def start(self, width, height, players = None):
        self.pointsBarHeight = 80
        self.counterToStart = 3
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
        maxHeight = screenHeight - self.pointsBarHeight

        initPositions = [
            (3,3, (1,0)),
            (width-3,height-3, (-1,0)),
            (width-3,3, (0,1)),
            (3,height-3, (0,-1)),
        ]

        playersCounter = 0

        if not self.players:
            self.players['main'] = {
                'type': 'main',
                'color': 0
            }

        for player in self.players.values():
            if player['type'] == 'main':
                controller = Keyboard()
            if player['type'] == 'joystick':
                controller = Pad(player['joystick'])
            self.addSnake(initPositions[playersCounter], 3, controller, player['color'])
            playersCounter += 1

        print("Requested board size:", width, "x", height)
        print("Screen size:", screenWidth, "x", screenHeight)

        self.fieldSize = min(maxWidth // width, maxHeight // height)

        print( self.fieldSize)
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

    def isLevelEnd():
        pass

    def nextLevel():
        pass
    
    def addSnake(self, position, length, controller, color):
        if (len(position) > 2):
            direction = position[2]
        else:
            direction = (1,0)

        segments = [(position[0] - (i * direction[0]), position[1] - (i * direction[1])) for i in range(length)]
        print(segments)
        snake = Snake(len(self.snakes), segments, color)
        snake.setDirection(direction)
        if controller:
            controller.setSnake(snake)
        self.snakes.append(snake)

    def update(self):
        isAliveSnake = False
        if self.counterToStart > 0:
            if Timer().has_elapsed("game-start-counter", 0.1):
                if math.ceil(self.counterToStart) - self.counterToStart < 0.1:
                    sound = pygame.mixer.Sound("assets/counter1.wav")
                    sound.play()
                self.counterToStart -= 0.1
        else:
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
        self.displayCounter()    

        self.screen.blit(self.gameSurface, (posX, self.pointsBarHeight))

    def displayCounter(self):
        if (self.counterToStart <= 0):
            return
        font = pygame.font.Font(None, 300)
        text = font.render(str(math.ceil(self.counterToStart)), True, "White")
        target_height = self.screen.get_height() * (self.counterToStart % 1)
        scale = target_height / text.get_height()
        new_width = int(text.get_width() * scale)
        text = pygame.transform.scale(text, (new_width, target_height))
        textRect = text.get_rect()
        centerX = self.gameSurface.get_width() / 2
        centerY = self.gameSurface.get_height() / 2
        textRect.center = (centerX, centerY)
        self.gameSurface.blit(text, textRect)

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
        