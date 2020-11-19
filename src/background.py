""" Gestion de l'arrière-plan """
import random
import pygame
import src.conf as cf


class Nuage(cf.GameObject):
    def __init__(self, position, i):
        super().__init__(position, 0.2*random.random() + 0.1, cf.nuage_img[i])
        pygame.sprite.Sprite.__init__(self, cf.nuages)

    def update(self):
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH*0.8 and self.pasencorecree:
            i = random.randint(0, cf.n_nuage - 1)
            pos = (random.randint(cf.SCREEN_WIDTH, int(cf.SCREEN_WIDTH*2)),
                   random.randint(0, cf.SCREEN_HEIGHT // 2))
            Nuage(pos, i)
            self.pasencorecree = False  # On en met un nouveau juste après


class Arbre(cf.GameObject):
    def __init__(self, pos_x, i):
        img = cf.arbre_img[i]
        _, height = img.get_rect().size
        super().__init__((pos_x, cf.SCREEN_HEIGHT - height), 0.6, img)
        pygame.sprite.Sprite.__init__(self, cf.arbres)

    def update(self):
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH*0.8 and self.pasencorecree:
            i = random.randint(0, cf.n_arbre-1)
            pos_x = random.randint(cf.SCREEN_WIDTH, int(cf.SCREEN_WIDTH*2))
            Arbre(pos_x, i)
            self.pasencorecree = False  # On en met un nouveau juste après
