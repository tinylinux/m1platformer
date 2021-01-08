"""Génération des sprites."""

import os
import rollnjump.conf as cf
import rollnjump.utilities as ut


def listdir(path):
    """
    os.listdir sans les fichiers cachés.

    Parameters
    ----------
    path : str
        Chemin de fichier

    Returns
    -------
    str list
        La liste des fichiers visibles de `path`
    """
    return [f for f in os.listdir(path) if not f.startswith('.')]


# IMAGES
Names = ["cloud", "tree", "item"]
"""Liste des noms des différents éléments de décor."""
for color in cf.COLORS:
    Names.append('mono' + color)
img_dict = {}
"""
Dictionnaire associant, pour chaque élément de `Nom` :
un facteur de taille,
un nombre d'images
et la liste de ces images.
"""
for color in cf.COLORS:
    img_dict['mono' + color + '_factor'] = 1
img_dict["cloud_factor"] = 4
img_dict["tree_factor"] = 8
img_dict["item_factor"] = 2

for name in Names:
    img_dict['n_' + name] = len(listdir(os.path.join(cf.ASSETS, "img", name)))
    img_dict[name + '_img'] = []
    for i in range(img_dict['n_' + name]):
        img = ut.load_image(os.path.join(cf.ASSETS, "img",
                                         name, name + str(i) + ".png"))
        w, h = img.get_rect().size
        img = ut.resize(img, (img_dict[name + '_factor'] * w,
                              img_dict[name + '_factor'] * h))
        img_dict[name + '_img'].append(img)

GROUND_IMG = ut.load_image(os.path.join(cf.ASSETS, "img", "ground.png"))
"""Image pour le sol"""
PLTFRM_IMG = ut.load_image(os.path.join(cf.ASSETS, "img", "pltfrm.png"))
"""Image pour une plateforme métallique"""
BAT_IMG = ut.load_image(os.path.join(cf.ASSETS, "img", "bat.png"))
"""Image pour un bâtiment"""

# Dimensions
for color in cf.COLORS:
    w, h = img_dict["mono" + color + "_img"][0].get_rect().size
    for key in cf.SIZE:
        cf.SIZE[key] = (w * cf.SIZE_FACTOR[key], h * cf.SIZE_FACTOR[key])
    ut.resize_list(img_dict['mono' + color + '_img'], cf.SIZE['normal'])

w, h = GROUND_IMG.get_rect().size
GROUND_HEIGHT = (cf.SCREEN_HEIGHT - h)
"""Hauteur du sol"""
GROUND_WIDTH = w
"""Longueur d'un bloc de sol"""

# Groupes
ground = ut.group_sprite_define()
"""Groupe des éléments du sol"""
clouds = ut.group_sprite_define()
"""Groupe des nuages"""
trees = ut.group_sprite_define()
"""Groupe des arbres"""
items = ut.group_sprite_define()
"""Groupe des objets"""
