import pygame
from game.boardView.classic import ClassicBoardView
from random import randrange
from helpers.timer import Timer
import math

class SpaceBoardView(ClassicBoardView):

    COLOR_LIGHT = (170, 215, 81)
    COLOR_DARK = (162, 209, 73)

    def drawField(self, surface, x, y):
        pygame.draw.rect(surface, "black", (
            x * self.fieldSize,
            y * self.fieldSize,
            self.fieldSize,
            self.fieldSize,
        ))

    def getBackground(self, board):
        ClassicBoardView.getBackground(self, board)
        move = False
        if Timer().has_elapsed("stars", 0.02):
            move = True
            self.background.fill("black")
        for star in self.stars:
            if star[1] == 0:
                color = "white"
                speed = 2
            if star[1] == 1:
                color = (100,100,100)
                speed = 1
            pygame.draw.circle(
                self.background,
                color,
                (star[0]),
                1
            )
            if move:
                star[0][0] -= speed
                if star[0][0] < 0:
                    star[0][0] = self.background.get_width()
        return self.background
    
    def drawBackground(self, board):
        ClassicBoardView.drawBackground(self, board)
        self.stars = []
        for i in range(self.background.get_width() * self.background.get_height() // 100000):
            x = randrange(0, self.background.get_width())
            y = randrange(0, self.background.get_height())
            self.stars.append(([x, y], 0))
            x = randrange(0, self.background.get_width())
            y = randrange(0, self.background.get_height())
            self.stars.append(([x, y], 1))


    def getNormalFruitSruface(self, fruitData):
        surface = pygame.Surface((self.fieldSize, self.fieldSize), pygame.SRCALPHA)
        cx = self.fieldSize // 2
        cy = self.fieldSize // 2

        radius = self.fieldSize // 4
        points = []

        for i in range(10):
            angle = i * math.pi / 5  # 36 stopni
            r = radius if i % 2 == 0 else radius / 2
            x = cx + math.cos(angle - math.pi / 2) * r
            y = cy + math.sin(angle - math.pi / 2) * r
            points.append((x, y))


        pygame.draw.polygon(surface, "white", points)
        return surface
