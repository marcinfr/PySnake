import pygame
from helpers.events import Events

class Pad:
    def __init__(self, joystick):
        self.joystick = joystick

    def setSnake(self, snake):
        Events.addEventListener("snake_up" + str(snake.id), "joy_hat_motion", (self.moveSnake, snake))

    def moveSnake(self, snake):
        if self.joystick.get_id() in Events.JOYHATMOTIONS:
            value = Events.JOYHATMOTIONS[self.joystick.get_id()]
            if value[0] == 1:
                snake.moveRight()
            if value[0] == -1:
                snake.moveLeft()
            if value[1] == 1:
                snake.moveUp()
            if value[1] == -1:
                snake.moveDown()
