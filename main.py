import pygame
import sys
from helpers.events import Events
from game.game import Game
from menu.menu import Menu

class Main:
    def __init__(self):
        self.events = Events()
        pygame.init()
        pygame.display.set_caption("Snake")
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1600, 1000))
        self.game = Game(self.screen)
        self.menu = Menu(self.screen)
        self.menu.addButton("START", self.startGame)
        self.menu.addButton("EXIT", self.exit)

    def exit(self):
        pygame.quit()
        sys.exit()

    def startGame(self):
        self.screen.fill((100, 100, 100))
        self.game.start(16, 12)

    def run(self):
        while True:
            Events.reset()
            if Events.QUIT:
                self.exit()
            
            if (self.game.isRunning):
                self.game.update()
                self.game.display()
            else:
                self.menu.display()
            pygame.display.flip()

main = Main();\
main.run()