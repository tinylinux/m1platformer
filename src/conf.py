""" Stocke des variables partagées entre les différents fichiers """

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# vitesse initiale de défilement du sol
INITIAL_SPEED = 5
SPEED = INITIAL_SPEED
# Drapeau de disponibilité du saut
FLAG_JUMP = False
# Drapeau de disponibilité du second saut
FLAG_JUMP_2 = False

# Couleur du ciel
BlueSky = (0, 170, 251)

# Compteurs pour le score
SECONDS = 0
FRAMES = 0

# États du jeu : 
# {menu, in-game, gameover, highscore}
STATE = 'menu'

# La fenêtre principale
DISPLAYSURF = None
WINDOWSURF = None
