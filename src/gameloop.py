"""Fonctions pour la boucle principale du jeu."""

import os
import random as rd
import src.conf as cf
from src.conf import State
import src.utilities as ut
import src.menu as mn
import src.worldgen as wrld
import src.player as plyr
import src.lang as lg
import src.score as scre
import src.sprites as spt
import src.key as ky


def main_loop(players, mouse=None):
    """
    Applique les mises à jour nécessaires au jeu.

    Parameters
    ----------
    players : Player list
        Liste des joueurs
    mouse : int * int, optionnel
        Impose une position du curseur de la souris.

    Returns
    -------
    Player list
        Liste des joueurs actualisée
    """
    if mouse is None:  # pragma: no cover
        mouse = mn.scaled_mouse_pos(ut.mouse_pos())

    if cf.STATE == State.menu:  # On est dans le menu
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "title.png")), (357, 132))
        for P in rd.sample(players, len(players)):
            P.move()
        mn.oneplayer_button.print(mouse)
        mn.multiplayer_button.print(mouse)
        mn.settings_button.print(mouse)
        mn.records_button.print(mouse)
        mn.credits_button.print(mouse)
        mn.sound_button.print(mouse)

    elif cf.STATE == State.setup:  # Paramètres
        mn.language_button.print(mouse)
        mn.return_button.print(mouse)
        mn.commands_button.print(mouse)

    elif cf.STATE == State.languages:  # Choix de la langue (1e fois)
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "title.png")), (357, 132))

        for lang in mn.flagbutton:
            lang.print(mouse)

    elif cf.STATE == State.langchange:  # Changement de la langue
        mn.return_button.print(mouse)
        for lang in mn.flagbutton:
            lang.print(mouse)

    elif cf.STATE == State.multiplayer_set:  # Régler le multijoueur
        mn.return_button.print(mouse)
        mn.print_text(mn.MULTIMENU[cf.LANG],
                      mn.Multi_nb_pos,
                      cf.GREY,
                      ut.font(mn.FONT_PIXEL, 3 * cf.RESULT_FONT_SIZE // 4))
        mn.start_button.print(mouse)
        for i in range(cf.NB_PLAYERS_MAX - 1):
            mn.multi_button[i].print(mouse, cf.NB_PLAYERS == i + 2)
        for i in range(cf.NB_PLAYERS_MAX):
            if i < cf.NB_PLAYERS:
                mn.print_image(os.path.join(
                    cf.ASSETS, "img", "mono" + cf.COLORS[i],
                    "mono" + cf.COLORS[i] + "0.png"),
                    (cf.SCREEN_WIDTH // 8 + i * cf.SCREEN_WIDTH // 4 - 50,
                        5 * cf.SCREEN_HEIGHT // 12),
                    scale=4)
                mn.print_text(ut.keyname(plyr.JUMP_KEYS[i]),
                              (cf.SCREEN_WIDTH // 8
                               + i * cf.SCREEN_WIDTH // 4,
                               2 * cf.SCREEN_HEIGHT // 3),
                              cf.GREY,
                              ut.font(mn.FONT_PIXEL,
                                      2 * cf.RESULT_FONT_SIZE // 3))

    elif cf.STATE == State.keyset:  # Changement des commandes
        mn.return_button.print(mouse)
        for button in ky.modifybutton:
            button.print(mouse)
        for i in range(cf.NB_PLAYERS_MAX):
            mn.print_text(cf.COLORSTRAD[cf.LANG][i],
                          (370, 135 + i * 150),
                          cf.GREY,
                          ut.font(mn.FONT_PIXEL, cf.RESULT_FONT_SIZE))
            mn.print_text(ut.keyname(plyr.JUMP_KEYS[i]),
                          (700, 135 + i * 150),
                          cf.GREY,
                          ut.font(mn.FONT_PIXEL, cf.RESULT_FONT_SIZE))
        if cf.CAPT:
            mn.print_image((os.path.join(cf.UI, "messagebox.png")), (189, 249))
            mn.print_text(ky.TEXTCAPT[cf.LANG]
                          + cf.COLORSTRAD[cf.LANG][cf.CAPT_PLYR],
                          (640, 350),
                          cf.GREY,
                          ut.font(mn.FONT_PIXEL, cf.RESULT_FONT_SIZE // 2))

    elif cf.STATE == State.ingame:  # On est en jeu

        # Décompte des secondes
        cf.FRAMES += 1
        if cf.FRAMES % cf.FPS == 0:
            cf.SECONDS += 1
        scre.score(cf.SECONDS)

        nb_player_alive = 0
        # Déplacement des joueurs
        for i, P in rd.sample(list(enumerate(players)), len(players)):
            if P.alive:
                P.move()
                nb_player_alive += 1
                plyr.WINNER = i

        # Affichage de la commande en début de game
        if cf.SECONDS < 3 and cf.NB_PLAYERS == 1:
            mn.print_text(mn.INDICBUTTON[cf.LANG]
                          + ut.keyname(plyr.JUMP_KEYS[0]),
                          (cf.SCREEN_WIDTH // 2, 70),
                          cf.GREY,
                          ut.font(mn.FONT_PIXEL,
                                  3 * cf.RESULT_FONT_SIZE // 4))

        # Gestion de la mort

        if cf.NB_PLAYERS > 1 >= nb_player_alive:
            # Fin du mode multijoueur
            cf.STATE = State.gameover_multi
            cf.NEWHS = scre.maj(cf.SECONDS)
        elif nb_player_alive == 0:
            # Fin du mode solo
            cf.STATE = State.gameover
            cf.NEWHS = scre.maj(cf.SECONDS)
            cf.NEWRC = scre.get_best_score() < cf.SECONDS
            mn.player_name_area.select()

    elif cf.STATE == State.gameover:  # Menu de fin solo

        scre.score_endgame(cf.SECONDS)
        if cf.CAPT:  # Demander au joueur son nom avant de MaJ le scoreboard
            mn.print_image((os.path.join(cf.UI, "messagebox.png")), (189, 249))
            mn.print_text(scre.NAMEASK[cf.LANG],
                          (640, 300),
                          cf.GREY,
                          ut.font(mn.FONT_PIXEL, cf.RESULT_FONT_SIZE // 2))
            mn.player_name_area.print()
        else:
            if cf.NEWHS:  # Nouveau record
                if cf.NEWRC:
                    if cf.LANG == "fr":
                        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                                            "highscore.png")), (428, 350))
                    else:
                        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                                            "newrecord.png")), (428, 350))
                else:
                    cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                                        "top5mes.png")), (428, 350))
            cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                                "gameover.png")), (395, 100))
            mn.restart_button.print(mouse)
            mn.return_button.print(mouse)

    elif cf.STATE == State.gameover_multi:  # Menu de fin multi

        scre.winner_endgame()

        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "gameover.png")), (395, 100))
        mn.restart_button.print(mouse)
        mn.return_button.print(mouse)

    elif cf.STATE == State.highscore:  # Affichage des meilleurs scores

        # Récupération des meilleurs scores
        records = scre.get_scores()
        number_scores = len(records)
        font_size = cf.HIGHSCORES_FONT_SIZE
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
    # remet le monocycle à la taille normale
    for color in cf.COLORS:
        ut.resize_list(spt.img_dict['mono' + color + '_img'],
                       cf.SIZE['normal'])
    cf.SPEED = cf.INITIAL_SPEED
    cf.SECONDS = 0
    cf.FRAMES = 0
    cf.NEW_ITEM_TIME = rd.randint(cf.ITEM_PROBA_MIN,
                                  cf.ITEM_PROBA_MAX)
    cf.FLAG_ITEM = False
    # efface les items, plateformes et le background
    spt.ground = ut.group_sprite_define()
    spt.clouds = ut.group_sprite_define()
    spt.trees = ut.group_sprite_define()
    spt.items = ut.group_sprite_define()
    wrld.initgen()
    return [plyr.Player(cf.COLORS[i]) for i in range(cf.NB_PLAYERS)]


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
    if mouse is None:  # pragma: no cover
        mouse = mn.scaled_mouse_pos(ut.mouse_pos())

    if event.type == ut.INC_SPEED:
        if cf.STATE == State.ingame:  # Si on est in game
            cf.SPEED += 0.5

    if event.type == ut.KEYDOWN:
        if cf.STATE == State.ingame:
            for i, P in enumerate(players):
                if event.key == plyr.JUMP_KEYS[i]:  # Saut
                    P.jump()

        elif cf.STATE == State.keyset:
            if cf.CAPT:
                if event.key == ut.K_ESCAPE:
                    cf.CAPT = False
                else:
                    if event.key in plyr.JUMP_KEYS:
                        plyr.JUMP_KEYS[plyr.JUMP_KEYS.index(event.key)] \
                            = plyr.JUMP_KEYS[cf.CAPT_PLYR]
                        plyr.JUMP_KEYS[cf.CAPT_PLYR] = event.key
                    plyr.JUMP_KEYS[cf.CAPT_PLYR] = event.key
                    ky.set_keys(plyr.JUMP_KEYS)
                    cf.CAPT = False

        elif cf.STATE == State.gameover:
            if cf.CAPT:
                if event.key == ut.K_RETURN:
                    scre.PLAYER = mn.player_name_area.input
                    scre.set_best_score(cf.SECONDS)
                    cf.CAPT = False
                    mn.player_name_area.deselect()
                else:
                    mn.player_name_area.read(event.key)

    if event.type == ut.MOUSEBUTTONDOWN:

        if cf.STATE == State.menu and\
                mn.oneplayer_button.click(mouse):
            # Clic de la souris sur le bouton "Un joueur"
            cf.NB_PLAYERS = 1
            players = reset_world()
            cf.STATE = State.ingame
            wrld.stop_ground()  # Arrêt de la création du sol du menu

        elif cf.STATE == State.menu and\
                mn.multiplayer_button.click(mouse):
            # Clic de la souris sur le bouton "Multi-joueur"
            cf.STATE = State.multiplayer_set

        elif cf.STATE == State.menu and\
                mn.records_button.click(mouse):
            # Clic de la souris sur le bouton "Records"
            cf.STATE = State.highscore

        elif cf.STATE == State.menu and\
                mn.settings_button.click(mouse):
            cf.STATE = State.setup

        elif cf.STATE == State.menu and\
                mn.sound_button.click(mouse):  # pragma: no cover
            if cf.FLAG_MUSIC:
                cf.FLAG_MUSIC = False
                ut.pause_music()
                mn.sound_button.image = 'soundoff.png'
                mn.sound_button.image_hover = 'soundoffpushed.png'
            else:
                cf.FLAG_MUSIC = True
                ut.unpause_music()
                mn.sound_button.image = 'soundon.png'
                mn.sound_button.image_hover = 'soundonpushed.png'

        elif cf.STATE == State.languages:
            for i in range(len(mn.flagbutton)):
                if mn.flagbutton[i].click(mouse):
                    cf.STATE = State.menu
                    lg.set_lang(lg.AVAILABLE[i])

        elif cf.STATE == State.multiplayer_set:
            for i in range(cf.NB_PLAYERS_MAX - 1):
                if mn.multi_button[i].click(mouse):
                    cf.NB_PLAYERS = i + 2
            if mn.return_button.click(mouse):
                cf.STATE = State.menu
            if mn.start_button.click(mouse):
                players = reset_world()
                cf.STATE = State.ingame
                wrld.stop_ground()  # Arrêt de la création du sol du menu

        elif cf.STATE == State.langchange:
            for i in range(len(mn.flagbutton)):
                if mn.flagbutton[i].click(mouse):
                    cf.STATE = State.setup
                    lg.set_lang(lg.AVAILABLE[i])
            if mn.return_button.click(mouse):
                cf.STATE = State.setup

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

        elif cf.STATE == State.setup and\
                mn.language_button.click(mouse):
            cf.STATE = State.langchange

        elif cf.STATE == State.setup and\
                mn.commands_button.click(mouse):
            cf.STATE = State.keyset

        elif cf.STATE == State.setup and\
                mn.return_button.click(mouse):
            # Clic de la souris sur le bouton "Retour"
            cf.STATE = State.menu

        elif cf.STATE == State.keyset:
            if mn.return_button.click(mouse):
                cf.STATE = State.setup
            for i in range(len(ky.modifybutton)):
                if ky.modifybutton[i].click(mouse):
                    cf.CAPT = True
                    cf.CAPT_PLYR = i

    if event.type == ut.VIDEORESIZE:  # pragma: no cover
        ut.resize_window(event.size)

    if event.type == ut.QUIT:  # pragma: no cover
        ut.quit_game()

    return players
