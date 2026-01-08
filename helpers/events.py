import pygame

class Events:
    eventListeners = {}
    MOUSEBUTTONDOWN = False
    QUIT = False
    EVENTPOSITION = (0, 0)
    KEYDOWN = False
    PRESSEDKEYS = []
    JOYSTICKS = {}
    JOYHATMOTIONS = {}
    JOYBUTTONDOWNS = {}

    @staticmethod
    def reset():
        Events.resetKeys()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                Events.QUIT = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                Events.MOUSEBUTTONDOWN = True
                Events.EVENTPOSITION = event.pos
            if event.type == pygame.KEYDOWN:
                Events.KEYDOWN = True
                Events.PRESSEDKEYS.append(event.key)
                Events.dispatchEvent("key_down_" + str(event.key))
            if event.type == pygame.JOYBUTTONDOWN:
                js = Events.JOYSTICKS.get(event.joy)
                if (js):
                    Events.JOYBUTTONDOWNS[js.get_id()] = event.button
                    Events.dispatchEvent("joy_button_down")
            if event.type == pygame.JOYHATMOTION:
                js = Events.JOYSTICKS.get(event.joy)
                if (js):
                    Events.JOYHATMOTIONS[js.get_id()] = event.value
                    Events.dispatchEvent('joy_hat_motion')
                    Events.dispatchEvent('joy_hat_motion_' + str(js.get_id()))

    @staticmethod
    def addJoystick(js):
        Events.JOYSTICKS[js.get_id()] = js

    @staticmethod
    def resetKeys():
        Events.MOUSEBUTTONDOWN = False
        Events.QUIT = False
        Events.KEYDOWN = False
        Events.PRESSEDKEYS = []
        Events.JOYHATMOTIONS = {}
        Events.JOYBUTTONDOWNS = {}

    @staticmethod
    def isKeyPressed(key):
        return key in Events.PRESSEDKEYS

    @staticmethod
    def addEventListener(eventName, onEvent, callback):
        Events.eventListeners[eventName] = (onEvent, callback)

    @staticmethod
    def dispatchEvent(eventName):
        eventsToDispatch = []
        for event in Events.eventListeners.values():
            if event[0] == eventName:
                eventsToDispatch.append(event[1])
        for event in eventsToDispatch:
            if callable(event):
                event()
            else:
                event[0](event[1])

    @staticmethod
    def removeEventListener(eventName):
        Events.eventListeners.pop(eventName, None)