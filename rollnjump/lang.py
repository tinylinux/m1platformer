# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Gestion de la langue."""

import rollnjump.utilities as ut
import rollnjump.conf as cf
from rollnjump.conf import State
import rollnjump.menu as mn

FILE = "lang.txt"
"""Fichier de langue."""
AVAILABLE = ["fr", "en"]
"""Langues disponibles."""


def init_lang():
    """Initialiser le fichier lang.txt."""
    with open(FILE, "w") as empty_lang:
        empty_lang.write(cf.LANG)


def get_lang():
    """Récupère la langue choisie par l'utilisateur."""
    with open(FILE) as lg:
        lang = lg.readlines()
        if len(lang) > 0 and ut.onlyalphanum(lang[0]) in AVAILABLE:
            cf.LANG = ut.onlyalphanum(lang[0])
            changbuttonslang(cf.LANG)
        else:
            cf.STATE = State.languages
            cf.LANG = ""


def set_lang(lang):
    """
    Change la langue du jeu.

    Parameters
    ----------
    lang : str
        Langue choisie par l'utilisateur
    """
    cf.LANG = ut.onlyalphanum(lang)
    changbuttonslang(cf.LANG)
    with open(FILE, "w") as empty_lang:
        empty_lang.write(cf.LANG)


def changbuttonslang(lang):
    """
    Change l'ensemble des boutons après avoir changé la langue.

    Parameters
    ----------
    lang : str
        Langue à mettre
    """
    mn.restart_button.changlang(lang)
    mn.language_button.changlang(lang)
    mn.commands_button.changlang(lang)
