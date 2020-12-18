""" Fonctions pour la boucle principale du jeu """

import src.conf as cf
import src.utilities as ut
import src.menu as mn
import src.worldgen as wrld
import src.player as plyr
import src.score as scre
import src.sprites as spt


def main_loop(players, graphical):
    """ Applique les mises à jour nécessaires au jeu,
    et renvoie le nouvel objet joueur.
    P: joueur """
    if cf.STATE == 1:  # On est dans le menu
        cf.DISPLAYSURF.blit(ut.load_image
                            ("assets/img/ui/title.png"), (357, 132))
        for P in players:
            P.move()
        if graphical:
            mn.start_button.print(ut.mouse_pos())
            mn.records_button.print(ut.mouse_pos())

    elif cf.STATE == 2:  # On est en jeu

        # Décompte des secondes
        cf.FRAMES += 1
        if cf.FRAMES == cf.FPS:
            cf.FRAMES = 0
            cf.SECONDS += 1
        scre.score(cf.SECONDS)

        # Déplacement des joueurs
        for P in players:
            P.move()

        # Gestion de la mort
        nb_player_alive = cf.NB_PLAYERS
        for P in players:
            if P.death():
                nb_player_alive -= 1
        if cf.NB_PLAYERS > 1 >= nb_player_alive :
            # Fin du mode multijoueur
            cf.STATE = 3
            cf.NEWHS = scre.maj(cf.SECONDS)
        elif nb_player_alive == 0:
            # Fin du mode solo
            cf.STATE = 3
            cf.NEWHS = scre.maj(cf.SECONDS)

    elif cf.STATE == 3:  # Menu de fin

        scre.score_endgame(cf.SECONDS)
        if cf.NEWHS:  # Nouveau record
            cf.DISPLAYSURF.blit(ut.load_image
                                ("assets/img/ui/highscore.png"), (428, 350))
        cf.DISPLAYSURF.blit(ut.load_image
                            ("assets/img/ui/gameover.png"), (395, 100))
        if graphical:
            mn.restart_button.print(ut.mouse_pos())
            mn.return_button.print(ut.mouse_pos())

    elif cf.STATE == 4:  # Affichage des meilleurs scores

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


def reset_world(nb_players=1):
    """ Réinitialise le monde """
    cf.SPEED = cf.INITIAL_SPEED
    cf.SECONDS = 0
    cf.FRAMES = 0
    spt.ground = ut.group_sprite_define()
    spt.clouds = ut.group_sprite_define()
    spt.trees = ut.group_sprite_define()
    wrld.initgen()
    return [plyr.Player() for _ in range(nb_players)]


def event_handling(players, event, graphical):
    """ Effectue les mises à jour relatives à event,
    et renvoie le nouveau joueur.
    P: joueur
    event: événement """
    if event.type == ut.INC_SPEED:
        if cf.STATE == 2:  # Si on est in game
            cf.SPEED += 0.5

    if graphical:
        if event.type == ut.KEYDOWN:
            if cf.STATE == 2:
                for i, P in enumerate(players):
                    if event.key == plyr.JUMP_KEYS[i]:  # Saut
                        P.jump()

        if event.type == ut.MOUSEBUTTONDOWN:

            if cf.STATE == 1 and mn.start_button.click(ut.mouse_pos()):
                # Clic de la souris sur le bouton "Commencer"
                cf.STATE = 2
                wrld.stop_ground()  # Arrêt de la création du sol du menu

            elif cf.STATE == 1 and\
                    mn.records_button.click(ut.mouse_pos()):
                # Clic de la souris sur le bouton "Records"
                cf.STATE = 4

            elif cf.STATE == 3:
                if mn.return_button.click(ut.mouse_pos()):
                    # Clic de la souris sur le bouton "Retour"
                    players = reset_world(len(players))
                    cf.STATE = 1
                if mn.restart_button.click(ut.mouse_pos()):
                    # Clic sur recommencer, on réinitialise le monde
                    players = reset_world(len(players))
                    cf.STATE = 2
                    wrld.stop_ground()

            elif cf.STATE == 4 and mn.return_button.click(ut.mouse_pos()):
                # Clic de la souris sur le bouton "Records"
                cf.STATE = 1

        if event.type == ut.VIDEORESIZE:
            ut.resize_window(event.size)

    if event.type == ut.QUIT:
        ut.quit_game()

    return players
