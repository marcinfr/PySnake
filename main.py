import pygame
import sys
from helpers.events import Events
from game.game import Game

class Main:
    def __init__(self):
        self.events = Events()
        pygame.init()
        pygame.display.set_caption("Snake")
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1600, 1000))
        self.game = Game(self.screen, 30, 30)

    def exit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            Events.reset();
            if Events.QUIT:
                self.exit()
            self.game.update()
            self.game.display()
            pygame.display.flip()

main = Main();
main.run();