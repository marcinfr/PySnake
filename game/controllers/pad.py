import pygame
from helpers.events import Events

class Pad:
    def __init__(self, joystick):
        self.joystick = joystick

    def setSnake(self, snake):
        pass
        #Events.addEventListener("snake_up" + str(snake.id), "key_down_" + str(pygame.K_UP), snake.moveUp)
        #Events.addEventListener("snake_down" + str(snake.id), "key_down_" + str(pygame.K_DOWN), snake.moveDown)
        #Events.addEventListener("snake_left" + str(snake.id), "key_down_" + str(pygame.K_LEFT), snake.moveLeft)
        #Events.addEventListener("snake_right" + str(snake.id), "key_down_" + str(pygame.K_RIGHT), snake.moveRight)
