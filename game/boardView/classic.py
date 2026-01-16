import pygame
from game.fruits import Fruits
import math

from helpers.timer import Timer

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
            for y, data in inner.items():
                self.drawFruit(data, x, y)

    def drawField(self, surface, x, y):
        if x % 2 == y % 2:
            color = self.COLOR_LIGHT
        else:
            color = self.COLOR_DARK
        pygame.draw.rect(surface, color, (
            x * self.fieldSize,
            y * self.fieldSize,
            math.ceil(self.fieldSize),
            math.ceil(self.fieldSize),
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

    def drawFruit(self, fruitData, x, y):
        type = fruitData['type']
        surface = False
        if type == Fruits.FRUIT_TYPE_NORMAL:
            surface = self.getNormalFruitSruface(fruitData)
        elif type == Fruits.FRUIT_TYPE_FROZEN:
            surface = self.getFrozenFruitSruface()
        elif type == Fruits.FRUIT_TYPE_DARKNESS:
            surface = self.getDarknessFruitSruface()

        if 'lifeTime' in fruitData:
            surface = self.getSurfaceWithLifetime(surface, fruitData)

        if surface:
            offsetX = self.fieldSize - surface.get_width()
            offsetY = self.fieldSize - surface.get_height()
            self.screen.blit(
                surface, 
                (self.fieldSize * x + offsetX // 2, self.fieldSize * y + offsetY // 2)
            )
    
    def getNormalFruitSruface(self, fruitData):
        surface = pygame.Surface((self.fieldSize, self.fieldSize), pygame.SRCALPHA)
        color = (255, 0, 0)

        pygame.draw.circle(
            surface,
            color,
            (
                surface.get_width() // 2,
                surface.get_height() // 2
            ),
            self.fieldSize // 4
        )

        return surface
    
    def getSurfaceWithLifetime(self, surface, fruitData):
        elapsed = Timer.get_timestamp() - fruitData['createTime']
        lifeTime = fruitData['lifeTime']
        visibleParts = 4 - (elapsed / lifeTime * 4) // 1

        if visibleParts < 4:
            mask = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.rect(mask, (0, 0, 0, 220), (
                surface.get_width() // 2,
                0,
                surface.get_width() // 2,
                surface.get_height() // 2
            ))
            if visibleParts < 3:
                pygame.draw.rect(mask, (0, 0, 0, 220), (
                    surface.get_width() // 2,
                    surface.get_height() // 2,
                    self.fieldSize // 2,
                    self.fieldSize // 2
                ))
            if visibleParts < 2:
                pygame.draw.rect(mask, (0, 0, 0, 220), (
                    0,
                    surface.get_height() // 2,
                    self.fieldSize // 2,
                    self.fieldSize // 2
                ))

            surface.blit(
                mask,
                    (0, 0),
                    special_flags=pygame.BLEND_RGBA_SUB
                )
        return surface

    def getFrozenFruitSruface(self):
        surface = pygame.Surface((self.fieldSize // 2, self.fieldSize // 2), pygame.SRCALPHA)

        pygame.draw.rect(surface, (255,255,255), (
            0,
            0,
            surface.get_width(),
            surface.get_height(),
        ))
            
        margin = surface.get_width() // 10
        
        pygame.draw.rect(surface, (51,255,255), (
            margin,
            margin,
            surface.get_width() - margin * 2,
            surface.get_height() - margin * 2,
        ))
        
        return surface
    
    def getDarknessFruitSruface(self):
        surface = pygame.Surface((self.fieldSize // 2, self.fieldSize // 2), pygame.SRCALPHA)

        pygame.draw.rect(surface, (255,255,255), (
            0,
            0,
            surface.get_width(),
            surface.get_height(),
        ))
            
        margin = surface.get_width() // 10
        
        pygame.draw.rect(surface, (0,0,0), (
            margin,
            margin,
            surface.get_width() - margin * 2,
            surface.get_height() - margin * 2,
        ))
        
        return surface
 
    def displayDarkness(self, surface, snakes, darknessAlpha, color = (0,0,0)):
        darkness = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        darkness.fill((*color, darknessAlpha))

        visionRadius = self.fieldSize * 4.5

        if not hasattr(self, "vision_mask"):
            self.vision_mask = self.getDarknessVisionMask(visionRadius, 60)

        for snake in snakes:
            if snake.life > 0:
                head = snake.segments[0]

                x = math.ceil(head['x'] * self.fieldSize) + self.fieldSize // 2
                y = math.ceil(head['y'] * self.fieldSize) + self.fieldSize // 2

                darkness.blit(
                    self.vision_mask,
                    (x - visionRadius, y - visionRadius),
                    special_flags=pygame.BLEND_RGBA_SUB
                )

        surface.blit(darkness, (0,0))

    @staticmethod
    def getDarknessVisionMask(radius, softness):
        mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        for i in range(softness):
            alpha = int(255 * (i / softness))
            pygame.draw.circle(
                mask,
                (0, 0, 0, alpha),
                (radius, radius),
                radius - i
            )

        return mask