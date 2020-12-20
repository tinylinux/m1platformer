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
LANG = "NONE"

# La fenêtre principale
DISPLAYSURF = None
WINDOWSURF = None

# Nombre maximal de joueurs
NB_PLAYERS_MAX = 3
# Nombre de joueurs
NB_PLAYERS = 3

# Vitesse initiale lors d'un saut
V_JMP = 15
# Accélération due à la gravité
G = 0.8

# Flag : true si y a un item à l'écran
# ou qu'on est dans un état spécial à cause d'un item
FLAG_ITEM = False
