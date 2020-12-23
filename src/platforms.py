"""Création et déplacement des plateformes."""
import src.conf as cf
import src.utilities as ut
import src.sprites as spt


class Ground(ut.GameObject):
    """Plateforme initiale (dans le menu)."""

    def __init__(self, x):
        """
        Initialisation.

        Parameters
        ----------
        x : int
            Abscisse du début de la plateforme
        """
        super().__init__((x, spt.GROUND_HEIGHT), 1, spt.GROUND_IMG)
        ut.add_to_group(self, spt.ground)

    def update(self):
        """Met à jour la position des plateformes du sol."""
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH and self.FLAG_creation:
            # si le dernier ne couvre plus tout sur la droite,
            # il faut ajouter un nouveau
            Ground(self.rect.right)
            self.stop_creation()

    def stop_creation(self):
        """Arrête la génération du sol."""
        self.FLAG_creation = False


class Platform(ut.GameObject):
    """Plateformes pendant le jeu."""

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
        ut.add_to_group(self, spt.ground)
