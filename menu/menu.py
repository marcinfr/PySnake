import pygame
from helpers.events import Events

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.currentButton = 0
        Events.addEventListener("key_down_" + str(pygame.K_UP), self.moveUp)
        Events.addEventListener("key_down_" + str(pygame.K_DOWN), self.moveDown)
        Events.addEventListener("key_down_" + str(pygame.K_RETURN), self.click)

    def moveUp(self):
        self.currentButton -= 1
        if self.currentButton < 0:
            self.currentButton = len(self.buttons) -1
        print(self.currentButton)

    def moveDown(self):
        self.currentButton += 1
        if self.currentButton == len(self.buttons):
            self.currentButton = 0
        print(self.currentButton)

    def click(self):
        button = self.buttons[self.currentButton]
        button.click()

    def display(self):
        self.screen.fill((100, 100, 100))
        pygame.draw.rect(self.screen, "red", (
            0,
            0,
            20,
            20,
        ))
        x = 10
        y = 0
        for index, button in enumerate(self.buttons):
            if (index == self.currentButton):
                button.isActive = True
            else:
                button.isActive = False
            button.display(self.screen, x, y)
            y += 120

    def addButton(self, title, onClick = False):
        self.buttons.append(Button(title, onClick))

class Button:
    def __init__(self, title, onClick = False):
        self.title = title
        self.textColor = "white"
        self.isActive = False
        self.onclick = onClick

    def display(self, surface, x, y):
        width = 500
        height = 100
        button = pygame.Surface((width, height), pygame.SRCALPHA)
        if self.isActive:
            button.fill((200, 0, 0, 255))
        else:
            button.fill((100, 0, 0, 255))
        font = pygame.font.Font(None, 25) 
        text = font.render(self.title, True, self.textColor)
        #pygame.draw.rect(button, "blue", (
        #    0,
        #    0,
        #    width,
        #    height,
        #))
        textRect = text.get_rect()
        centerX = width / 2
        centerY = height / 2
        textRect.center = (centerX, centerY)
        button.blit(text, textRect)
        surface.blit(button, (x, y))

    def click(self):
        if self.onclick:
            self.onclick()
        