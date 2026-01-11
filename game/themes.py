from random import randrange
from game.boardView.classic import ClassicBoardView
from game.boardView.space import SpaceBoardView
from game.boardView.retro import RetroBoardView

from game.snakeView.default import DefaultSnakeView
from game.snakeView.rocket import RocketSnakeView

class Themes:
    THEMES = [
        {
            'name': "Classic",
            'boardView': ClassicBoardView(),
            'snakeView': DefaultSnakeView(),
        },
        #{
        #    'name': "Retro",
        #    'boardView': RetroBoardView(),
        #    'snakeView': DefaultSnakeView(),
        #},
        {
            'name': "Space",
            'boardView': SpaceBoardView(),
            'snakeView': RocketSnakeView(),
        }
    ]


    @staticmethod
    def getTheme(themeId):
        return Themes.THEMES[themeId]
    
    @staticmethod
    def getRandomTheme():
        themeId = randrange(0, len(Themes.THEMES))
        return Themes.getTheme(themeId)