import pygame
from game.levels import Levels
from game.snakeView import SnakeView
from game.snake import Snake
from game.controllers.keyboard import Keyboard
from game.controllers.pad import Pad
from random import randrange
from collections import defaultdict
from helpers.events import Events
from helpers.timer import Timer
import math
from game.boardView.classic import ClassicBoardView

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.isRunning = False
        self.players = []
        Events.addEventListener("game-esc", "key_down_" + str(pygame.K_ESCAPE), self.pause)

    def start(self, players = []):
        self.pointsBarHeight = 80
        self.players = players

        if not self.players:
            self.players['main'] = {
                'type': 'main',
                'color': 0
            }

        #self.players['test'] = {
        #    'type': 'test',
        #    'color': 2
        #}

        self.snakes = []

        for player in self.players.values():
            if player['type'] == 'main':
                controller = Keyboard()
            elif player['type'] == 'joystick':
                controller = Pad(player['joystick'])
            else:
                controller = None
            self.addSnake(controller, player['color'])

        self.nextLevel();


    def isLevelEnd(self):
        if len(self.snakes) > 1 and self.aliveSnakes < 2:
            return True
        return False

    def nextLevel(self):
        self.level = Levels.getRandomLevel()
        self.width = self.level['mapSize'][0]
        self.height = self.level['mapSize'][1]

        self.counterToStart = 3
        self.isRunning = True
        self.isEndGame = False
        self.board = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.fruits = defaultdict(dict)
        screenWidth, screenHeight = self.screen.get_size()
        maxWidth = screenWidth
        maxHeight = screenHeight - self.pointsBarHeight
        print("Requested board size:", self.width, "x", self.height)
        print("Screen size:", screenWidth, "x", screenHeight)
        self.fieldSize = min(maxWidth // self.width, maxHeight // self.height)
        surfaceWidth = self.fieldSize * self.width
        surfaceHeight = self.fieldSize * self.height
        print("Game initialized with board size:", surfaceWidth, "x", surfaceHeight)
        self.gameSurface = pygame.Surface((surfaceWidth, surfaceHeight))
        self.boardView = ClassicBoardView()
        self.boardView.init(self.gameSurface, self.fieldSize)
        self.snakeView = SnakeView(self.gameSurface, self.fieldSize)

        snakeLength = 10 #self.level['snakeLenght']
        startPositions = self.level['startPositions']
        walls = self.level['walls']
        for wall in walls:
            x1 = wall[0][0]
            y1 = wall[0][1]
            x2 = wall[1][0]
            y2 = wall[1][1]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy
            while True:
                self.board[x1][y1] = 2
                if x1 == x2 and y1 == y2:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy

        self.aliveSnakes = 0
        for snakeNumber, snake in enumerate(self.snakes):
            position = startPositions[snakeNumber][0]
            direction = startPositions[snakeNumber][1]
            snake.segments = [(position[0] - (i * direction[0]), position[1] - (i * direction[1])) for i in range(snakeLength)]
            snake.setDirection(direction)
            snake.life = 1
            self.aliveSnakes += 1

        self.addRandomFruit()

    
    def addSnake(self, controller, color):
        snake = Snake(len(self.snakes), [], color)
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
            self.aliveSnakes = 0
            for snake in self.snakes:
                if snake.life > 0:
                    isAliveSnake = True
                    self.aliveSnakes += 1
                if snake.life == 1:
                    snake.move(self)
                elif snake.life > 0:
                    snake.die(self)

            if self.isLevelEnd():
                self.nextLevel();
            elif not isAliveSnake:
                #self.start(self.players)
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
        self.displayCounter()
        self.displayPoints()
        posX = (self.screen.get_width() - self.gameSurface.get_width()) // 2
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

    def displayPoints(self):
        for snakeNumber, snake in enumerate(self.snakes):
            pygame.draw.rect(self.screen, snake.color, (
                snakeNumber * 200 + 20,
                20,
                40,
                40,
            ))
            font = pygame.font.Font(None, 40)
            text = font.render(str(snake.totalPoints), True, "White")
            self.screen.blit(text, (snakeNumber * 200 + 70, 30))

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
        
    def onSnakeDie(self, snake):
        sound = pygame.mixer.Sound("assets/dead1.wav")
        sound.play()

    def onFruitPick(self, sneak):
        sound = pygame.mixer.Sound("assets/pick1.wav")
        sound.play()
        sneak.totalPoints += 1