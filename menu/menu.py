import pygame
from helpers.events import Events

class Menu:
    def __init__(self, screen, main):
        pygame.joystick.init()
        self.screen = screen
        self.buttons = []
        self.main = main
        self.isActive = False

    def activate(self):
        self.isActive = True
        Events.addEventListener("menu_down", "key_down_" + str(pygame.K_UP), self.moveUp)
        Events.addEventListener("menu_up", "key_down_" + str(pygame.K_DOWN), self.moveDown)
        Events.addEventListener("menu_click", "key_down_" + str(pygame.K_RETURN), self.click)
        self.openMenu('main')

    def deactivate(self):
        self.isActive = False
        Events.removeEventListener("menu_down")
        Events.removeEventListener("menu_up")
        Events.removeEventListener("menu_click")

    def moveUp(self):
        self.currentButton -= 1
        if self.currentButton < 0:
            self.currentButton = len(self.buttons) -1
            
    def moveDown(self):
        self.currentButton += 1
        if self.currentButton == len(self.buttons):
            self.currentButton = 0

    def click(self):
        button = self.buttons[self.currentButton]
        button.click()

    def display(self):
        if (not self.isActive):
            self.activate()

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

        if (self.currentMenu == 'multiplayer'):
            count = pygame.joystick.get_count()
            #print("Wykryte kontrolery:", count)
            Button("Wykryte kontrolery:" + str(count), False).display(self.screen, x, y)

            for i in range(count):
                js = pygame.joystick.Joystick(i)
                js.init()
                Button(js.get_name(), False).display(self.screen, x, y)
                y += 120


    def openMenu(self, menu):
        self.currentMenu = menu
        self.initButtons(menu)

    def initButtons(self, menu):
        self.currentButton = 0
        self.buttons = []
        if (menu == "main"):
            self.addButton("SINGLE PLAYER", self.main.startGame)
            self.addButton("MULTI PLAYER", [self.openMenu, 'multiplayer'])
            self.addButton("EXIT", self.main.exit)
        if (menu == "multiplayer"):
            self.addButton("START", self.main.startGame2)
            self.addButton("BACK", [self.openMenu, 'main'])

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
            if callable(self.onclick):
                self.onclick()
            else:
                self.onclick[0](self.onclick[1])
        