"""Gère la génération d'items."""

import random as rd
import rollnjump.conf as cf
import rollnjump.utilities as ut
import rollnjump.sprites as spt


ITEMS = ["fast", "slow", "little", "big"]
"""
fast : fait accélérer le joueur (sauf après les 2/3 de l'écran)
slow : fait ralentir le joueur (sauf s'il sort presque de l'écran)
little : fait rapetisser le joueur
big : fait grossir le joueur
"""


class Item(ut.GameObject):
    """
    Gestion des objets.

    Attributes
    ----------
    type : str
        Type de l'objet
    width : float
        Largeur de l'objet
    height : float
        Hauteur de l'objet
    vel : float
        Vitesse de l'objet
    acc : float
        Accélération de l'objet
    """

    def __init__(self):
        """Initialisation de l'objet."""
        cf.FLAG_ITEM = True
        i = rd.randint(0, spt.img_dict["n_item"] - 1)
        self.type = ITEMS[i]
        img = spt.img_dict["item_img"][i]

        self.width, self.height = img.get_rect().size
        x = cf.SCREEN_WIDTH - self.width
        y = 0

        # Au début il tombe du ciel
        self.vel = ut.Vec(-cf.SPEED, 0)
        self.acc = ut.Vec(0, cf.G)

        super().__init__((x, y), 1, img)

    def update(self):
        """Met à jour l'item."""
        self.vel.x = -cf.SPEED

        ut.update_pos_vel(self, spt.ground)

        cf.DISPLAYSURF.blit(self.image, self.rect)  # affichage
        # Si on sort de l'écran, on annule le FLAG,
        # on programme un nouvel item et on kill celui-là.
        if (self.pos.y > cf.SCREEN_HEIGHT) or (self.rect.right < 0):
            cf.FLAG_ITEM = False
            cf.NEW_ITEM_TIME = cf.SECONDS + rd.randint(cf.ITEM_PROBA_MIN,
                                                       cf.ITEM_PROBA_MAX)
            self.kill()
