""" Stocke des variables partagées entre les différents fichiers """

import os
import pygame


def listdir(path):
    """listdir sans fichiers cachés (genre les .DS_Store)"""
    return [f for f in os.listdir(path) if not f.startswith('.')]


Vec = pygame.math.Vector2

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

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

# Crée un nouvel event, le +1 sert à avoir un nouvel ID
INC_SPEED = pygame.USEREVENT + 1

# Toutes les secondes on augmente la vitesse
FPS = 60
pygame.time.set_timer(INC_SPEED, 1000)

# Compteurs pour le score
SECONDS = 0
FRAMES = 0

# États du jeu :
# 1 : menu de départ
# 2 : jeu en cours
# 3 : menu de fin (scores)
# 4 : affichage des meilleurs scores
STATE = 1

# IMAGES
d = {}
Nom = ["mono", "nuage", "arbre"]
d["mono_factor"] = 3
d["nuage_factor"] = 4
d["arbre_factor"] = 8
for nom in Nom:
    d['n_'+nom] = len(listdir("./assets/img/"+nom))
    d[nom+'_img'] = []
    for i in range(d['n_'+nom]):
        img = pygame.image.load("assets/img/"+nom+"/"+nom+str(i)+".png")
        w, h = img.get_rect().size
        img = pygame.transform.scale(img, (d[nom+'_factor'] * w,
                                     d[nom+'_factor'] * h))
        d[nom+'_img'].append(img)

SOL_IMG = pygame.image.load("assets/img/sol.png")
PLTFRM_IMG = pygame.image.load("assets/img/pltfrm.png")
BAT_IMG = pygame.image.load("assets/img/bat.png")

# Dimensions
p_WIDTH, p_HEIGHT = d["mono_img"][0].get_rect().size
w, h = SOL_IMG.get_rect().size
SOL_HAUT = (SCREEN_HEIGHT - h)      # La hauteur du sol en général
SOL_LONG = w      # La longueur d'un bloc du sol en général

# Groupes
sol = pygame.sprite.Group()
nuages = pygame.sprite.Group()
arbres = pygame.sprite.Group()

# La fenêtre principale
DISPLAYSURF = None
WINDOWSURF = None

# Nombre maximal de joueurs
NB_PLAYERS_MAX = 2
# Nombre de joueurs
NB_PLAYERS = 2
# Touches de saut des joueurs
JUMP_KEYS = [pygame.K_SPACE, pygame.K_RETURN]

class GameObject(pygame.sprite.Sprite):
    # pylint: disable=too-few-public-methods
    """Utilisée pour tous les objets du monde, comme le sol, les plateformes,
        les nuages, les bâtiments, etc. qui se déplacent de droite à gauche"""
    def __init__(self, position, scroll, image):
        """position : int * int, position de l'objet
        scroll : float/int, vitesse de déplacement
        img : sprite"""
        super().__init__()
        self.pos = Vec(position)
        self.scroll = scroll
        # 0 si c'est loin et que ça bouge pas,
        # 1 si c'est près et que ça bouge à la vitesse du sol
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        # Limite à partir de laquelle on génère un nouvel objet sur sa droite
        # pasencorecree est un flag pour ne générer qu'un seul nouvel objet
        self.pasencorecree = True

    def update(self):
        """Modifie le vecteur position"""
        posnext = self.pos + self.scroll * Vec(-SPEED, 0)
        self.pos = posnext
        self.rect.topleft = self.pos
        if self.rect.right < 0:     # si l'objet sort de l'écran
            self.kill()              # on le supprime
        # On met à jour l'image
        DISPLAYSURF.blit(self.image, self.rect)
