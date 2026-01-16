from game.maps import Maps
from game.themes import Themes

class SingleLevel:
    def __init__(self):
        self.pointsToWin = 0
        self.displayLevel = True

    def initLevel(self, game):
        self.pointsToWin = 10
        snake = self.getSnake(game)
        snake.totalPoints = 0
        game.map = Maps.getMap((game.currentLevel -1) % len(Maps.MAPS))
        themeId = (game.currentLevel -1) // len(Maps.MAPS)
        game.theme = Themes.getTheme(themeId % len(Themes.THEMES))

    def isLevelFinished(self, game):
        if self.getSnake(game).totalPoints >= self.pointsToWin:
            return True
        return False
    
    def getSnake(self, game):
        return game.snakes[0]