from helpers.timer import Timer

class Notifications:
    def __init__(self, screen):
        Timer.set_time("notifications")
        self.screen = screen
        self.notifications = []
        
    def addNotification(self, pos, text, time):
        self.notifications.append({
            'pos': pos,
            'text': text,
            'time': time,
            'added_at': Timer.get_elapsed_time("notifications")
        })

    def process(self):
        for n in self.notifications:
            elapsed = Timer.get_elapsed_time("notifications") - n['added_at']
            if elapsed > n['time']:
                self.notifications.remove(n)
                continue

    def display(self):
        for n in self.notifications:
            text = n['text']
            elapsed = Timer.get_elapsed_time("notifications") - n['added_at']
            alpha = 255 - (255 / n['time']) * elapsed
            pos = n['pos']
            pos = (pos[0], pos[1] - round((255 / text.get_height()) * elapsed))
            
            text.set_alpha(alpha)
            self.screen.blit(text, pos)