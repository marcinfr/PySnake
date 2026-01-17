import pygame
import random
import math

class DefaultSnakeView:

    offsetRate = 1

    def init(self, screen, fieldSize):
        self.screen = screen
        self.fieldSize = fieldSize
        self.cachedSegemnts = {}

    def display(self, snake):
        for segmentNumber in range(len(snake.segments)):
            self.drawSegment(self.screen, snake, segmentNumber)
        self.drawSegment(self.screen, snake, 0)

    def drawSegment(self, surface, snake, segmentNumber):
        x = snake.segments[segmentNumber]['x']
        y = snake.segments[segmentNumber]['y']
        dir = snake.segments[segmentNumber]['dir']
        life = snake.life
        if life > 0:
            #nextSegment = False
            prevSegment = False
            isCornerSegment = False
            if segmentNumber == 0:
                segment = self.getHeadSegment(snake, segmentNumber) # head
                #nextSegment = snake.segments[segmentNumber + 1]
            elif segmentNumber == len(snake.segments) - 1:
                prevSegment = snake.segments[segmentNumber - 1]
                segment = self.getTailSegment(snake, segmentNumber) # tail
                dir = prevSegment['dir']
            else:
                prevSegment = snake.segments[segmentNumber - 1]
                #nextSegment = snake.segments[segmentNumber + 1]
                #if prevSegment['x'] == nextSegment['x']:
                #    segment = self.getStraightSegment(snake, segmentNumber)
                #elif prevSegment['y'] == nextSegment['y']:
                if dir == prevSegment['dir']:
                    segment = self.getStraightSegment(snake, segmentNumber)
                else:
                    segment = self.getCornerSegment(snake, segmentNumber)
                    isCornerSegment = True

            if snake.isFrozen:
                segment = self.getFrozenElement(snake, segmentNumber, segment)

            if isCornerSegment:
                prevDir = prevSegment['dir']
                if dir[0] < 0 and prevDir[1] > 0:
                    dir = (0,-1)
                elif dir[0] > 0 and prevDir[1] < 0:
                    dir = (0,1)
                elif dir[1] < 0 and prevDir[0] < 0:
                    dir = (1,0)
                elif dir[1] > 0 and prevDir[0] > 0:
                    dir = (-1,0)
            
            if (dir[0] < 0):
                segment = pygame.transform.rotate(segment, 180)
            elif (dir[1] < 0):
                segment = pygame.transform.rotate(segment, 90)
            elif (dir[1] > 0):
                segment = pygame.transform.rotate(segment, 270)

            if segmentNumber == 0 and snake.offsetRate < 1:
                offsetX = dir[0] * snake.offset * self.fieldSize
                offsetY = dir[1] * snake.offset * self.fieldSize
            #elif segmentNumber == len(snake.segments) - 1 and snake.offsetRate < 1:
            #    offsetX = 1 + (-1) * dir[0] * (1 - snake.offset) * self.fieldSize
            #    offsetY = 1 + (-1) * dir[1] * (1 - snake.offset) * self.fieldSize
            else:
                offsetX = 0
                offsetY = 0


            if (snake.life < 1):
                segment = pygame.transform.scale(segment, (self.fieldSize * snake.life, self.fieldSize * snake.life))

            px = x * self.fieldSize + self.fieldSize // 2 - offsetX
            py = y * self.fieldSize + self.fieldSize // 2 - offsetY
            rect = segment.get_rect(center=(px, py))

            surface.blit(
                segment, 
                rect
            )

    def getHeadSegment(self, snake, segmentNumber):
        return self.getStraightSegment(snake, segmentNumber)
    
    def getTailSegment(self, snake, segmentNumber):
        return self.getStraightSegment(snake, segmentNumber)

    def getStraightSegment(self, snake, segmentNumber):
        cacheId = 'straight-' + str(snake.id)
        if cacheId not in self.cachedSegemnts:
            fieldSize = math.ceil(self.fieldSize)
            surface = pygame.Surface((fieldSize, fieldSize))

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.8), (
                0,
                0,
                fieldSize,
                fieldSize,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.9), (
                0,
                fieldSize * 0.05,
                fieldSize,
                fieldSize - fieldSize * 0.1,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake), (
                0,
                fieldSize * 0.2,
                fieldSize,
                fieldSize - fieldSize * 0.4,
            ))

            self.cachedSegemnts[cacheId] = surface
        return self.cachedSegemnts[cacheId]
    
    def getCornerSegment(self, snake, segmentNumber):
        cacheId = 'corner-' + str(snake.id)
        if cacheId not in self.cachedSegemnts:
            fieldSize = math.ceil(self.fieldSize)
            surface = pygame.Surface((fieldSize, fieldSize), pygame.SRCALPHA)

            pygame.draw.circle(
                surface,
                self.getSnakeColor(snake, 0.8),
                (
                    fieldSize / 2,
                    fieldSize / 2
                ),
                fieldSize / 2
            )

            pygame.draw.circle(
                surface,
                self.getSnakeColor(snake, 0.9),
                (
                    fieldSize / 2,
                    fieldSize / 2
                ),
                fieldSize / 2 - fieldSize * 0.05
            )

            pygame.draw.circle(
                surface,
                self.getSnakeColor(snake),
                (
                    fieldSize / 2,
                    fieldSize / 2
                ),
                fieldSize / 2 - fieldSize * 0.2
            )

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.8), (
                0,
                0,
                fieldSize * 0.5,
                fieldSize,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.8), (
                0,
                fieldSize * 0.5,
                fieldSize,
                fieldSize,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.9), (
                0,
                fieldSize * 0.05,
                fieldSize * 0.5,
                fieldSize - fieldSize * 0.1,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.9), (
                fieldSize * 0.05,
                fieldSize * 0.5,
                fieldSize - fieldSize * 0.1,
                fieldSize,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake), (
                0,
                fieldSize * 0.2,
                fieldSize * 0.5,
                fieldSize - fieldSize * 0.4,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake), (
                fieldSize * 0.2,
                fieldSize * 0.5,
                fieldSize - fieldSize * 0.4,
                fieldSize,
            ))
            
            self.cachedSegemnts[cacheId] = surface
        return self.cachedSegemnts[cacheId]

    def getSnakeColor(self, snake, factor=1, transp = 255):
        color = snake.color
        return tuple(min(255, max(0, int(c * factor))) for c in color) + (transp,)
    
    def getFrozenElement(self, snake, segmentNumber, segment):

        cacheId = 'frozen-' + str((segmentNumber + snake.id) % 10)

        if cacheId not in self.cachedSegemnts:
            fieldSize = math.ceil(self.fieldSize)
            surface = pygame.Surface((fieldSize, fieldSize))
            pygame.draw.rect(surface, (255,255,255), (
                    0,
                    0,
                    fieldSize,
                    fieldSize,
                ))
            
            pygame.draw.rect(surface, (51,255,255), (
                    0 + fieldSize // 20,
                    0 + fieldSize // 20,
                    fieldSize - fieldSize // 20 * 2,
                    fieldSize - fieldSize // 20 * 2,
                ))

            for i in range(15):
                w1, w2 = random.sample(range(4), 2)

                p1 = self.randomWallPoint(fieldSize, w1)
                p2 = self.randomWallPoint(fieldSize, w2)

                pygame.draw.line(surface, 
                    "white", 
                    p1,
                    p2,
                    fieldSize // (20 * random.randint(1,3))
                )

            self.cachedSegemnts[cacheId] = surface
        
        return self.cachedSegemnts[cacheId]

    @staticmethod
    def randomWallPoint(x, wall):
        if wall == 0:      # góra
            return (random.randint(0, x), 0)
        elif wall == 1:    # prawo
            return (x, random.randint(0, x))
        elif wall == 2:    # dół
            return (random.randint(0, x), x)
        else:              # lewo
            return (0, random.randint(0, x))