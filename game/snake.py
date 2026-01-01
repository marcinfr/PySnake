from helpers.timer import Timer

class Snake:
    def __init__(self, id, segements):
        self.id = id
        self.segments = segements
        self.direction = (1, 0)
        self.speed = 0.1  # seconds per move

    def move(self, board):
        if not Timer().has_elapsed("snake-move-" + str(self.id), self.speed):
            return
        
        head_x, head_y = self.segments[0]
        dir_x, dir_y = self.direction

        new_head_x = head_x + dir_x
        new_head_y = head_y + dir_y

        if new_head_x < 0:
            new_head_x = len(board[0]) - 1
        elif new_head_x >= len(board[0]):
            new_head_x = 0
        if new_head_y < 0:
            new_head_y = len(board) - 1
        elif new_head_y >= len(board):
            new_head_y = 0

        new_head = (new_head_x, new_head_y)
        self.segments = [new_head] + self.segments[:-1]

    def moveUp(self):
        self.direction = (0, -1)

    def moveDown(self):
        self.direction = (0, 1)

    def moveLeft(self):
        self.direction = (-1, 0)

    def moveRight(self):
        self.direction = (1, 0)