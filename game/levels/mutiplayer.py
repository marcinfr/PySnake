from game.levels.single import SingleLevel
from game.maps import Maps
from game.themes import Themes

class MultiplayerLevel(SingleLevel):

    def initLevel(self, game):
        self.displayLevel = False
        game.map = Maps.getRandomMap()
        themeId = game.settings['theme']
        if themeId == None:
            game.theme = Themes.getRandomTheme()
        else:
            game.theme = Themes.getTheme(themeId)

    def isLevelFinished(self, game):
        if len(game.snakes) > 1 and game.aliveSnakes < 2:
            return True
        return False
