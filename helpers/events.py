import pygame

class Events:
    eventListeners = []
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
    def addEventListener(eventName, callback):
        Events.eventListeners.append((eventName, callback))

    @staticmethod
    def dispatchEvent(eventName):
        print("Dispatching event: " + eventName)
        for listenerEventName, callback in Events.eventListeners:
            if listenerEventName == eventName:
                callback()

    @staticmethod
    def removeEventListener(eventName, callback):
        Events.eventListeners = [
            (en, cb) for (en, cb) in Events.eventListeners
            if en != eventName or cb != callback
        ]