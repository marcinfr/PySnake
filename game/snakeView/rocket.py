from game.snakeView.default import DefaultSnakeView
import pygame

class RocketSnakeView(DefaultSnakeView):

    offsetRate = 0.3

    def getHeadSegment(self, snake):
        surface = pygame.Surface((self.fieldSize, self.fieldSize))
        image = pygame.image.load('assets/rocket1.png')
        image = image.convert_alpha()
        width, height = image.get_size()

        for y in range(height):
            for x in range(width):
                current_pixel = image.get_at((x, y))
                if current_pixel[0] < 50 and current_pixel[1] < 50 and current_pixel[2] < 50 and current_pixel[3] > 0:
                    image.set_at((x, y), snake.color)

        image = pygame.transform.scale(image, (self.fieldSize, self.fieldSize))
        image = pygame.transform.rotate(image, -90)
        surface.blit(image, (0, 0))
        return surface