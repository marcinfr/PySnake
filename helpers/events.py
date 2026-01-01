import pygame

class Events:
    def __init__(self):
        self.MOUSEBUTTONDOWN = False
        self.QUIT = False
        self.EVENTPOSITION = False
        pass

    def reset(self):
        self.MOUSEBUTTONDOWN = False
        self.QUIT = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.QUIT = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.MOUSEBUTTONDOWN = True
                self.EVENTPOSITION = event.pos