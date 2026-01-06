from random import randrange
from game.boardView.classic import ClassicBoardView
from game.boardView.space import SpaceBoardView

class Themes:
    THEMES = [
        {
            'name': "Classic",
            'boardView': ClassicBoardView()
        },
        {
            'name': "Space",
            'boardView': SpaceBoardView()
        }
    ]


    @staticmethod
    def getTheme(themeId):
        return Themes.THEMES[themeId]
    
    @staticmethod
    def getRandomTheme():
        themeId = randrange(0, len(Themes.THEMES))
        return Themes.getTheme(themeId)