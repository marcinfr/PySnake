import pygame
import sys
from helpers.events import Events
from helpers.timer import Timer
from game.game import Game
from menu.menu import Menu

class Main:
    def __init__(self):
        self.events = Events()
        pygame.init()
        pygame.mixer.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.screen = pygame.display.set_mode((1280, 800))
        #self.screen = pygame.display.set_mode((800, 600))
        self.game = Game(self.screen)
        self.menu = Menu(self.screen, self)
        self.menu.activate()

    def exit(self):
        print("pygame.quit")
        pygame.quit()
        print("sys.exit")
        sys.exit()
        print("EXIT")


    def startGame(self, data):
        self.menu.deactivate()
        self.menu.currentMenu = 'game'
        self.screen.fill((100, 100, 100))
        self.game.start(data)

    def run(self):

        font = pygame.font.SysFont(None, 24)
        clock = pygame.time.Clock()
        fps_text = False

        while True:
            Events.reset()
            if Events.QUIT:
                self.exit()

            clock.tick(1000)
            
            if (not self.game.isPaused):
                #if self.game.isRunning:
                self.game.update()
                self.game.display()
            else:
                if (self.menu.currentMenu == 'game'):
                    self.game.display()
                self.menu.display()


            if Timer.has_elapsed('fps', 1):
                fps = clock.get_fps()
                fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
                
            if fps_text:
                self.screen.blit(fps_text, (self.screen.get_width() - 100, 10))

            pygame.display.flip()

main = Main()
main.run()