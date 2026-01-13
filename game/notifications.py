from helpers.timer import Timer
import pygame

class Notifications:
    def __init__(self, screen):
        self.screen = screen
        self.notifications = []
        
    def addNotification(self, pos, text, time):
        Timer.get_timestamp()
        self.notifications.append({
            'pos': pos,
            'text': text,
            'time': time,
            'added_at': Timer.get_timestamp()
        })

    def process(self):
        for n in self.notifications:
            elapsed = Timer.get_timestamp() - n['added_at']
            if elapsed > n['time']:
                self.notifications.remove(n)
                continue

    def display(self):
        for n in self.notifications:
            text = n['text']
            elapsed = Timer.get_timestamp() - n['added_at']
            alpha = 255 - (255 / n['time']) * elapsed
            pos = n['pos']
            pos = (pos[0], pos[1] - round((255 / text.get_height()) * elapsed))
            
            text.set_alpha(alpha)
            self.screen.blit(text, pos)