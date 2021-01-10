# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Gestion des commandes."""

from os.path import join
import rollnjump.conf as cf
import rollnjump.utilities as ut
import rollnjump.menu as mn
import rollnjump.player as plyr

FILE = join(cf.CONFDIR, "commands.txt")
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
    keys : int list
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
