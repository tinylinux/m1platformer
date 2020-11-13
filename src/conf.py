""" Stocke des variables partagées entre les différents fichiers """
import pygame, os
vec = pygame.math.Vector2



SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0

def update_window_size():
    global WINDOW_HEIGHT, WINDOW_WIDTH
    ch, cw = pygame.display.Info().current_h, pygame.display.Info().current_w
    if ch * 16 > cw * 9:
        WINDOW_WIDTH = cw
        WINDOW_HEIGHT = 9 * cw
    else:
        WINDOW_HEIGHT = ch
        WINDOW_WIDTH = 16 * ch

INITIAL_SPEED = 1
SPEED = INITIAL_SPEED           # vitesse initiale de défilement du sol

BlueSky = (0,170,251)

#IMAGES
n_mono = len(os.listdir("./assets/img/mono")) - 1
mono_img = []
for i in range(n_mono) :
    mono_img.append(pygame.image.load("assets/img/mono/Mono"+str(i)+".png"))

n_nuage = len(os.listdir("./assets/img/nuages")) - 1
nuage_img = []
for i in range(n_nuage) :
    nuage_img.append(pygame.image.load("assets/img/nuages/nuage"+str(i)+".png"))
    
n_arbre = len(os.listdir("./assets/img/arbres")) - 1
arbre_img = []
for i in range(n_arbre) :
    arbre_img.append(pygame.image.load("assets/img/arbres/Arbre"+str(i)+".png"))
    
SOL_IMG = pygame.image.load("assets/img/sol.png")
PLTFRM_IMG = pygame.image.load("assets/img/pltfrm.png")
BAT_IMG = pygame.image.load("assets/img/bat.png")

# Dimensions
p_WIDTH,p_HEIGHT = mono_img[0].get_rect().size
w,h = SOL_IMG.get_rect().size
SOL_HAUT = (SCREEN_HEIGHT - h)      # La hauteur du sol en général
SOL_LONG = w      # La longueur d'un bloc du sol en général

sol = pygame.sprite.Group()
nuages = pygame.sprite.Group()
arbres = pygame.sprite.Group()

DISPLAYSURF = pygame.display.set_mode((1280, 720))
WINDOWSURF = None


class GameObject(pygame.sprite.Sprite):
    """Utilisé pour tous les objets du monde, genre le sol, les plateformes,
        les nuages, les bâtiments, etc. qui se déplacent de droite à gauche"""
    def __init__(self,x,y,scroll,img):
        super().__init__()
        self.pos = vec((x,y))
        self.scroll = scroll
        # 0 si c'est loin et que ça bouge pas,
        # 1 si c'est près et que ça bouge à la vitesse du sol
        self.image = img
        self.rect = self.image.get_rect(topleft = self.pos)
        #limite à partir de laquelle on génère un nouvel objet sur sa droite
        #pasencorecree est un flag pour ne génèrer qu'un seul nouvel objet
        self.pasencorecree = True
        
    def update(self):
        """Modifie le vecteur position"""
        posnext = self.pos + self.scroll*vec(-SPEED, 0)
        self.pos = posnext
        self.rect.topleft = self.pos
        if self.rect.right < 0:     # si on est sorti de l'écran
            self.kill()              # on le supprime
        #On update l'image
        DISPLAYSURF.blit(self.image, self.rect)