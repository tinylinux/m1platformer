""" Stocke des variables partagées entre les différents fichiers """

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

# Drapeau qui dit si y a un item à l'écran
# ou qu'on est dans un état spécial à cause d'un item
FLAG_ITEM = False

# Dico avec la durée des effets des items (en nbre de frames)
ITEM_TIME = {'fast': 40, 'slow': 40, 'little': 200, 'big': 200}

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

# États du jeu :
# 1 : menu de départ
# 2 : jeu en cours
# 3 : menu de fin (scores)
# 4 : affichage des meilleurs scores
STATE = 1

# La fenêtre principale
DISPLAYSURF = None
WINDOWSURF = None
