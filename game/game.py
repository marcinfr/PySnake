import pygame
from game.snake import Snake
from game.controllers.keyboard import Keyboard
from game.controllers.pad import Pad
import random
from collections import defaultdict
from helpers.events import Events
from helpers.timer import Timer
import math
from game.notifications import Notifications
from game.fruits import Fruits

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.isRunning = False
        self.levelProvider = None
        self.players = []
        Events.addEventListener("game-esc", "key_down_" + str(pygame.K_ESCAPE), self.pause)

    def start(self, data = {}):
        self.pointsBarHeight = 80
        self.currentLevel = 0
        self.players = data['players']
        self.settings = data['settings']
        self.levelProvider = self.settings['level_provider']

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
    
    def getBoard(self, map):
        width = map['mapSize'][0]
        height = map['mapSize'][1]
        board = [[0 for _ in range(height)] for _ in range(width)]
        walls = self.map['walls']
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
                board[x1][y1] = 2
                if x1 == x2 and y1 == y2:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy
        return board

    
    def nextLevel(self):
        self.currentLevel += 1
        self.levelProvider.initLevel(self)

        self.width = self.map['mapSize'][0]
        self.height = self.map['mapSize'][1]

        pygame.mixer.stop()
        if self.levelProvider.displayLevel:
            self.counterToStart = 4
        else:
            self.counterToStart = 3
        self.isRunning = True
        self.isEndGame = False
        self.board = self.getBoard(self.map)
        self.fruits = defaultdict(dict)
        screenWidth, screenHeight = self.screen.get_size()
        maxWidth = screenWidth
        maxHeight = screenHeight - self.pointsBarHeight
        print("Requested board size:", self.width, "x", self.height)
        print("Screen size:", screenWidth, "x", screenHeight)
        self.fieldSize = min(maxWidth / self.width, maxHeight / self.height)
        surfaceWidth = self.fieldSize * self.width
        surfaceHeight = self.fieldSize * self.height
        print("Game initialized with board size:", surfaceWidth, "x", surfaceHeight)
        self.gameSurface = pygame.Surface((surfaceWidth, surfaceHeight))
        self.boardView = self.theme['boardView']
        self.boardView.init(self.gameSurface, self.fieldSize)
        self.snakeView = self.theme['snakeView']
        self.snakeView.init(self.gameSurface, self.fieldSize)
        self.boardNotification = Notifications(self.gameSurface)
        self.darkness = 0
        self.darknessFactor = 0

        snakeLength = self.map['snakeLenght']
        startPositions = self.map['startPositions']

        self.aliveSnakes = 0
        for snakeNumber, snake in enumerate(self.snakes):
            position = startPositions[snakeNumber][0]
            direction = startPositions[snakeNumber][1]
            snake.segments = [{'x': position[0] - (i * direction[0]), 'y': position[1] - (i * direction[1]), 'dir': direction} for i in range(snakeLength)]
            snake.setDirection(direction)
            snake.life = 1
            snake.offsetRate = self.snakeView.offsetRate
            snake.isFrozen = False
            self.aliveSnakes += 1

        self.addRandomFruit()
        #self.addRandomFruit(Fruits.FRUIT_TYPE_FROZEN)
        #self.addRandomFruit(Fruits.FRUIT_TYPE_DARKNESS)

    
    def addSnake(self, controller, color):
        snake = Snake(len(self.snakes), [], color)
        if controller:
            controller.setSnake(snake)
        self.snakes.append(snake)

    def update(self):
        Timer.tick()
        isAliveSnake = False
        if self.counterToStart == 0:
            self.aliveSnakes = 0
            for snake in self.snakes:
                if snake.life > 0:
                    isAliveSnake = True
                    self.aliveSnakes += 1
                if snake.life == 1:
                    snake.move(self)
                elif snake.life > 0:
                    snake.die(self)

            if self.levelProvider.isLevelFinished(self):
                self.nextLevel();
            elif not isAliveSnake:
                #self.start(self.players)
                self.stop()

            if Timer().has_elapsed("spacial-fruit", 2):
                if random.randint(0, 10) == 0:
                    self.addRandomFruit(Fruits.FRUIT_TYPE_FROZEN)
                if random.randint(0, 10) == 0:
                    self.addRandomFruit(Fruits.FRUIT_TYPE_DARKNESS)
        self.prcessDarkness()
        self.boardNotification.process()


    def stop(self):
        self.isRunning = False
        self.isEndGame = True

    def pause(self):
        Timer.pause()
        self.isRunning = False

    def unPause(self):
        self.isRunning = True

    def display(self):
        self.screen.fill((0, 0, 0))
        self.boardView.display(self.board)
        self.boardView.displayFruits(self.fruits)
        for snake in self.snakes:
            self.snakeView.display(snake)

        self.boardView.displayDarkness(self.gameSurface, self.snakes, self.darkness)

        self.displayCounter()
        self.displayPoints()
        posX = (self.screen.get_width() - self.gameSurface.get_width()) // 2
        self.boardNotification.display()
        self.screen.blit(self.gameSurface, (posX, self.pointsBarHeight))


    def prcessDarkness(self):
        if self.darknessFactor == 0 and self.darkness == 0:
            return
        
        if self.darknessFactor != 0 and (self.darkness == 0 or Timer.has_elapsed('game.darkness', 0.1)):
            self.darkness += self.darknessFactor

        if self.darkness <= 0:
            self.darkness = 0
            self.darknessFactor = 0
            Timer.remove('game.darkness.time')
        elif self.darkness >= 255:
            self.darkness = 255
            self.darknessFactor = 0
            if Timer.has_elapsed('game.darkness.time', 3):
                sound = pygame.mixer.Sound("assets/darkness1.wav")
                sound.play()
                self.darknessFactor = -20

        

    def displayCounter(self):
        if self.counterToStart > 0 and Timer().has_elapsed("game-start-counter", 0.1):
            if math.ceil(self.counterToStart) - self.counterToStart < 0.1:
                if self.counterToStart > 3:
                    sound = pygame.mixer.Sound("assets/level1.wav")
                else:
                    sound = pygame.mixer.Sound("assets/counter1.wav")
                sound.play()
            self.counterToStart -= 0.1

        if (self.counterToStart <= 0):
            self.counterToStart = 0
            return

        font = pygame.font.Font(None, 300)
        text = font.render(str(math.ceil(self.counterToStart)), True, "White")

        if self.counterToStart > 3:
            font = pygame.font.Font(None, 300)
            text = font.render("Level " + str(self.currentLevel), True, "White")
        else:
            target_height = self.screen.get_height() * (self.counterToStart % 1)
            scale = target_height / text.get_height()
            new_width = int(text.get_width() * scale)
            text = pygame.transform.scale(text, (new_width, target_height))

        if self.counterToStart % 1 < 0.5:
            alpha = 255  * min((self.counterToStart * 2 % 1), 1)
            text.set_alpha(alpha)

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
            text = str(snake.totalPoints)
            if self.levelProvider.pointsToWin:
                text += " / " + str(self.levelProvider.pointsToWin)
            text = font.render(text, True, "White")
            self.screen.blit(text, (snakeNumber * 200 + 70, 30))

    def addRandomFruit(self, type = Fruits.FRUIT_TYPE_NORMAL):
        x = random.randrange(0, len(self.board))
        y = random.randrange(0, len(self.board[0]))
        if self.board[x][y] == 0:
            self.addFruit(x, y, type)
        else:
            self.addRandomFruit(type)

    def addFruit(self, x, y, type = Fruits.FRUIT_TYPE_NORMAL):
        self.fruits[x][y] = type
        self.board[x][y] = -1

    def removeFruit(self, x, y):
        #if x in self.fruits and y in self.addFruitfruits[x]:
        type = self.fruits[x][y]
        del self.fruits[x][y]
        if type == Fruits.FRUIT_TYPE_NORMAL:
            self.addRandomFruit()
        self.board[x][y] = 0
        
    def onSnakeDie(self, snake):
        sound = pygame.mixer.Sound("assets/dead1.wav")
        sound.play()

    def onFruitPick(self, snake):
        head_x = snake.segments[0]['x']
        head_y = snake.segments[0]['y']
        fruitType = self.fruits[head_x][head_y]
        sound = False

        points = 0
        notification = False
        font = pygame.font.SysFont(None, round(self.fieldSize))
        
        if fruitType == Fruits.FRUIT_TYPE_NORMAL:
            points = 1
            sound = pygame.mixer.Sound("assets/pick1.wav")
            notification = font.render("+" + str(points), True, (255, 255, 255))


        if fruitType == Fruits.FRUIT_TYPE_FROZEN:
            sound = pygame.mixer.Sound("assets/freezing1.mp3")
            notification = font.render("Stop!!!", True, (51,255,255))
            for s in self.snakes:
                if s.id != snake.id:
                    s.freeze(5)

        if fruitType == Fruits.FRUIT_TYPE_DARKNESS:
            notification = font.render("Ciemność", True, (0, 0, 0))
            sound = pygame.mixer.Sound("assets/darkness1.wav")
            self.darknessFactor = 20


        if (notification):
            self.boardNotification.addNotification(
                (head_x * self.fieldSize + self.fieldSize // 2,head_y * self.fieldSize), 
                notification, 
                1
            )

        snake.totalPoints += points

        if sound:
            sound.play()