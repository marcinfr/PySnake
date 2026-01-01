import pygame
import sys
from helpers.events import Events
from game.game import Game
from menu.menu import Menu
from game.controllers.keyboard import Keyboard

class Main:
    def __init__(self):
        self.events = Events()
        pygame.init()
        pygame.display.set_caption("Snake")
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1280, 800))
        self.game = Game(self.screen)
        self.menu = Menu(self.screen)
        self.menu.addButton("1 PLAYER", self.startGame)
        self.menu.addButton("2 PLAYERS", self.startGame2)
        self.menu.addButton("EXIT", self.exit)
        self.menu.activate()

    def exit(self):
        pygame.quit()
        sys.exit()

    def startGame(self):
        self.menu.deactivate()
        self.screen.fill((100, 100, 100))
        self.game.start(32, 20)
        self.game.addSnake((1,1), 3, Keyboard())

    def startGame2(self):
        self.startGame()
        self.game.addSnake((10, 10), 3, False)

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