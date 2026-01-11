from game.boardView.classic import ClassicBoardView
import pygame

class RetroBoardView(ClassicBoardView):
    color1 = (168, 176, 153)
    color2 = (156, 163, 142)
    color3 = "black"

    def drawField(self, surface, x, y):
        pygame.draw.rect(surface, self.color2, (
            x * self.fieldSize,
            y * self.fieldSize,
            self.fieldSize,
            self.fieldSize,
        ))

        pygame.draw.rect(surface, self.color1, (
            x * self.fieldSize + self.fieldSize // 40,
            y * self.fieldSize + self.fieldSize // 40,
            self.fieldSize - self.fieldSize // 20,
            self.fieldSize - self.fieldSize // 20,
        ))

    def drawWall(self, surface, x, y):
        pygame.draw.rect(surface, self.color3, (
            x * self.fieldSize,
            y * self.fieldSize,
            self.fieldSize,
            self.fieldSize,
        ))

        pygame.draw.rect(surface, self.color1, (
            x * self.fieldSize + self.fieldSize // 20,
            y * self.fieldSize + self.fieldSize // 20,
            self.fieldSize - self.fieldSize // 10,
            self.fieldSize - self.fieldSize // 10,
        ))

        pygame.draw.rect(surface, self.color3, (
            x * self.fieldSize + self.fieldSize // 10,
            y * self.fieldSize + self.fieldSize // 10,
            self.fieldSize - self.fieldSize // 5,
            self.fieldSize - self.fieldSize // 5,
        ))

    def getNormalFruitSruface(self):
        surface = pygame.Surface((self.fieldSize, self.fieldSize), pygame.SRCALPHA)
        friutColor = (170, 34, 17)

        margin = surface.get_width() // 5
        
        pygame.draw.rect(surface, friutColor, (
            margin,
            margin,
            surface.get_width() - margin * 2,
            surface.get_height() - margin * 2,
        ))

        margin = surface.get_width() // 3

        pygame.draw.rect(surface, self.color1, (
            margin,
            margin,
            surface.get_width() - margin * 2,
            surface.get_height() - margin * 2,
        ))

        return surface