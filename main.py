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
        self.screen = pygame.display.set_mode((1200, 800))
        self.game = Game(self.screen, 50, 30)

    def exit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.events.reset();
            if self.events.QUIT:
                self.exit()
            self.game.update(self.events)
            self.game.display()
            pygame.display.flip()

main = Main();
main.run();