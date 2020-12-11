""" Gestion de l'arrière-plan """
import random
import pygame
import src.utilities as ut
import src.conf as cf
import src.sprites as spt
import src.utilities as ut


class Cloud(ut.GameObject):
    """Gère les nuages dans l'arrière-plan', par la méthode update(self)"""
    def __init__(self, position, i):
        """ position : int * int, position du nuage
            i : quel type de nuage (y a plusieurs images)"""
        scroll = 0.2*random.random() + 0.1
        img = spt.d["cloud_img"][i]
        super().__init__(position, scroll, img)
        ut.add_to_group(self, spt.clouds)

    def update(self):
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH*0.8 and self.FLAG_creation:
            i = random.randint(0, spt.d["n_cloud"] - 1)
            pos = (random.randint(cf.SCREEN_WIDTH, int(cf.SCREEN_WIDTH*2)),
                   random.randint(0, cf.SCREEN_HEIGHT // 2))
            Cloud(pos, i)
            self.FLAG_creation = False  # On en met un nouveau juste après


class Tree(ut.GameObject):
    """Gère les arbres dans l'arrière-plan', par la méthode update(self)"""
    def __init__(self, pos_x, i):
        """ pos_x : int, position sur l'axe des x de l'arbre
            i : quel type de nuage (y a plusieurs images)"""
        img = spt.d["tree_img"][i]
        _, height = img.get_rect().size
        scroll = 0.6
        super().__init__((pos_x, cf.SCREEN_HEIGHT - height), scroll, img)
        ut.add_to_group(self, spt.trees)

    def update(self):
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH*0.8 and self.FLAG_creation:
            i = random.randint(0, spt.d["n_tree"]-1)
            pos_x = random.randint(cf.SCREEN_WIDTH, int(cf.SCREEN_WIDTH*2))
            Tree(pos_x, i)
            self.FLAG_creation = False  # On en met un nouveau juste après
