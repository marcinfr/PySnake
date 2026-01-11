from helpers.timer import Timer

class Snake:

    COLORS = [
        (138, 43, 226),  # fioletowy (Blue Violet)
        (220, 20, 60),    # czerwony (Crimson)
        (30, 144, 255),  # niebieski (Dodger Blue)
        (255, 215, 0),  # żółty / złoty (Gold)
        (255, 140, 0),   # pomarańczowy (Dark Orange)
        (0, 206, 209),   # turkusowy (Dark Turquoise)
    ]

    def __init__(self, id, segements, color):
        self.id = id
        self.segments = segements
        self.life = 1
        self.speed = 0.12  # seconds per move
        self.color = self.COLORS[color]
        self.setDirection((1,0))
        self.totalPoints = 0
        self.offset = 0.1
        self.offsetRate = 1
        self.isFrozen = 0

    def setDirection(self, dir):
        self.direction = dir
        self.nextDirection = self.direction

    def move(self, game):
        if self.isFrozen > 0:
            self.unFreeze()
            return

        if Timer().has_elapsed("snake-move-" + str(self.id), self.speed * self.offsetRate):
            self.offset -= self.offsetRate

        if self.offset > 0:
            return
                
        self.direction = self.nextDirection
        board = game.board
        
        head_x = self.segments[0]['x']
        head_y = self.segments[0]['y']
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

        if game.board[new_head_x][new_head_y] > 0:
            game.onSnakeDie(self)
            self.life -= 0.1
            return

        new_head = {'x': new_head_x, 'y': new_head_y, 'dir': self.direction}
        self.segments = [new_head] + self.segments

        grow = False    
        fruits = game.fruits
        if new_head_x in fruits and new_head_y in fruits[new_head_x]:
            grow = True;
            game.onFruitPick(self)
            game.removeFruit(new_head_x, new_head_y)
        
        self.offset = 1
        game.board[new_head_x][new_head_y] = 1;

        if not grow:
            lastSegment = self.segments[-1]
            self.segments = self.segments[:-1]
            game.board[lastSegment['x']][lastSegment['y']] = 0

    def die(self, game):
        self.offset = 0
        if not Timer().has_elapsed("snake-die-" + str(self.id), 0.1):
            return
        self.life -= 0.1
        if self.life <= 0:
            self.life = 0
        if self.life <= 0.6:
            for segment in self.segments:
                game.board[segment['x']][segment['y']] = 0

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

    def freeze(self, seconds):
        if self.life < 1:
            return
        
        Timer.set_time("snake-frozen-" + str(self.id))
        self.isFrozen = seconds

    
    def unFreeze(self):
        print( self.isFrozen)
        if self.isFrozen > 0 and Timer().has_elapsed("snake-frozen-" + str(self.id), self.isFrozen):
            self.isFrozen = 0;