import pygame
from helpers.events import Events

class Keyboard:
    def __init__(self, snake):
        self.snake = snake
        Events.addEventListener("key_down_" + str(pygame.K_UP), snake.moveUp)
        Events.addEventListener("key_down_" + str(pygame.K_DOWN), snake.moveDown)
        Events.addEventListener("key_down_" + str(pygame.K_LEFT), snake.moveLeft)
        Events.addEventListener("key_down_" + str(pygame.K_RIGHT), snake.moveRight)
