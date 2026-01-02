import pygame

class Events:
    eventListeners = {}
    MOUSEBUTTONDOWN = False
    QUIT = False
    EVENTPOSITION = (0, 0)
    KEYDOWN = False
    PRESSEDKEYS = []

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
                Events.dispatchEvent("key_down_" + str(event.key))
                Events.KEYDOWN = True
                Events.PRESSEDKEYS.append(event.key)
            if event.type == pygame.JOYBUTTONDOWN:
                js = pygame.joystick.Joystick(event.joy)
                print(f"Pad {js.get_name()} przycisk {event.button} wciśnięty")

    @staticmethod
    def resetKeys():
        Events.MOUSEBUTTONDOWN = False
        Events.QUIT = False
        Events.KEYDOWN = False
        Events.PRESSEDKEYS = []

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
            event()

    @staticmethod
    def removeEventListener(eventName):
        Events.eventListeners.pop(eventName, None)