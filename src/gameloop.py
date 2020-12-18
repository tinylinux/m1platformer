""" Fonctions pour la boucle principale du jeu """

import src.conf as cf
import src.utilities as ut
import src.menu as mn
import src.worldgen as wrld
import src.player as plyr
import src.score as scre
import src.sprites as spt


def main_loop(players):
    """ Applique les mises à jour nécessaires au jeu,
    et renvoie le nouvel objet joueur.
    P: joueur """
    if cf.STATE == "menu":  # On est dans le menu
        cf.DISPLAYSURF.blit(ut.load_image
                            ("assets/img/ui/title.png"), (357, 132))
        for P in players:
            P.move()
        mn.start_button.print(ut.mouse_pos())
        mn.records_button.print(ut.mouse_pos())

    elif cf.STATE == "in-game":  # On est en jeu

        # Décompte des secondes
        cf.FRAMES += 1
        if cf.FRAMES == 60:
            cf.FRAMES = 0
            cf.SECONDS += 1
        scre.score(cf.SECONDS)

        # Déplacement des joueurs
        for P in players:
            P.move()

        # Gestion de la mort
        for P in players:
            if P.death():
                cf.STATE = "gameover"
                cf.NEWHS = scre.maj(cf.SECONDS)

    elif cf.STATE == "gameover":  # Menu de fin

        scre.score_endgame(cf.SECONDS)
        if cf.NEWHS:  # Nouveau record
            cf.DISPLAYSURF.blit(ut.load_image
                                ("assets/img/ui/highscore.png"), (428, 350))
        cf.DISPLAYSURF.blit(ut.load_image
                            ("assets/img/ui/gameover.png"), (395, 100))
        mn.restart_button.print(ut.mouse_pos())
        mn.return_button.print(ut.mouse_pos())

    elif cf.STATE == "highscore":  # Affichage des meilleurs scores

        # Récupération des meilleurs scores
        records = scre.get_scores()
        number_scores = len(records)
        size_height = 36 * 2 * number_scores
        if number_scores == 0:
            mn.print_text("Pas de scores", (640, 360), (240, 240, 240),
                          ut.font(mn.FONT_PIXEL, 36), True)
        else:
            for best_score in range(number_scores):
                position_score = 360 - (size_height//2) + best_score*2*36 + 18
                text_display = records[best_score][1] + " : "
                text_display += str(records[best_score][0])
                mn.print_text(text_display,
                              (640, position_score), (240, 240, 240),
                              ut.font(mn.FONT_PIXEL, 36), True)
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


def event_handling(players, event):
    """ Effectue les mises à jour relatives à event,
    et renvoie le nouveau joueur.
    P: joueur
    event: événement """
    if event.type == ut.INC_SPEED:
        if cf.STATE == "in-game":  # Si on est in game
            cf.SPEED += 0.5

    if event.type == ut.KEYDOWN:
        if cf.STATE == "in-game" and event.key == ut.K_SPACE:  # Saut
            players[0].jump()

    if event.type == ut.MOUSEBUTTONDOWN:

        if cf.STATE == "menu" and mn.start_button.click(ut.mouse_pos()):
            # Clic de la souris sur le bouton "Commencer"
            cf.STATE = "in-game"
            wrld.stop_ground()  # Arrêt de la création du sol du menu

        elif cf.STATE == "menu" and\
                mn.records_button.click(ut.mouse_pos()):
            # Clic de la souris sur le bouton "Records"
            cf.STATE = "highscore"

        elif cf.STATE == "gameover":
            if mn.return_button.click(ut.mouse_pos()):
                # Clic de la souris sur le bouton "Retour"
                players = reset_world(len(players))
                cf.STATE = "menu"
            if mn.restart_button.click(ut.mouse_pos()):
                # Clic sur recommencer, on réinitialise le monde
                players = reset_world(len(players))
                cf.STATE = "in-game"
                wrld.stop_ground()

        elif cf.STATE == "highscore" and\
                mn.return_button.click(ut.mouse_pos()):
            # Clic de la souris sur le bouton "Records"
            cf.STATE = "menu"

    if event.type == ut.VIDEORESIZE:
        ut.resize_window(event.size)

    if event.type == ut.QUIT:
        ut.quit_game()

    return players
