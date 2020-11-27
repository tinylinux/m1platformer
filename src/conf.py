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


#IMAGES
d = {}
Nom = ["mono","nuage","arbre"]
d["mono_factor"] = 3
d["nuage_factor"] = 4
d["arbre_factor"] = 8
for nom in Nom :
    d['n_'+nom] = len(listdir("./assets/img/"+nom))
    d[nom+'_img'] = []
    for i in range(d['n_'+nom]):
        img = pygame.image.load("assets/img/"+nom+"/"+nom+str(i)+".png")
        w, h = img.get_rect().size
        img = pygame.transform.scale(img, (d[nom+'_factor']*w,d[nom+'_factor']*h))
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
