import pygame
from helpers.events import Events
import math
from game.snake import Snake
from game.themes import Themes

class Menu:
    def __init__(self, screen, main):
        pygame.joystick.init()
        self.screen = screen
        self.buttons = []
        self.main = main
        self.isActive = False
        self.background = None
        self.currentMenu = 'main'
        self.players = {}
        self.gameSettings = {}

    def activate(self):
        self.isActive = True
        Events.addEventListener("menu_down", "key_down_" + str(pygame.K_UP), self.moveUp)
        Events.addEventListener("menu_up", "key_down_" + str(pygame.K_DOWN), self.moveDown)
        Events.addEventListener("menu_click", "key_down_" + str(pygame.K_RETURN), self.click)
        self.openMenu()

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

        self.screen.fill((0, 0, 0))
        self.displayBackground()

        x = self.screen.get_width() // 2 - 300
        y = self.screen.get_height() * 20 / 100

        for index, button in enumerate(self.buttons):
            if (index == self.currentButton):
                button.isActive = True
            else:
                button.isActive = False
            button.display(self.screen, x, y)
            y += 90


        if (self.currentMenu == 'multiplayer'):
            self.initJoysticks()
            Button('Press any button on pad to join', False).disable().display(self.screen, x, y)

    def initJoysticks(self):
        count = pygame.joystick.get_count()
        #print("Wykryte kontrolery:", count)
        #Button("Wykryte kontrolery:" + str(count), False).display(self.screen, x, y)

        for i in range(count):
            js = pygame.joystick.Joystick(i)
            js.init()
        
    def openMenu(self, menu = None):
        if menu is not None:
            self.currentMenu = menu

        if (self.currentMenu == 'main'):
            print("!!!");
            self.players = {}
            self.gameSettings = {
                'level': None,
                'theme': 0
            }
        if (self.currentMenu == 'multiplayer'):
            Events.addEventListener("menu_multiplayer_joy_button_down", "joy_button_down", self.addJoystickPlayer)
        else:
            Events.removeEventListener("menu_multiplayer_joy_button_down")
    
        self.initButtons()

    def addJoystickPlayer(self):
        for joy_id in Events.JOYBUTTONDOWNS:
            if joy_id not in self.players:
                js = pygame.joystick.Joystick(joy_id)
                self.addPlayer(joy_id, 
                    {
                        'type': 'joystick',
                        'joystick': js,
                        'color': 0
                    }
                )
                Events.addEventListener('joy_player_next_color_event' + str(joy_id), 'joy_hat_motion_' + str(joy_id), [self.changeJoyPlayerColor, joy_id]);

    def addMainPlayer(self):
        self.addPlayer('main', { 'type': 'main', 'color': 0})
        Events.addEventListener('main_player_next_color_event', "key_down_" + str(pygame.K_RIGHT), [self.nextPlayerColor, 'main']);
        Events.addEventListener('main_player_prev_color_event', "key_down_" + str(pygame.K_LEFT), [self.prevPlayerColor, 'main']);

    def addPlayer(self, id, playerData):
        self.players[id] = playerData
        self.addPlayerButton('Player ' + str(len(self.players)), id, False)

    def changeJoyPlayerColor(self, joy_id):
        value = Events.JOYHATMOTIONS[joy_id]
        if value[0] == 1:
            self.nextPlayerColor(joy_id)
        if value[0] == -1:
            self.prevPlayerColor(joy_id)

    def nextPlayerColor(self, playerId):
        if self.currentMenu != 'multiplayer':
            return
        currentColor = self.players[playerId]['color']
        currentColor += 1
        if currentColor == len(Snake.COLORS):
            currentColor = 0
        self.players[playerId]['color'] = currentColor

    def prevPlayerColor(self, playerId):
        if self.currentMenu != 'multiplayer':
            return
        currentColor = self.players[playerId]['color']
        currentColor -= 1
        if currentColor < 0:
            currentColor = len(Snake.COLORS) - 1
        self.players[playerId]['color'] = currentColor

    def initButtons(self):
        self.currentButton = 0
        self.buttons = []
        if (self.currentMenu == "main"):
            self.addButton("SINGLE PLAYER", (self.main.startGame, {'players': {}, 'settings': self.gameSettings}))
            self.addButton("MULTI PLAYER", [self.openMenu, 'multiplayer'])
            self.addButton("EXIT", self.main.exit)
        if (self.currentMenu == "multiplayer"):
            self.addButton("START", (self.main.startGame, {'players': self.players, 'settings': self.gameSettings}))
            #self.addSelectLevelButton()
            self.addSelectThemeButton()
            self.addButton("BACK", [self.openMenu, 'main'])
            self.addMainPlayer()
        if (self.currentMenu == "game"):
            if (not self.main.game.isEndGame):
                self.addButton("RESUME", self.unPause)
            self.addButton("PLAY AGAIN", (self.main.startGame, {'players': self.players, 'settings': self.gameSettings}))
            self.addButton("EXIT", [self.openMenu, 'main'])

    def unPause(self):
        self.deactivate()
        self.main.game.unPause()

    def addButton(self, title, onClick = False):
        self.buttons.append(Button(title, onClick))

    def addPlayerButton(self, title, playerId, onClick = False):
        self.buttons.append(PlayerButton(title, onClick).setPlayerId(playerId).setPlayers(self.players))

    def addSelectLevelButton(self):
        self.buttons.append(SelectLevelButton('', self.selectNextLevel).setGameSettings(self.gameSettings))

    def addSelectThemeButton(self):
        self.buttons.append(SelectThemeButton('', self.selectNextTheme).setGameSettings(self.gameSettings))

    def displayBackground(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))

        cols = 30
        self.background = pygame.Surface(self.screen.get_size())
        size = math.ceil(self.screen.get_width() / cols)
        rows = math.ceil(self.screen.get_height() / size)

        for x in range(cols):
            for y in range(rows):
                d = 1
                if (x + 1) * size < self.screen.get_width() / 2 - 500:
                    d = 0.6
                if x * size > self.screen.get_width() / 2 + 500:
                    d = 0.6
                    
                if x % 2 == y % 2:
                    color = (170 * d, 215 * d, 81 * d)
                else:
                    color = (162 * d, 209 * d, 73 * d)
                pygame.draw.rect(self.background, color, (
                    x * size,
                    y * size,
                    size,
                    size,
                ))
        font = pygame.font.Font(None, 300)
        text = font.render("SNAKE", True, "White")

        target_height = self.screen.get_height() * 15 / 100 
        scale = target_height / text.get_height()
        new_width = int(text.get_width() * scale)
        text = pygame.transform.scale(text, (new_width, target_height))

        textRect = text.get_rect()
        centerX = self.background.get_width() / 2
        centerY = self.background.get_height() * 20 / 100 - (textRect.height / 2)
        textRect.center = (centerX, centerY)
        self.background.blit(text, textRect)
    
    def selectNextLevel(self):
        if self.gameSettings['level'] == False:
            self.gameSettings['level'] = 0
        else:
            self.gameSettings['level'] = False
    
    def selectNextTheme(self):
        if self.gameSettings['theme'] == None:
            self.gameSettings['theme'] = 0
        else:
            self.gameSettings['theme'] += 1

        if self.gameSettings['theme'] >= len(Themes.THEMES):
            self.gameSettings['theme'] = None

        print(self.gameSettings['theme'])

