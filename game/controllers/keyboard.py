import pygame
from helpers.events import Events

class Keyboard:
    def __init__(self):
        pass

    def setSnake(self, snake):
        Events.addEventListener("snake_up" + str(snake.id), "key_down_" + str(pygame.K_UP), snake.moveUp)
        Events.addEventListener("snake_down" + str(snake.id), "key_down_" + str(pygame.K_DOWN), snake.moveDown)
        Events.addEventListener("snake_left" + str(snake.id), "key_down_" + str(pygame.K_LEFT), snake.moveLeft)
        Events.addEventListener("snake_right" + str(snake.id), "key_down_" + str(pygame.K_RIGHT), snake.moveRight)
