""" Stocke des variables partagées entre les différents fichiers """
from enum import Enum

# Screen configurations
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Font sizes
HIGHTSCORES_FONT_SIZE = 36
SCORE_FONT_SIZE = 25
RESULT_FONT_SIZE = 50
INPUT_FONT_SIZE = 35
TEXT_FONT_SIZE = 25

# vitesse initiale de défilement du sol
INITIAL_SPEED = 5
SPEED = INITIAL_SPEED
# Drapeau de disponibilité du saut
FLAG_JUMP = False
# Drapeau de disponibilité du second saut
FLAG_JUMP_2 = False

# Couleurs
BLACK = (255, 255, 255)
GREY = (240, 240, 240)
BlueSky = (0, 170, 251)
WHITE = (255, 255, 255)
IDLE = (170, 170, 170)
HOVER = (100, 100, 100)

# Compteurs pour le score
SECONDS = 0
FRAMES = 0

# États du jeu
class State(Enum):
    """
    Type énuméré pour l'état du jeu
    """
    languages = 0
    menu = 1
    ingame = 2
    gameover = 3
    highscore = 4
    setup = 5


STATE = State.menu

# La fenêtre principale
DISPLAYSURF = None
WINDOWSURF = None
