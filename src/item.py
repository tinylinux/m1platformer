"""Gère la génération d'items
    fast : fait accélérer le joueur (sauf après les 2/3 de l'écran)
    slow : fait ralentir le joueur (sauf s'il sort presque de l'écran)
    big : fait grossir le joueur
    little : fait rapetisser le joueur"""

import random as rd
import src.conf as cf
import src.utilities as ut
import src.sprites as spt

# proba de faire apparaître nouvel item sur une plateforme
# (par ex: 1 chance sur 10)
PROBA = 1 #10

ITEMS = ["fast", "slow", "little", "big"]

class item(ut.GameObject):
    """Gère les items"""
    def __init__(self, plt):
        """Crée un item sur une plateforme
            plt : plateforme sur laquelle apparait l'item"""
        cf.FLAG_ITEM = False #True
        i = rd.randint(0, spt.d["n_item"]-1)
        self.type = ITEMS[i]
        img = spt.d["item_img"][i]

        w, h = img.get_rect().size
        x_plt, y_plt = plt.pos
        dx = plt.dim[0]  # longueur de la plateforme
        x = rd.randint(x_plt, x_plt+dx-w)
        y = y_plt-h

        super().__init__((x, y), 1, img)
        ut.add_to_group(self, spt.items)

    def update(self):
        """update l'item"""
        super().update()
        if self.rect.left < cf.SPEED:  # Si l'item va sortir de l'écran bientôt
            cf.FLAG_ITEM = False     # On annule le cf.FLAG_ITEM
