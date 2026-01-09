from game.snakeView.default import DefaultSnakeView
import pygame
import math

class RocketSnakeView(DefaultSnakeView):

    offsetRate = 0.3

    def display(self, snake):
        freq = 4
        t = pygame.time.get_ticks() / 1000.0  
        self.alpha = int(200 + 30 * math.sin(2 * math.pi * freq * t))
        DefaultSnakeView.display(self, snake)

    def getHeadSegment(self, snake, segmentNumber):
        cacheId = 'head-' + str(snake.id)
        if cacheId not in self.cachedSegemnts:
            surface = pygame.Surface((self.fieldSize * 1.5, self.fieldSize * 1.5), pygame.SRCALPHA)
            image = pygame.image.load('assets/rocket1.png')
            image = image.convert_alpha()
            width, height = image.get_size()

            for y in range(height):
                for x in range(width):
                    current_pixel = image.get_at((x, y))
                    if current_pixel[0] < 50 and current_pixel[1] < 50 and current_pixel[2] < 50 and current_pixel[3] > 0:
                        image.set_at((x, y), snake.color)

            image = pygame.transform.scale(image, surface.get_size())
            image = pygame.transform.rotate(image, -90)
            surface.blit(image, (0, 0))
            self.cachedSegemnts[cacheId] = surface
        return self.cachedSegemnts[cacheId]
    
    def getStraightSegment(self, snake, segmentNumber):
        alpha = self.alpha - 20 * 4 // min((max(len(snake.segments) - segmentNumber, 1), 4))
        surface = pygame.Surface((self.fieldSize, self.fieldSize), pygame.SRCALPHA)

        pygame.draw.line(
            surface, 
            self.getSnakeColor(snake, 0.5, alpha),
            (0, self.fieldSize // 2),
            (self.fieldSize, self.fieldSize // 2),
            self.fieldSize // 2
        )

        pygame.draw.line(
            surface, 
            self.getSnakeColor(snake, 1.2 , alpha), 
            (0, self.fieldSize // 2),
            (self.fieldSize, self.fieldSize // 2),
            self.fieldSize // 10
)
        return surface
    
    def getCornerSegment(self, snake, segmentNumber):
        alpha = self.alpha - 20 * 4 // min((max(len(snake.segments) - segmentNumber, 1), 4))
        surface = pygame.Surface((self.fieldSize, self.fieldSize), pygame.SRCALPHA)
        width = self.fieldSize / 2
        pygame.draw.circle(
            surface, 
            self.getSnakeColor(snake, 0.5, alpha), 
            (0, self.fieldSize), (self.fieldSize + width) // 2, 
            round(width)
        )
        width = self.fieldSize / 10
        pygame.draw.circle(
            surface, 
            self.getSnakeColor(snake, 1.2, alpha), 
            (0, self.fieldSize), 
            (self.fieldSize + width) // 2, 
            round(width)
        )

        return surface