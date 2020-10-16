import pygame
from .conf import *

class plateforme(pygame.sprite.Sprite):
    def __init__(self, x=1, y=SOL_HAUT, haut=SOL_HAUT, long=SOL_LONG, image=SOL_IMG) :
        super().__init__()
        self.haut = haut
        self.long = long
        self.image = pygame.image.load(image) #Image de la plateforme
        self.surf = pygame.Surface((long, haut))        #Hit-box
        self.rect = self.surf.get_rect(topleft = (x,y))
        pygame.sprite.Sprite.__init__(self, sol)
        #Ajoute notre plateforme au groupe "sol". sol.sprites() est la liste des plateformes
        self.pasencorecree = True

    def move(self):
        self.rect.move_ip(-SPEED,0)
        #Défile à la vitesse SPEED (positive, donc on met un - pour aller à gauche)
        if self.rect.right < 0:     #si on est sorti de l'écran
            self.kill()              #on le supprime
        if SCREEN_WIDTH - self.long < self.rect.right < SCREEN_WIDTH and self.pasencorecree:
            #si le dernier ne couvre plus tout sur la droite, il faut ajouter un nouveau
            plateforme(self.rect.right)
            self.pasencorecree = False    #On en met un nouveau juste après
