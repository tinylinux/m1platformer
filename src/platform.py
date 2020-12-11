""" Gère la création et les déplacements des plateformes """
import pygame
import src.conf as cf
import src.utilities as ut
import src.sprites as spt


class Ground(ut.GameObject):
    """Gestion de la plateforme initiale (menu)"""
    def __init__(self, x):
        super().__init__((x, spt.GROUND_HEIGHT), 1, spt.GROUND_IMG)
        ut.add_to_group(self, spt.ground)

    def update(self):
        """ Fait se déplacer la plateforme selon la variable SPEED du module conf.
        Suprrime la plateforme si celle-ci sort de l'écran, et demande
        la création d'une nouvelle plateforme si nécessaire"""
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH and self.FLAG_creation:
            # si le dernier ne couvre plus tout sur la droite,
            # il faut ajouter un nouveau
            Ground(self.rect.right)
            self.stop_creation()

    def stop_creation(self):
        """Arrête la création de ces plateformes"""
        self.FLAG_creation = False


class Platform(ut.GameObject):
    """ Gère les plateformes """
    def __init__(self, pos=(1, 1), dim=(8, 3), img=spt.PLTFRM_IMG):
        """pos : int * int, position de la plateforme
        dim : int * int, largeur * hauteur de la plateforme
        img : image"""
        img = pygame.transform.scale(img, dim)
        super().__init__(pos, 1, img)
        ut.add_to_group(self, spt.ground)
