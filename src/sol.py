#Imports
import pygame, sys
from pygame.locals import *
import random, time
 
#Initialisation
pygame.init()
 
#FPS (pour pas que ça aille trop vite)
#FPS = 40
#FramePerSec = pygame.time.Clock()

#Colors
#BLUE  = (0, 0, 255)
#RED   = (255, 0, 0)
#GREEN = (0, 255, 0)
#BLACK = (0, 0, 0)
#WHITE = (255, 255, 255)

#Autres variables
SCREEN_WIDTH = 1000  #largeur fenêtre
SCREEN_HEIGHT = 600 #hauteur fenêtre
SPEED = 5           #vitesse initiale de défilement du sol
SOL_HAUT = (SCREEN_HEIGHT - 117)      #La hauteur du sol en général
SOL_LONG = 609      #La longueur d'un bloc du sol en général
SOL_IMG = "../assets/img/plantes.png"
#LIST_SOL = []   #Contient la liste des plateformes qui sont en ce moment à l'écran

#Écran avec fond
#background = pygame.image.load("../assets/img/fond.jpg")
#DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#pygame.display.set_caption("Game")

#Je crée un groupe de plateformes
sol = pygame.sprite.Group()

class plateforme(pygame.sprite.Sprite): 
    def __init__(self, x=1, y=SOL_HAUT, haut=SOL_HAUT, long=SOL_LONG, image=SOL_IMG, ) :
        super().__init__()
        self.haut = haut
        self.long = long
        self.image = pygame.image.load(image) #Image de la plateforme
        self.surf = pygame.Surface((long, haut))        #Hit-box
        self.rect = self.surf.get_rect(topleft = (x,y))
        pygame.sprite.Sprite.__init__(self, sol)
        #Ajoute notre plateforme au groupe "sol". sol.sprites() est la liste des plateformes

    def move(self):
        self.rect.move_ip(-SPEED,0)
        #Défile à la vitesse SPEED (positive, donc on met un - pour aller à gauche)
        if self.rect.right < 0:     #si on est sorti de l'écran
            self.kill()               #on le supprime
        if SCREEN_WIDTH - self.long < self.rect.right < SCREEN_WIDTH:
            #si le dernier ne couvre plus tout sur la droite, il faut ajouter un nouveau
            plateforme(self.rect.right)    #On en met un nouveau juste après

#initialisation du sol
longueur_totale = 0
while longueur_totale < SCREEN_WIDTH :
    #on rajoute des bouts de sol, on additionne leur longueur
    #et quand on a couvert tout l'écran on s'arrête.
    plateforme(longueur_totale)          #On en met un nouveau à la position x = longueur_totale.
    longueur_totale += SOL_LONG

INC_SPEED = pygame.USEREVENT + 1        #Crée un nouvel event, le +1 sert à avorir un nouvel ID
pygame.time.set_timer(INC_SPEED, 1000)  #Toutes les secondes on augmente la vitesse

#Game Loop
while True :
#    for event in pygame.event.get():  
#        if event.type == INC_SPEED: 
#              SPEED += 0.5      #Augmente la vitesse de 0.5
#        if event.type == QUIT:  #Fin du game si on a l'event QUIT
#            pygame.quit()
#            sys.exit()   
            
    #redessine l'écran        
    DISPLAYSURF.blit(background, (0,0))
    
    for bloc in sol :
        bloc.move()     #On déplace chaque bloc
        DISPLAYSURF.blit(bloc.image, bloc.rect) #affiche l'image du bloc dans sa hitbox
        
    pygame.display.update()
#    FramePerSec.tick(FPS)