class Button:
    def __init__(self, title = '', onClick = False):
        self.title = title
        self.textColor = "white"
        self.textColorActive = "black"
        self.isActive = False
        self.isDisabled = False
        self.onclick = onClick

    def disable(self):
        self.isDisabled = True
        return self

    def display(self, surface, x, y):
        button = self.getButton()
        surface.blit(button, (x, y))

    def getButton(self):
        width = 600
        height = 80
        button = pygame.Surface((width, height), pygame.SRCALPHA)
        if self.isDisabled:
            #button.fill((100, 100, 100, 255))
            color = self.textColor
            pass
        elif self.isActive:
            button.fill((255, 255, 255, 255))
            color = self.textColorActive
        else:
            button.fill((255, 255, 255, 100))
            color = self.textColor
        font = pygame.font.Font(None, 50) 
        text = font.render(self.title, True, color)
        textRect = text.get_rect()
        centerX = width / 2
        centerY = height / 2
        textRect.center = (centerX, centerY)
        button.blit(text, textRect)
        return button

    def click(self):
        if self.onclick:
            if callable(self.onclick):
                self.onclick()
            else:
                self.onclick[0](self.onclick[1])
        
class PlayerButton(Button):

    def setPlayerId(self, id):
        self.playerId = id
        return self
    
    def setPlayers(self, players):
        self.players = players
        return self

    def getButton(self):
        color = Snake.COLORS[self.players[self.playerId]['color']];

        button = super().getButton()
        size = button.get_height() - 10
        pygame.draw.rect(button, color, (
            5,
            5,
            size,
            size
        ))
        #button.blit(colorBox, (10, 10))
        return button

class SelectLevelButton(Button):

    def setGameSettings(self, gameSettings):
        self.gameSettings = gameSettings
        return self

    def getButton(self):
        if self.gameSettings['level']:
            self.title = ""
        else: 
            self.title = "Random Level"
        button = super().getButton()


        if self.gameSettings['level']:
            size = button.get_height() - 10
            pygame.draw.rect(button, "black", (
                (button.get_width() - size) // 2,
                5,
                size,
                size
            ))

        return button
    
class SelectThemeButton(Button):
        
    def setGameSettings(self, gameSettings):
        self.gameSettings = gameSettings
        return self
    
    def getButton(self):
        if self.gameSettings['theme'] == None:
            self.title = "Random"
        else: 
            theme = Themes.getTheme(self.gameSettings['theme'])
            self.title = theme['name']

        self.title = self.title + " Theme"
        button = super().getButton()
        return button