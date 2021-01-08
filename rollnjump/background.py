# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Gestion de l'arrière-plan."""
import random
import rollnjump.utilities as ut
import rollnjump.conf as cf
import rollnjump.sprites as spt


class Cloud(ut.GameObject):
    """Nuages en arrière-plan."""

    def __init__(self, position, i):
        """
        Initialisation.

        Parameters
        ----------
        position : int * int
            Position du nuage
        i : int
            Type de nuage
        """
        scroll = 0.2 * random.random() + 0.1
        img = spt.img_dict["cloud_img"][i]
        super().__init__(position, scroll, img)
        ut.add_to_group(self, spt.clouds)

    def update(self):
        """Mise à jour du nuage."""
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH * 0.8 and self.FLAG_creation:
            i = random.randint(0, spt.img_dict["n_cloud"] - 1)
            pos = (random.randint(cf.SCREEN_WIDTH, int(cf.SCREEN_WIDTH * 2)),
                   random.randint(0, cf.SCREEN_HEIGHT // 2))
            Cloud(pos, i)
            self.FLAG_creation = False  # On en met un nouveau juste après


class Tree(ut.GameObject):
    """Arbres en arrière-plan."""

    def __init__(self, pos_x, i):
        """
        Initialisation.

        Parameters
        ----------
        pos_x : int
            Abscisse de l'arbre
        i : int
            Type d'arbre
        """
        img = spt.img_dict["tree_img"][i]
        _, height = img.get_rect().size
        scroll = 0.6
        super().__init__((pos_x, cf.SCREEN_HEIGHT - height), scroll, img)
        ut.add_to_group(self, spt.trees)

    def update(self):
        """Mise à jour de l'arbre."""
        super().update()
        if self.rect.right < cf.SCREEN_WIDTH * 0.8 and self.FLAG_creation:
            i = random.randint(0, spt.img_dict["n_tree"] - 1)
            pos_x = random.randint(cf.SCREEN_WIDTH, int(cf.SCREEN_WIDTH * 2))
            Tree(pos_x, i)
            self.FLAG_creation = False  # On en met un nouveau juste après
