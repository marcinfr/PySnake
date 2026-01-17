from random import random
import pygame
from helpers.timer import Timer
import random

class Fruits:
    FRUIT_TYPE_NORMAL = 1
    FRUIT_TYPE_FROZEN = 2
    FRUIT_TYPE_DARKNESS = 3
    FRUIT_TYPE_WALL = 4

    @staticmethod
    def processFruits(game):
        for x, inner in game.fruits.items():
            for y, data in inner.items():
                Fruits.processFruit(game, data, x, y)

    @staticmethod
    def processFruit(game, fruitData, posX, posY):
        if 'lifeTime' in fruitData:
            elapsed = Timer.get_timestamp() - fruitData['createTime']
            lifeTime = fruitData['lifeTime']
            if (elapsed >= lifeTime):
                game.removeFruit(posX, posY)

    @staticmethod
    def getFruitData(type, data = {}):
        fruitData = {
            'type': type
        }
        if 'lifeTime' in data:
            fruitData['lifeTime'] = data['lifeTime']  # seconds
            fruitData['createTime'] = Timer.get_timestamp()

        if type == Fruits.FRUIT_TYPE_WALL:
            fruitData['wall'] = [(-1,0),(0,0),(1,0),(0,-1),(0,1)]

        return fruitData

    @staticmethod
    def onRemove(game, x, y, fruitData):
        type = fruitData['type']
        if type == Fruits.FRUIT_TYPE_WALL:
            for wall in fruitData['wall']:
                x1 = x + wall[0]
                y1 = y + wall[1]
                if 0 <= x1 < len(game.board) and 0 <= y1 < len(game.board[0]):
                    if game.board[x1][y1]['moveable'] == True \
                        and game.board[x1][y1]['type'] == None \
                        and not game.board[x1][y1]['has_fruit']:
                        game.addWall(x1, y1)
        if type == Fruits.FRUIT_TYPE_NORMAL:
            if random.randint(0, 2) == 0:
                game.addRandomFruit(Fruits.FRUIT_TYPE_NORMAL, {'lifeTime': 4})
            else:
                game.addRandomFruit(Fruits.FRUIT_TYPE_NORMAL)

    @staticmethod
    def onPick(game, snake, fruitData):
        type = fruitData['type']
        sound = False
        head_x = snake.segments[0]['x']
        head_y = snake.segments[0]['y']

        points = 0
        notification = False
        font = pygame.font.SysFont(None, round(game.fieldSize))
        
        if type == Fruits.FRUIT_TYPE_NORMAL:
            points = 1
            notification = font.render("+" + str(points), True, (255, 255, 255))

        if type == Fruits.FRUIT_TYPE_FROZEN:
            sound = pygame.mixer.Sound("assets/freezing1.mp3")
            notification = font.render("Stop!!!", True, (51,255,255))
            for s in game.snakes:
                if s.id != snake.id:
                    s.freeze(5)

        if type == Fruits.FRUIT_TYPE_DARKNESS:
            notification = font.render("Ciemność", True, (0, 0, 0))
            sound = pygame.mixer.Sound("assets/darkness1.wav")
            game.darknessFactor = 20

        game.fruits[head_x][head_y]['wall'] = []


        if (notification):
            game.boardNotification.addNotification(
                (head_x * game.fieldSize + game.fieldSize // 2,head_y * game.fieldSize), 
                notification, 
                1
            )

        snake.totalPoints += points

        if not sound:
            sound = pygame.mixer.Sound("assets/pick1.wav")
            
        sound.play()