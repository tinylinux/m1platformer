""" Stocke des variables partagées entre les différents fichiers """

import os
import pygame


def listdir(path) :
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
# d = {}
# Nom = ["mono","nuage","arbre"]
# mono_factor = 3
# nuage_factor = 4
# arbre_factor = 8
# for nom in Nom :
#     d['n_'+nom] = len(listdir("./assets/img/"+nom))
#     d[nom+'_img'] = []
#     for i in range(d['n_'+nom]):
#         img = pygame.image.load("assets/img/"+nom+"/"+nom+str(i)+".png")
#         w, h = img.get_rect().size
#         img = pygame.transform.scale(img, (d[nom+'_factor']*w,d[nom+'_factor']*h))
#         d[nom+'_img'].append(img)






mono_factor = 3
n_mono = len(listdir("./assets/img/mono"))
mono_img = []
for i in range(n_mono):
    img = pygame.image.load("assets/img/mono/mono"+str(i)+".png")
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (mono_factor*w,mono_factor*h))
    mono_img.append(img)

nuage_factor = 4
n_nuage = len(listdir("./assets/img/nuage"))
nuage_img = []
for i in range(n_nuage):
    img = pygame.image.load("assets/img/nuage/nuage"+str(i)+".png")
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (nuage_factor*w,nuage_factor*h))
    nuage_img.append(img)

arbre_factor = 8
n_arbre = len(listdir("./assets/img/arbre"))
arbre_img = []
for i in range(n_arbre):
    img = pygame.image.load("assets/img/arbre/arbre"+str(i)+".png")
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (arbre_factor*w,arbre_factor*h))
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
    def __init__(self, position, scroll, img):
        """position : int * int, position de l'objet
        scroll : float/int, vitesse de déplacement
        img : sprite"""
        super().__init__()
        self.pos = Vec(position)
        self.scroll = scroll
        # 0 si c'est loin et que ça bouge pas,
        # 1 si c'est près et que ça bouge à la vitesse du sol
        self.image = img
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
