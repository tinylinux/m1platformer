"""Gestion de la langue"""

import re
import src.conf as cf
from src.conf import State

FILE = "lang.txt"
AVAILABLE = ["fr", "en"]


def init_lang():
    """
    Initialiser le fichier lang.txt
    """
    with open(FILE, "w") as empty_lang:
        empty_lang.write(cf.LANG)


def onlyalphanum(value):
    """
    Fonction qui permet de filtrer uniquement les caractères
    alphanumériques (pour la langue)

    Entrée :
    --------
    value : <string>
        Chaîne de caractères

    Sortie :
    --------
    <string>
        Chaîne de caractères filtrée
    """
    return re.sub(r'[^A-Za-z0-9]+', '', value)


def get_lang():
    """
    Récupérer la langue choisie par l'utilisateur
    """
    with open(FILE) as lg:
        lang = lg.readlines()
        if len(lang) > 0 and onlyalphanum(lang[0]) in AVAILABLE:
            cf.LANG = onlyalphanum(lang[0])
        else:
            cf.STATE = State.languages
            cf.LANG = ""


def set_lang(lang):
    """
    Changer la langue du jeu

    Entrée :
    --------
    lang :  <string>
        Langue choisie par l'utilisateur
    """
    cf.LANG = onlyalphanum(lang)
    with open(FILE, "w") as empty_lang:
        empty_lang.write(cf.LANG)
