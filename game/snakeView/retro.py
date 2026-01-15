from game.snakeView.default import DefaultSnakeView
import pygame
from helpers.timer import Timer
import math

class RetroSnakeView(DefaultSnakeView):

    #def display(self, snake):
        #self.nextFrame = False
        #if Timer.has_elapsed('restro_snake_anim_' + str(snake.id), 0.1):
        #    self.nextFrame = True
        #return DefaultSnakeView.display(self, snake)

    def getStraightSegment(self, snake, segmentNumber):
        cacheId = 'straight-' + str(snake.id)
        
        #if 'segment_size' not in  snake.segments[segmentNumber]:
        #    snake.segments[segmentNumber]['segment_size'] = 0.4

        #if self.nextFrame and not snake.isFrozen:
        #    snake.segments[segmentNumber]['segment_size'] += 0.05

        #if snake.segments[segmentNumber]['segment_size'] >= 1:
        #    snake.segments[segmentNumber]['segment_size'] = 1

        if cacheId not in self.cachedSegemnts:
            self.cachedSegemnts[cacheId] = self.getRetroSegment(snake.color)
        
        #scale =  snake.segments[segmentNumber]['segment_size']

        surface = self.cachedSegemnts[cacheId]
        #surface = pygame.transform.scale(surface, (surface.get_width() * scale, surface.get_height() * scale))

        return surface
    
    def getFrozenElement(self, snake, segmentNumber, segment):
        cacheId = 'frozen-' + str(snake.id)
        if cacheId not in self.cachedSegemnts:
            self.cachedSegemnts[cacheId] = self.getRetroSegment((156, 163, 142))
        return self.cachedSegemnts[cacheId]

    
    def getHeadSegment(self, snake, segmentNumber):
        return self.getStraightSegment(snake, segmentNumber)
    
    def getTailSegment(self, snake, segmentNumber):
        return self.getStraightSegment(snake, segmentNumber)
    
    def getCornerSegment(self, snake, segmentNumber):
        return self.getStraightSegment(snake, segmentNumber)
    
    def getRetroSegment(self, color):
        fieldSize = math.ceil(self.fieldSize)
        surface = pygame.Surface((fieldSize, fieldSize), pygame.SRCALPHA)

        margin = self.fieldSize // 4
        pygame.draw.rect(surface, color, (
            margin,
            margin,
            fieldSize - margin * 2,
            fieldSize - margin * 2,
        ))

        lineSize = fieldSize // 5
        pygame.draw.line(
            surface, 
            color,
            (0, 0),
            (0, fieldSize),
            lineSize
        )

        pygame.draw.line(
            surface, 
            color,
            (fieldSize, 0),
            (fieldSize, fieldSize),
            lineSize
        )

        pygame.draw.line(
            surface, 
            color,
            (0, 0),
            (fieldSize, 0),
            lineSize
        )

        pygame.draw.line(
            surface, 
            color,
            (0, fieldSize),
            (fieldSize, fieldSize),
            lineSize
        )
    
        return surface