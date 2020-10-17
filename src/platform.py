import pygame
import src.conf as cf

class plateforme(pygame.sprite.Sprite):
    def __init__(self, x = 1, y = cf.SOL_HAUT, haut = cf.SOL_HAUT, length = cf.SOL_LONG, image = cf.SOL_IMG):
        super().__init__()
        self.haut = haut
        self.length = length
        self.image = pygame.image.load(image) #Image de la plateforme
        self.surf = pygame.Surface((length, haut))        #Hit-box
        self.rect = self.surf.get_rect(topleft = (x,y))
        pygame.sprite.Sprite.__init__(self, cf.sol)
        #Ajoute notre plateforme au groupe "sol". sol.sprites() est la liste des plateformes
        self.pasencorecree = True

    def move(self):
        print(cf.SPEED)
        self.rect.move_ip(-cf.SPEED, 0)
        #Défile à la vitesse SPEED (positive, donc on met un - pour aller à gauche)
        if self.rect.right < 0:     #si on est sorti de l'écran
            self.kill()              #on le supprime
        if cf.SCREEN_WIDTH - self.length < self.rect.right < cf.SCREEN_WIDTH and self.pasencorecree:
            #si le dernier ne couvre plus tout sur la droite, il faut ajouter un nouveau
            plateforme(self.rect.right)
            self.pasencorecree = False    #On en met un nouveau juste après
