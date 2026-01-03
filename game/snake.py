from helpers.timer import Timer

class Snake:

    COLORS = [
        "red",
        "black",
        "green",
        "yellow"
    ]

    def __init__(self, id, segements):
        self.id = id
        self.segments = segements
        self.direction = (1, 0)
        self.life = 1
        self.speed = 0.1  # seconds per move
        self.nextDirection = self.direction

    def move(self, game):
        if not Timer().has_elapsed("snake-move-" + str(self.id), self.speed):
            return
        
        self.direction = self.nextDirection
        board = game.board
        
        head_x, head_y = self.segments[0]
        dir_x, dir_y = self.direction

        new_head_x = head_x + dir_x
        new_head_y = head_y + dir_y

        if new_head_x < 0:
            new_head_x = len(board) - 1
        elif new_head_x >= len(board):
            new_head_x = 0
        if new_head_y < 0:
            new_head_y = len(board[0]) - 1
        elif new_head_y >= len(board[0]):
            new_head_y = 0

        grow = False    
        fruits = game.fruits
        if new_head_x in fruits and new_head_y in fruits[new_head_x]:
            grow = True;
            game.removeFruit(new_head_x, new_head_y)

        new_head = (new_head_x, new_head_y)

        if game.board[new_head_x][new_head_y] > 0:
            self.life -= 0.1
            return

        game.board[new_head_x][new_head_y] = 1;

        self.segments = [new_head] + self.segments
        if not grow:
            lastSegment = self.segments[-1]
            self.segments = self.segments[:-1]
            game.board[lastSegment[0]][lastSegment[1]] = 0

    def die(self, game):
        if not Timer().has_elapsed("snake-die-" + str(self.id), 0.1):
            return
        self.life -= 0.1
        if self.life <= 0:
            self.life = 0
            for segment in self.segments:
                 game.board[segment[0]][segment[1]] = 0

    def moveUp(self):
        if self.direction[1] != 1:
            self.nextDirection = (0, -1)

    def moveDown(self):
        if self.direction[1] != -1:
            self.nextDirection = (0, 1)

    def moveLeft(self):
        if self.direction[0] != 1:
            self.nextDirection = (-1, 0)

    def moveRight(self):
        if self.direction[0] != -1:
            self.nextDirection = (1, 0)