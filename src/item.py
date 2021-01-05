"""Gère la génération d'items
    fast : fait accélérer le joueur (sauf après les 2/3 de l'écran)
    slow : fait ralentir le joueur (sauf s'il sort presque de l'écran)
    little : fait rapetisser le joueur
    big : fait grossir le joueur"""

import random as rd
import src.conf as cf
import src.utilities as ut
import src.sprites as spt

NEW_ITEM_TIME = rd.randint(cf.ITEM_PROBA_MIN, cf.ITEM_PROBA_MAX)

ITEMS = ["fast", "slow", "little", "big"]

class item(ut.GameObject):
    """Gère les items"""
    def __init__(self):
        """Crée un item"""
        cf.FLAG_ITEM = True
        i = rd.randint(0, spt.d["n_item"]-1)
        self.type = ITEMS[i]
        img = spt.d["item_img"][i]

        self.width, self.height = img.get_rect().size
        x = cf.SCREEN_WIDTH - self.width
        y = 0

        #Au début il tombe du ciel
        self.vel = ut.Vec(-cf.SPEED, 0)
        self.acc = ut.Vec(0, cf.G)

        super().__init__((x, y), 1, img)
        ut.add_to_group(self, spt.items)

    def update(self):
        """update l'item"""

        self.vel.x = -cf.SPEED
        self.vel += self.acc
        posnext = self.pos + self.vel + 0.5 * self.acc
    	# On regarde si on tombe sur une plateforme
        for plat in spt.ground:
    	    coll = ut.collide(self, self.pos, posnext, plat.rect)
    	    if coll[0] or coll[1]:
    	    	posnext = coll[2]
    	    	self.vel.y = 0
        self.pos = posnext
        self.rect.topleft = self.pos  # Mise à jour de la position
        cf.DISPLAYSURF.blit(self.image, self.rect) # affichage
        # Si on sort de l'écran, on annule le FLAG, on programme un nouvel item et on kill celui-là.
        if (self.pos.y > cf.SCREEN_HEIGHT) or (self.rect.right < 0):
        	cf.FLAG_ITEM = False
        	cf.NEW_ITEM_TIME = cf.SECONDS + rd.randint(cf.ITEM_PROBA_MIN, cf.ITEM_PROBA_MAX)
        	self.kill()


