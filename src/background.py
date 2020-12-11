""" Gestion de l'arrière-plan """
import random
import pygame
import src.utilities as ut
import src.conf as cf
import src.sprites as spt


class Nuage(ut.GameObject):
    """Gère les nuages dans l'arrière-plan', par la méthode update(self)"""
    def __init__(self, position, i):
        """ position : int * int, position du nuage
            i : quel type de nuage (y a plusieurs images)"""
        scroll = 0.2*random.random() + 0.1
        img = spt.d["nuage_img"][i]
        super().__init__(position, scroll, img)
        pygame.sprite.Sprite.__init__(self, spt.nuages)

    def update(self):
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH*0.8 and self.pasencorecree:
            i = random.randint(0, spt.d["n_nuage"] - 1)
            pos = (random.randint(cf.SCREEN_WIDTH, int(cf.SCREEN_WIDTH*2)),
                   random.randint(0, cf.SCREEN_HEIGHT // 2))
            Nuage(pos, i)
            self.pasencorecree = False  # On en met un nouveau juste après


class Arbre(ut.GameObject):
    """Gère les arbres dans l'arrière-plan', par la méthode update(self)"""
    def __init__(self, pos_x, i):
        """ pos_x : int, position sur l'axe des x de l'arbre
            i : quel type de nuage (y a plusieurs images)"""
        img = spt.d["arbre_img"][i]
        _, height = img.get_rect().size
        scroll = 0.6
        super().__init__((pos_x, cf.SCREEN_HEIGHT - height), scroll, img)
        pygame.sprite.Sprite.__init__(self, spt.arbres)

    def update(self):
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH*0.8 and self.pasencorecree:
            i = random.randint(0, spt.d["n_arbre"]-1)
            pos_x = random.randint(cf.SCREEN_WIDTH, int(cf.SCREEN_WIDTH*2))
            Arbre(pos_x, i)
            self.pasencorecree = False  # On en met un nouveau juste après
