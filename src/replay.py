"""Gestion de l'enregistrement des parties."""

import src.conf as cf

FILE = "replay.txt"
"""Fichier contenant l'enregistrement"""

JUMPS = []
"""Sauts enregistrés dans le replay"""


def init_replay():
    """Initialisation du fichier d'enregistrement."""
    with open(FILE, "w") as replay:
        replay.write(str(cf.SEED) + "\n")


def add_jump(time):
    """
    Ajout d'un saut au fichier d'enregistrement.

    Parameters
    ----------
    time : int
        Nombre de frames depuis le début de la partie
    """
    with open(FILE, "a") as replay:
        replay.write(str(time) + "\n")


def start_replay():
    global JUMPS
    with open(FILE, "r") as replay:
        lines = replay.readlines()
    lines = [int(line.strip('\n')) for line in lines]
    seed = lines[0]
    JUMPS = lines[1:]
    return seed
