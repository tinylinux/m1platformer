"""Fonctions pour la boucle principale du jeu."""

import time
import random as rd
import src.conf as cf
from src.conf import State
import src.utilities as ut
import src.menu as mn
import src.worldgen as wrld
import src.player as plyr
import src.score as scre
import src.sprites as spt


def main_loop(players, graphical):
    """
    Applique les mises à jour nécessaires au jeu.

    Parameters
    ----------
    players : Player list
        Liste des joueurs
    graphical : bool
        Indique si le jeu est en mode graphique ou non

    Returns
    -------
    Player list
        Liste des joueurs actualisée
    """
    if cf.STATE == State.menu:  # On est dans le menu
        cf.DISPLAYSURF.blit(ut.load_image
                            ("assets/img/ui/title.png"), (357, 132))
        for P in players:
            P.move()
        if graphical:
            mn.start_button.print(ut.mouse_pos())
            mn.records_button.print(ut.mouse_pos())

    elif cf.STATE == State.ingame:  # On est en jeu

        # Décompte des secondes
        cf.FRAMES += 1
        if cf.FRAMES % cf.FPS == 0:
            cf.SECONDS += 1
        scre.score(cf.SECONDS)

        # Déplacement des joueurs
        for P in players:
            P.move()

        # Gestion de la mort
        for P in players:
            if P.death():
                cf.STATE = State.gameover
                cf.NEWHS = scre.maj(cf.SECONDS)

    elif cf.STATE == State.gameover:  # Menu de fin

        scre.score_endgame(cf.SECONDS)
        if cf.NEWHS:  # Nouveau record
            cf.DISPLAYSURF.blit(ut.load_image
                                ("assets/img/ui/highscore.png"), (428, 350))
        cf.DISPLAYSURF.blit(ut.load_image
                            ("assets/img/ui/gameover.png"), (395, 100))
        if graphical:
            mn.restart_button.print(ut.mouse_pos())
            mn.return_button.print(ut.mouse_pos())

    elif cf.STATE == State.highscore:  # Affichage des meilleurs scores

        # Récupération des meilleurs scores
        records = scre.get_scores()
        number_scores = len(records)
        font_size = cf.HIGHTSCORES_FONT_SIZE
        size_height = font_size * 2 * number_scores
        if number_scores == 0:
            mn.print_text("Pas de scores", (640, 360), cf.GREY,
                          ut.font(mn.FONT_PIXEL, font_size),
                          True)
        else:
            for best_score in range(number_scores):
                position_score = 10 * font_size - (size_height // 2)\
                                + best_score * 2 * font_size + font_size // 2
                text_display = records[best_score][1] + " : "
                text_display += str(records[best_score][0])
                mn.print_text(text_display,
                              (640, position_score), cf.GREY,
                              ut.font(mn.FONT_PIXEL, font_size),
                              True)
        mn.return_button.print(ut.mouse_pos())

    return players


def set_seed(seed=None):
    """
    Initialise la graine pour le module random.

    Parameters
    ----------
    seed : int, optionnel
        Valeur imposée
    """
    if seed is None:
        seed = int(time.time())
    cf.SEED = seed
    rd.seed(seed)


def reset_world(nb_players=1):
    """
    Réinitialise le monde.

    Parameters
    ----------
    nb_player : int, optionnel
        Nombre de joueurs dans le jeu (1 par défaut)

    Returns
    -------
    Player list
        Une liste de joueurs réinitialisés de longueur nb_players
    """
    cf.SPEED = cf.INITIAL_SPEED
    cf.SECONDS = 0
    cf.FRAMES = 0
    spt.ground = ut.group_sprite_define()
    spt.clouds = ut.group_sprite_define()
    spt.trees = ut.group_sprite_define()
    set_seed()
    wrld.initgen()
    return [plyr.Player() for _ in range(nb_players)]


def event_handling(players, event, graphical):
    """
    Permet de gérer les événements.

    Parameters
    ----------
    players : Player list
        Liste des joueurs
    event : Event
        L'événement à traiter
    graphical : bool
        Indique si le jeu est en mode graphique ou non

    Returns
    -------
    Player list
        Renvoie la liste des joueurs mis à jour
    """
    if event.type == ut.INC_SPEED:
        if cf.STATE == State.ingame:  # Si on est in game
            cf.SPEED += 0.5

    if graphical:
        if event.type == ut.KEYDOWN:
            if cf.STATE == State.ingame and event.key == ut.K_SPACE:  # Saut
                players[0].jump()

        if event.type == ut.MOUSEBUTTONDOWN:

            if cf.STATE == State.menu and\
                    mn.start_button.click(ut.mouse_pos()):
                # Clic de la souris sur le bouton "Commencer"
                cf.STATE = State.ingame
                wrld.stop_ground()  # Arrêt de la création du sol du menu

            elif cf.STATE == State.menu and\
                    mn.records_button.click(ut.mouse_pos()):
                # Clic de la souris sur le bouton "Records"
                cf.STATE = State.highscore

            elif cf.STATE == State.gameover:
                if mn.return_button.click(ut.mouse_pos()):
                    # Clic de la souris sur le bouton "Retour"
                    players = reset_world(len(players))
                    cf.STATE = State.menu
                if mn.restart_button.click(ut.mouse_pos()):
                    # Clic sur recommencer, on réinitialise le monde
                    players = reset_world(len(players))
                    cf.STATE = State.ingame
                    wrld.stop_ground()

            elif cf.STATE == State.highscore and\
                    mn.return_button.click(ut.mouse_pos()):
                # Clic de la souris sur le bouton "Records"
                cf.STATE = State.menu

        if event.type == ut.VIDEORESIZE:
            ut.resize_window(event.size)

    if event.type == ut.QUIT:
        ut.quit_game()

    return players
