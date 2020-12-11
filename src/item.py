""" Gère la génération d'items"""

import random as rd
import pygame


import src.conf as cf

# Flag : true si y a un item à l'écran
# ou qu'on est dans un état spécial à cause d'un item
FLAG_ITEM = False

# proba de faire apparaître nouvel item sur un plateforme
proba = 2

ITEMS = ["fast","slow","big","little"]

class item(cf.GameObject):
    """Gère les items
        i = n° d'item :
            0 = fast
            1 = slow
            2 = big
            3 = little"""
    def __init__(self, plt):
        """Crée un item sur une plateforme
            plt : plateforme sur laquelle apparait l'item"""
        cf.FLAG_ITEM = True
        i = rd.randint(0, cf.d["n_item"]-1)
        self.type = ITEMS[i]
        img = cf.d["item_img"][i]
        w,h = img.get_rect().size

        x_plt,y_plt = plt.pos
        dx = plt.dim[0] # longueur de la plateforme
        x = rd.randint(x_plt,x_plt+dx-w)
        y = y_plt-h

        super().__init__((x,y), 1, img)
        pygame.sprite.Sprite.__init__(self, cf.items)

    def update(self):
        """update l'item"""
        super().update()
        if self.rect.left<cf.SPEED: # Si l'item va sortir de l'écran bientôt
            cf.FLAG_ITEM=False      # On annule le cf.FLAG_ITEM

