""" Gère la création et les déplacements des plateformes """
import src.conf as cf
import src.utilities as ut
import src.sprites as spt


class Sol(ut.GameObject):
    """Gestion de la plateforme initiale (menu)"""
    def __init__(self, x):
        super().__init__((x, spt.SOL_HAUT), 1, spt.SOL_IMG)
        ut.add_to_group(self, spt.sol)

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
        """Arrête la création de ces plateformes"""
        self.pasencorecree = False


class Platform(ut.GameObject):
    """ Gère les plateformes """
    def __init__(self, pos=(1, 1), dim=(8, 3), img=spt.PLTFRM_IMG):
        """pos : int * int, position de la plateforme
        dim : int * int, largeur * hauteur de la plateforme
        img : image"""
        img = ut.resize(img, dim)
        super().__init__(pos, 1, img)
        ut.add_to_group(self, spt.sol)
