"""Gestion des commandes"""

import re
import src.conf as cf
from src.conf import State
import src.utilities as ut
import src.player as plyr

FILE = "commands.txt"
"""Fichier des commandes"""

def init_com():
    """Initialiser le fichier des commandes."""
    with open(FILE, "w") as empty_com:
        empty_com.writelines([keyname(key) for key in plyr.JUMP_KEYS])


def get_keys():
    """Récupère les commandes sauvegardées par les utilisateurs"""
    with open(FILE) as coms:
        plyr.JUMP_KEYS = coms.read().splitlines()


def set_keys(keys):
    """
    Changer les commandes du jeu

    Parameters :
    ------------
    keys : array
        Liste des commandes
    """
    plyr.JUMP_KEYS = keys
    with open(FILE, "w") as coms:
        empty_com.writelines([ut.keyname(key)+str("\n") for key in plyr.JUMP_KEYS])
