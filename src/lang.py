"""Gestion de la langue."""

import re
import src.conf as cf
from src.conf import State
import src.menu as mn

FILE = "lang.txt"
"""Fichier de langue."""
AVAILABLE = ["fr", "en"]
"""Langues disponibles."""


def init_lang():
    """Initialiser le fichier lang.txt."""
    with open(FILE, "w") as empty_lang:
        empty_lang.write(cf.LANG)


def onlyalphanum(value):
    """
    Fonction ne conservant que les caractères alphanumériques.

    Parameters
    ----------
    value : str
        Chaîne de caractères

    Returns
    -------
    str
        Chaîne de caractères filtrée
    """
    return re.sub(r'[^A-Za-z0-9]+', '', value)


def get_lang():
    """Récupère la langue choisie par l'utilisateur."""
    with open(FILE) as lg:
        lang = lg.readlines()
        if len(lang) > 0 and onlyalphanum(lang[0]) in AVAILABLE:
            cf.LANG = onlyalphanum(lang[0])
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
    cf.LANG = onlyalphanum(lang)
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
    mn.langue_button.changlang(lang)
    mn.commands_button.changlang(lang)
