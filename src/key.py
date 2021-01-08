"""Gestion des commandes."""

import src.conf as cf
import src.utilities as ut
import src.menu as mn
import src.player as plyr

FILE = "commands.txt"
"""Fichier des commandes"""

TEXTCAPT = {
    "fr": "Capture de la touche pour le joueur : ",
    "en": "Key capture for player : "
}


def init_com():
    """Initialiser le fichier des commandes."""
    with open(FILE, "w") as empty_com:
        empty_com.writelines([ut.keyname(key)
                              + "\n" for key in plyr.JUMP_KEYS])


def get_keys():
    """Récupère les commandes sauvegardées par les utilisateurs."""
    with open(FILE) as coms:
        plyr.JUMP_KEYS = [ut.keyidentifier(i)
                          for i in coms.read().splitlines()]


def set_keys(keys):
    """
    Changer les commandes du jeu.

    Parameters :
    ------------
    keys : array
        Liste des commandes
    """
    plyr.JUMP_KEYS = keys
    with open(FILE, "w") as coms:
        coms.writelines([ut.keyname(key)
                         + str("\n") for key in plyr.JUMP_KEYS])


Modify_size = (100, 100)
Modify_pos = [(900, 85 + i * 150) for i in range(cf.NB_PLAYERS_MAX)]
Modify_idle = "modify.png"
Modify_hover = "modifypushed.png"
modifybutton = []
"""Liste des boutons de modification."""
for i in range(cf.NB_PLAYERS_MAX):
    modifybutton.append(
        mn.ButtonImage(
            Modify_pos[i],
            Modify_size,
            Modify_idle,
            Modify_hover
        )
    )
