"""Fonctions pour la boucle principale du jeu."""

import src.conf as cf
from src.conf import State
import src.utilities as ut
import src.menu as mn
import src.worldgen as wrld
import src.player as plyr
import src.lang as lg
import src.score as scre
import src.sprites as spt


def main_loop(players, mouse=None):
    """
    Applique les mises à jour nécessaires au jeu.

    Parameters
    ----------
    players : Player list
        Liste des joueurs

    Returns
    -------
    Player list
        Liste des joueurs actualisée
    """
    if mouse is None:
        mouse = mn.scaled_mouse_pos(ut.mouse_pos())

    if cf.STATE == State.menu:  # On est dans le menu
        cf.DISPLAYSURF.blit(ut.load_image
                            ("assets/img/ui/title.png"), (357, 132))
        for P in players:
            P.move()
        mn.oneplayer_button.print(mouse)
        mn.multiplayer_button.print(mouse)
        mn.settings_button.print(mouse)
        mn.records_button.print(mouse)
        mn.credits_button.print(mouse)

    elif cf.STATE == State.languages:
        cf.DISPLAYSURF.blit(ut.load_image
                            ("assets/img/ui/title.png"), (357, 132))
        for lang in mn.flagbutton:
            lang.print(mouse)

    elif cf.STATE == State.ingame:  # On est en jeu

        # Décompte des secondes
        cf.FRAMES += 1
        if cf.FRAMES % cf.FPS == 0:
            cf.SECONDS += 1
        scre.score(cf.SECONDS)

        # Déplacement des joueurs
        for P in players:
            if P.alive:
                P.move()

        # Gestion de la mort
        nb_player_alive = 0
        for i, P in enumerate(players):
            if P.alive:
                nb_player_alive += 1
                plyr.WINNER = i+1
        if cf.NB_PLAYERS > 1 >= nb_player_alive:
            # Fin du mode multijoueur
            cf.STATE = State.gameover_multi
            cf.NEWHS = scre.maj(cf.SECONDS)
        elif nb_player_alive == 0:
            # Fin du mode solo
            cf.STATE = State.gameover
            cf.NEWHS = scre.maj(cf.SECONDS)

    elif cf.STATE == State.gameover:  # Menu de fin solo

        scre.score_endgame(cf.SECONDS)
        if cf.NEWHS:  # Nouveau record
            cf.DISPLAYSURF.blit(ut.load_image
                                ("assets/img/ui/highscore.png"), (428, 350))
        cf.DISPLAYSURF.blit(ut.load_image
                            ("assets/img/ui/gameover.png"), (395, 100))
        mn.restart_button.print(mouse)
        mn.return_button.print(mouse)

    elif cf.STATE == State.gameover_multi:  # Menu de fin multi

        scre.winner_endgame(plyr.WINNER)

        cf.DISPLAYSURF.blit(ut.load_image
                            ("assets/img/ui/gameover.png"), (395, 100))
        mn.restart_button.print(mouse)
        mn.return_button.print(mouse)

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
        mn.return_button.print(mouse)

    return players


def reset_world():
    """
    Réinitialise le monde.

    Returns
    -------
    Player list
        Une liste de joueurs réinitialisés de longueur NB_PLAYERS
    """
    cf.SPEED = cf.INITIAL_SPEED
    cf.SECONDS = 0
    cf.FRAMES = 0
    spt.ground = ut.group_sprite_define()
    spt.clouds = ut.group_sprite_define()
    spt.trees = ut.group_sprite_define()
    wrld.initgen()
    return [plyr.Player() for _ in range(cf.NB_PLAYERS)]


def event_handling(players, event, mouse=None):
    """
    Permet de gérer les événements.

    Parameters
    ----------
    players : Player list
        Liste des joueurs
    event : Event
        L'événement à traiter

    Returns
    -------
    Player list
        Renvoie la liste des joueurs mis à jour
    """
    if mouse is None:
        mouse = mn.scaled_mouse_pos(ut.mouse_pos())

    if event.type == ut.INC_SPEED:
        if cf.STATE == State.ingame:  # Si on est in game
            cf.SPEED += 0.5

    if event.type == ut.KEYDOWN:
        if cf.STATE == State.ingame:
            for i, P in enumerate(players):
                if event.key == plyr.JUMP_KEYS[i]:  # Saut
                    P.jump()

    if event.type == ut.MOUSEBUTTONDOWN:

        if cf.STATE == State.menu and\
                mn.oneplayer_button.click(mouse):
            # Clic de la souris sur le bouton "Commencer"
            cf.NB_PLAYERS = 1
            players = reset_world()
            cf.STATE = State.ingame
            wrld.stop_ground()  # Arrêt de la création du sol du menu

        elif cf.STATE == State.menu and\
                mn.multiplayer_button.click(mouse):
            # Clic de la souris sur le bouton "Commencer"
            cf.NB_PLAYERS = 3
            players = reset_world()
            cf.STATE = State.ingame
            wrld.stop_ground()  # Arrêt de la création du sol du menu

        elif cf.STATE == State.menu and\
                mn.records_button.click(mouse):
            # Clic de la souris sur le bouton "Records"
            cf.STATE = State.highscore

        elif cf.STATE == State.languages:
            for i in range(len(mn.flagbutton)):
                if mn.flagbutton[i].click(mouse):
                    cf.STATE = State.menu
                    lg.set_lang(lg.AVAILABLE[i])

        elif cf.STATE == State.gameover or\
                cf.STATE == State.gameover_multi:
            if mn.return_button.click(mouse):
                # Clic de la souris sur le bouton "Retour"
                players = reset_world()
                cf.STATE = State.menu
            if mn.restart_button.click(mouse):
                # Clic sur recommencer, on réinitialise le monde
                players = reset_world()
                cf.STATE = State.ingame
                wrld.stop_ground()

        elif cf.STATE == State.highscore and\
                mn.return_button.click(mouse):
            # Clic de la souris sur le bouton "Records"
            cf.STATE = State.menu

    if event.type == ut.VIDEORESIZE:  # pragma: no cover
        ut.resize_window(event.size)

    if event.type == ut.QUIT:  # pragma: no cover
        ut.quit_game()

    return players
