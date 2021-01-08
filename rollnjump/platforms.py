# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Création et déplacement des plateformes."""
import rollnjump.conf as cf
import rollnjump.utilities as ut
import rollnjump.sprites as spt


class Ground(ut.GameObject):
    """Plateforme initiale (dans le menu)."""

    def __init__(self, position_x):
        """
        Initialisation.

        Parameters
        ----------
        position_x : int
            Abscisse du début de la plateforme
        """
        super().__init__((position_x, spt.GROUND_HEIGHT), 1, spt.GROUND_IMG)

    def update(self):
        """Met à jour la position des plateformes du sol."""
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH and self.FLAG_creation:
            # si le dernier ne couvre plus tout sur la droite,
            # il faut ajouter un nouveau
            plat = Ground(self.rect.right)
            ut.add_to_group(plat, spt.ground)
            self.stop_creation()

    def stop_creation(self):
        """Arrête la génération du sol."""
        self.FLAG_creation = False


class Platform(ut.GameObject):
    """
    Plateformes pendant le jeu.

    Attributes
    ----------
    dim : int * int
        Dimensions de la plateforme
    """

    def __init__(self, pos=(1, 1), dim=(8, 3), img=spt.PLTFRM_IMG):
        """
        Initialisation.

        Parameters
        ----------
        pos : int * int, optionnel
            Position de la plateforme
        dim : int * int, optionnel
            Largeur et hauteur de la plateforme
        img : Surface, optionnel
            Apparence de la plateforme
        """
        self.dim = dim
        img = ut.resize(img, dim)
        super().__init__(pos, 1, img)
