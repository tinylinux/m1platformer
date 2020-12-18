"""Génération des sprites"""

import os
import src.conf as cf
import src.utilities as ut


def listdir(path):
    """listdir sans fichiers cachés (genre les .DS_Store)"""
    return [f for f in os.listdir(path) if not f.startswith('.')]


localdir = os.path.dirname(__file__)

# IMAGES
d = {}
Nom = ["mono", "cloud", "tree", "item"]
d["mono_factor"] = 1
d["cloud_factor"] = 4
d["tree_factor"] = 8
d["item_factor"] = 2
for nom in Nom:
    d['n_' + nom] = len(listdir(os.path.join(localdir, "..", "assets",
                                "img", nom)))
    d[nom + '_img'] = []
    for i in range(d['n_' + nom]):
        img = ut.load_image(os.path.join(localdir, "..", "assets", "img",
                                         nom, nom + str(i) + ".png"))
        w, h = img.get_rect().size
        img = ut.resize(img, (d[nom + '_factor'] * w,
                              d[nom + '_factor'] * h))
        d[nom + '_img'].append(img)

GROUND_IMG = ut.load_image(os.path.join(localdir, "..", "assets",
                                        "img", "ground.png"))
PLTFRM_IMG = ut.load_image(os.path.join(localdir, "..", "assets",
                                        "img", "pltfrm.png"))
BAT_IMG = ut.load_image(os.path.join(localdir, "..", "assets",
                                     "img", "bat.png"))

# Dimensions
w, h = GROUND_IMG.get_rect().size
GROUND_HEIGHT = (cf.SCREEN_HEIGHT - h)  # La hauteur du sol
GROUND_WIDTH = w      # La longueur d'un bloc du sol

w, h = d["mono_img"][0].get_rect().size
for key in cf.SIZE:
    cf.SIZE[key] = (w*cf.SIZE[key], h*cf.SIZE[key])
ut.resize_list(d['mono_img'], cf.SIZE['normal'])

# Groupes
ground = ut.group_sprite_define()
clouds = ut.group_sprite_define()
trees = ut.group_sprite_define()
items = ut.group_sprite_define()
