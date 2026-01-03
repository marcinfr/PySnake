import pygame

class SnakeView:
    def __init__(self, screen, fieldSize):
        self.screen = screen
        self.fieldSize = fieldSize

    def display(self, snake):
        for segmentNumber in range(len(snake.segments)):
            self.drawSegment(self.screen, snake, segmentNumber)

    def drawSegment(self, surface, snake, segmentNumber):
        x = snake.segments[segmentNumber][0]
        y = snake.segments[segmentNumber][1]
        life = snake.life
        if life > 0:
            pygame.draw.rect(surface, snake.color, (
                x * self.fieldSize + (self.fieldSize * (1 - snake.life) // 2),
                y * self.fieldSize + (self.fieldSize * (1 - snake.life) // 2),
                self.fieldSize * snake.life,
                self.fieldSize * snake.life,
            ))

            #pygame.draw.line(surface, "black", (x * self.fieldSize,y * self.fieldSize),  ((x + 1) * self.fieldSize,y * self.fieldSize), 2)
            #pygame.draw.line(surface, "black", (x * self.fieldSize,y * self.fieldSize),  (x * self.fieldSize,(y + 1) * self.fieldSize), 2)
            #pygame.draw.line(surface, "black", ((x+1) * self.fieldSize,y * self.fieldSize),  ((x+1) * self.fieldSize,(y + 1) * self.fieldSize), 2)
            #pygame.draw.line(surface, "black", (x * self.fieldSize,(y+1) * self.fieldSize),  ((x+1) * self.fieldSize,(y + 1) * self.fieldSize), 2)