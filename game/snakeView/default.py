import pygame

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
        x = snake.segments[segmentNumber][0]
        y = snake.segments[segmentNumber][1]
        dir = snake.segments[segmentNumber][2]
        life = snake.life
        if life > 0:
            nextSegment = False
            prevSegment = False
            isCornerSegment = False
            if segmentNumber == 0:
                segment = self.getHeadSegment(snake) # head
                nextSegment = snake.segments[segmentNumber + 1]
            elif segmentNumber == len(snake.segments) - 1:
                prevSegment = snake.segments[segmentNumber - 1]
                segment = self.getTailSegment(snake) # tail
                dir = prevSegment[2]
            else:
                prevSegment = snake.segments[segmentNumber - 1]
                nextSegment = snake.segments[segmentNumber + 1]
                if prevSegment[0] == nextSegment[0]:
                    segment = self.getStraightSegment(snake)
                elif prevSegment[1] == nextSegment[1]:
                    segment = self.getStraightSegment(snake)
                else:
                    segment = self.getCornerSegment(snake)
                    isCornerSegment = True

            if isCornerSegment:
                prevDir = prevSegment[2]
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

            if (snake.life < 1):
                segment = pygame.transform.scale(segment, (self.fieldSize * snake.life, self.fieldSize * snake.life))

            if segmentNumber == 0 and snake.offsetRate < 1:
                offsetX = dir[0] * snake.offset * self.fieldSize
                offsetY = dir[1] * snake.offset * self.fieldSize
            elif segmentNumber == len(snake.segments) - 1 and snake.offsetRate < 1:
                offsetX = 1 + (-1) * dir[0] * (1 - snake.offset) * self.fieldSize
                offsetY = 1 + (-1) * dir[1] * (1 - snake.offset) * self.fieldSize
            else:
                offsetX = 0
                offsetY = 0

            #pygame.draw.rect(surface, "red", (
            #    x * self.fieldSize + (self.fieldSize * (1 - snake.life) // 2),
            #    y * self.fieldSize + (self.fieldSize * (1 - snake.life) // 2),
            #    self.fieldSize,
            #    self.fieldSize
            #))

            surface.blit(
                segment, 
                (
                    x * self.fieldSize + (self.fieldSize * (1 - snake.life) // 2) - offsetX,
                    y * self.fieldSize + (self.fieldSize * (1 - snake.life) // 2) - offsetY,
                )
            )

    def getHeadSegment(self, snake):
        return self.getStraightSegment(snake)
    
    def getTailSegment(self, snake):
        return self.getStraightSegment(snake)

    def getStraightSegment(self, snake):
        cacheId = 'straight-' + str(snake.id)
        if cacheId not in self.cachedSegemnts:
            surface = pygame.Surface((self.fieldSize, self.fieldSize))

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.8), (
                0,
                0,
                self.fieldSize,
                self.fieldSize,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.9), (
                0,
                self.fieldSize * 0.05,
                self.fieldSize,
                self.fieldSize - self.fieldSize * 0.1,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake), (
                0,
                self.fieldSize * 0.2,
                self.fieldSize,
                self.fieldSize - self.fieldSize * 0.4,
            ))

            self.cachedSegemnts[cacheId] = surface
        return self.cachedSegemnts[cacheId]
    
    def getCornerSegment(self, snake):
        cacheId = 'corner-' + str(snake.id)
        if cacheId not in self.cachedSegemnts:
            surface = pygame.Surface((self.fieldSize, self.fieldSize), pygame.SRCALPHA)

            pygame.draw.circle(
                surface,
                self.getSnakeColor(snake, 0.8),
                (
                    self.fieldSize / 2,
                    self.fieldSize / 2
                ),
                self.fieldSize / 2
            )

            pygame.draw.circle(
                surface,
                self.getSnakeColor(snake, 0.9),
                (
                    self.fieldSize / 2,
                    self.fieldSize / 2
                ),
                self.fieldSize / 2 - self.fieldSize * 0.05
            )

            pygame.draw.circle(
                surface,
                self.getSnakeColor(snake),
                (
                    self.fieldSize / 2,
                    self.fieldSize / 2
                ),
                self.fieldSize / 2 - self.fieldSize * 0.2
            )

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.8), (
                0,
                0,
                self.fieldSize * 0.5,
                self.fieldSize,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.8), (
                0,
                self.fieldSize * 0.5,
                self.fieldSize,
                self.fieldSize,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.9), (
                0,
                self.fieldSize * 0.05,
                self.fieldSize * 0.5,
                self.fieldSize - self.fieldSize * 0.1,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake, 0.9), (
                self.fieldSize * 0.05,
                self.fieldSize * 0.5,
                self.fieldSize - self.fieldSize * 0.1,
                self.fieldSize,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake), (
                0,
                self.fieldSize * 0.2,
                self.fieldSize * 0.5,
                self.fieldSize - self.fieldSize * 0.4,
            ))

            pygame.draw.rect(surface, self.getSnakeColor(snake), (
                self.fieldSize * 0.2,
                self.fieldSize * 0.5,
                self.fieldSize - self.fieldSize * 0.4,
                self.fieldSize,
            ))
            
            self.cachedSegemnts[cacheId] = surface
        return self.cachedSegemnts[cacheId]

    def getSnakeColor(self, snake, factor=1):
        color = snake.color
        return tuple(min(255, max(0, int(c * factor))) for c in color)