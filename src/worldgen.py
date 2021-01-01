"""Gère la génération du monde."""

import os
import random as rd
# Import classes
import src.sprites as spt
import src.platforms as pltfrm
import src.conf as cf
import src.background as bg
import src.item as it

rd_map = rd.Random(0)


# Indexation des modules
localdir = os.path.dirname(__file__)
"""Chemin du répertoire local"""
modules = spt.listdir(os.path.join(localdir, "modules"))
modules = [file.split("_") for file in modules]
modules = [[int(mod[0]), int(mod[1]), mod[2]] for mod in modules]
"""Liste des modules"""

MAX_JUMP = 200
"""Hauteur maximale entre la dernière plateforme d'un module
et la première plateforme du suivant"""

FLAG_CREATION = False
"""Drapeau indiquant si la création des modules a débuté"""


# Fonctions de création
def platform_creation(bloc, xoffset, yoffset):
    """
    Crée une plateforme.

    Parameters
    ----------
    bloc : str list
        Liste des chaînes de caractères définissant la plateforme
    xoffset : int
        Décalage en abscisses du module
    yoffset : int
        D&calage en ordonnées du module
    """
    top_left = bloc[1][1:-1].split(',')
    top_left_y, top_left_x = int(top_left[0]), int(top_left[1])
    bot_right = bloc[2][1:-2].split(',')
    bot_right_y, bot_right_x = int(bot_right[0]), int(bot_right[1])
    return pltfrm.Platform((top_left_x + xoffset,
                            top_left_y + yoffset),
                           (bot_right_x - top_left_x,
                            bot_right_y - top_left_y),
                           spt.PLTFRM_IMG)


def batiment_creation(bloc, xoffset, yoffset):
    """
    Crée un bâtiment.

    Parameters
    ----------
    bloc : str list
        Liste des chaînes de caractères définissant le bâtiment
    xoffset : int
        Décalage en abscisses du module
    yoffset : int
        D&calage en ordonnées du module
    """
    top_left = bloc[1][1:-1].split(',')
    top_left_y, top_left_x = int(top_left[0]), int(top_left[1])
    bot_right = bloc[2][1:-2].split(',')
    bot_right_x = int(bot_right[1])
    return pltfrm.Platform((top_left_x + xoffset,
                            top_left_y + yoffset),
                           (bot_right_x - top_left_x,
                            cf.SCREEN_HEIGHT),
                           spt.BAT_IMG)


creation_functions = {"Plateforme": platform_creation,
                      "Batiment": batiment_creation}


def initgen():
    """Initialise le monde."""
    # Crée quelques nuages
    for _ in range(4):
        pos = (bg.rd_back.randint(0, cf.SCREEN_WIDTH),
               bg.rd_back.randint(0, cf.SCREEN_HEIGHT // 2))
        i = bg.rd_back.randint(0, spt.img_dict["n_cloud"] - 1)
        bg.Cloud(pos, i)
    # Crée quelques arbres
    for _ in range(4):
        pos_x = bg.rd_back.randint(0, cf.SCREEN_WIDTH)
        i = bg.rd_back.randint(0, spt.img_dict["n_tree"] - 1)
        bg.Tree(pos_x, i)

    # Lance la création du sol
    # on rajoute des bouts de sol, on additionne leur longueur
    # et quand on a couvert tout l'écran on s'arrête.
    longueur_totale = 0
    while longueur_totale < cf.SCREEN_WIDTH:
        # On en met un nouveau à la position x = longueur_totale.
        pltfrm.Ground(longueur_totale)
        longueur_totale += spt.GROUND_WIDTH


def genere_module(last_pltfrm):
    """
    Choisit et affiche un nouveau module à la fin de l'écran.

    Parameters
    ----------
    last_pltfrm : Plateform
        Dernière plateforme du module en cours
    """
    global FLAG_CREATION
    # Mise à jour du drapeau si nécessaire
    FLAG_CREATION = True

    # Offset dépendant de la vitesse
    module_offset = cf.SPEED * 10
    xoffset = cf.SPEED * 10
    # Début du nouveau module
    xoffset = last_pltfrm.rect.right + module_offset
    # Sélection des modules possibles
    modules_possibles = [mod for mod in modules
                         if last_pltfrm.rect.top - mod[0] < MAX_JUMP]
    # Choix aléatoire d'un module
    module = rd_map.choice(modules_possibles)
    # Chargement du module
    module_name = '_'.join([str(module[0]), str(module[1]), module[2]])
    module_file = open("./src/modules/" + module_name, "r")
    lines = module_file.readlines()
    module_height = int(lines[0])
    yoffset = cf.SCREEN_HEIGHT - module_height
    for line in lines[1:]:
        bloc = line.split(';')
        bloc_type = bloc[0]
        # xoffset += pltfrm_offset
        plt = creation_functions[bloc_type](bloc, xoffset, yoffset)
        # avec une chance sur 5 on fait apparaître un nouvel item
        if rd_map.randint(1, it.proba) == 1 and (not cf.FLAG_ITEM):
            it.item(plt)
    module_file.close()


def stop_ground():
    """Arrête la création infinie du sol."""
    for bloc in spt.ground:
        if isinstance(bloc, pltfrm.Ground):
            bloc.stop_creation()


def update():
    """Met à jour tous les objets du monde autres que Player."""
    cf.DISPLAYSURF.fill(cf.BlueSky)  # Le ciel
    spt.clouds.update()
    spt.trees.update()
    spt.ground.update()
    spt.items.update()

    last_pltfrm = max(spt.ground, key=lambda bloc: bloc.rect.right)
    if last_pltfrm.rect.right < cf.SCREEN_WIDTH:
        genere_module(last_pltfrm)
