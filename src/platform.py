""" Gère la création et les déplacements des plateformes """
import pygame
import src.conf as cf

class Sol(cf.GameObject):
    def __init__(self,x):
        super().__init__(x,cf.SOL_HAUT,1,cf.SOL_IMG)
        pygame.sprite.Sprite.__init__(self, cf.sol)
        
    def update(self):
        """ Fait se déplacer la plateforme selon la variable SPEED du module conf.
        Suprrime la plateforme si celle-ci sort de l'écran, et demande
        la création d'une nouvelle plateforme si nécessaire"""
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH and self.pasencorecree:
            # si le dernier ne couvre plus tout sur la droite,
            # il faut ajouter un nouveau
            Sol(self.rect.right)
            self.stop_creation()
    def stop_creation(self):
         self.pasencorecree = False


class Platform(cf.GameObject):
    """ Gère les plateformes """
    def __init__(self, x=1, y=1, haut=3,length=8, img=cf.PLTFRM_IMG):
        img = pygame.transform.scale(img, (length, haut))
        super().__init__(x,y,1,img)
        pygame.sprite.Sprite.__init__(self, cf.sol)


class Batiment(Platform):
    def __init__(self, x=1, y=1, haut=cf.SCREEN_HEIGHT, length=8, image=cf.BAT_IMG):
        super().__init__(x, y, haut,length, image)

