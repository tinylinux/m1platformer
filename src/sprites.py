"""Génération des sprites."""

import os
import src.conf as cf
import src.utilities as ut


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


localdir = os.path.dirname(__file__)
"""Chemin du répertoire local"""

# IMAGES
Nom = ["mono", "cloud", "tree", "item"]
"""Liste des noms des différents éléments de décor"""
img_dict = {}
"""Dictionnaire associant, pour chaque élément de `Nom` :
un facteur de taille,
un nombre d'images
et la liste de ces images."""
img_dict["mono_factor"] = 1
img_dict["cloud_factor"] = 4
img_dict["tree_factor"] = 8
img_dict["item_factor"] = 2

for nom in Nom:
    img_dict['n_' + nom] = len(listdir(os.path.join(localdir, "..", "assets",
                                       "img", nom)))
    img_dict[nom + '_img'] = []
    for i in range(img_dict['n_' + nom]):
        img = ut.load_image(os.path.join(localdir, "..", "assets", "img",
                                         nom, nom + str(i) + ".png"))
        w, h = img.get_rect().size
        img = ut.resize(img, (img_dict[nom + '_factor'] * w,
                              img_dict[nom + '_factor'] * h))
        img_dict[nom + '_img'].append(img)

GROUND_IMG = ut.load_image(os.path.join(localdir, "..", "assets",
                                        "img", "ground.png"))
"""Image pour le sol"""
PLTFRM_IMG = ut.load_image(os.path.join(localdir, "..", "assets",
                                        "img", "pltfrm.png"))
"""Image pour une plateforme métallique"""
BAT_IMG = ut.load_image(os.path.join(localdir, "..", "assets",
                                     "img", "bat.png"))
"""Image pour un bâtiment"""

# Dimensions
w, h = img_dict["mono_img"][0].get_rect().size
for key in cf.SIZE:
    cf.SIZE[key] = (w*cf.SIZE[key], h*cf.SIZE[key])
ut.resize_list(img_dict['mono_img'], cf.SIZE['normal'])
"""Les différentes dimensions du joueur (normal, big, little)"""

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
