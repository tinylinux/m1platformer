""" Stocke des variables partagées entre les différents fichiers """

import os
import pygame


def listdir(path):
    """listdir sans fichiers cachés (genre les .DS_Store)"""
    return [f for f in os.listdir(path) if not f.startswith('.')]


Vec = pygame.math.Vector2

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

# IMAGES
MONO_FACTOR = 3
n_mono = len(listdir("./assets/img/mono"))
mono_img = []
for i in range(n_mono):
    img = pygame.image.load("assets/img/mono/Mono"+str(i)+".png")
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (MONO_FACTOR*w, MONO_FACTOR*h))
    mono_img.append(img)

NUAGE_FACTOR = 4
n_nuage = len(listdir("./assets/img/nuages"))
nuage_img = []
for i in range(n_nuage):
    img = pygame.image.load("assets/img/nuages/nuage"+str(i)+".png")
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (NUAGE_FACTOR*w, NUAGE_FACTOR*h))
    nuage_img.append(img)

ARBRE_FACTOR = 8
n_arbre = len(listdir("./assets/img/arbres"))
arbre_img = []
for i in range(n_arbre):
    img = pygame.image.load("assets/img/arbres/Arbre"+str(i)+".png")
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (ARBRE_FACTOR*w, ARBRE_FACTOR*h))
    arbre_img.append(img)

SOL_IMG = pygame.image.load("assets/img/sol.png")
PLTFRM_IMG = pygame.image.load("assets/img/pltfrm.png")
BAT_IMG = pygame.image.load("assets/img/bat.png")

# Dimensions
p_WIDTH, p_HEIGHT = mono_img[0].get_rect().size
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
