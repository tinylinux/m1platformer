""" Fonctions pour la boucle principale du jeu """

import sys
from math import ceil
import pygame
import src.conf as cf
import src.menu as mn
import src.worldgen as wrld
import src.player as plyr
import src.score as scre


def main_loop(P):
    """ Applique les mises à jour nécessaires au jeu,
    et renvoie le nouvel objet joueur.
    P: joueur """
    if cf.STATE == 1:  # On est dans le menu
        cf.DISPLAYSURF.blit(pygame.image.load
                            ("assets/img/ui/title.png"), (357, 132))
        P.move()
        mn.start_button.print(pygame.mouse.get_pos())
        mn.records_button.print(pygame.mouse.get_pos())

    elif cf.STATE == 2:  # On est en jeu

        # Décompte des secondes
        cf.FRAMES += 1
        if cf.FRAMES == 60:
            cf.FRAMES = 0
            cf.SECONDS += 1
        scre.score(cf.SECONDS)

        # Déplacement du joueur
        P.move()

        # Gestion de la mort
        if P.death():
            cf.STATE = 3
            cf.NEWHS = scre.maj(cf.SECONDS)

    elif cf.STATE == 3:  # Menu de fin

        scre.score_endgame(cf.SECONDS)
        if cf.NEWHS:  # Nouveau record
            cf.DISPLAYSURF.blit(pygame.image.load
                                ("assets/img/ui/highscore.png"), (428, 350))
        cf.DISPLAYSURF.blit(pygame.image.load
                            ("assets/img/ui/gameover.png"), (395, 100))
        mn.restart_button.print(pygame.mouse.get_pos())
        mn.return_button.print(pygame.mouse.get_pos())

    elif cf.STATE == 4:  # Affichage des meilleurs scores

        # Récupération des meilleurs scores
        records = scre.get_scores()
        number_scores = len(records)
        size_height = 36 * 2 * number_scores
        if number_scores == 0:
            mn.print_text("Pas de scores", (640, 360), (240, 240, 240),
                          pygame.font.Font(mn.FONT_PIXEL, 36), True)
        else:
            for best_score in range(number_scores):
                position_score = 360 - (size_height//2) + best_score*2*36 + 18
                text_display = records[best_score][1] + " : "
                text_display += str(records[best_score][0])
                mn.print_text(text_display,
                              (640, position_score), (240, 240, 240),
                              pygame.font.Font(mn.FONT_PIXEL, 36), True)
        mn.return_button.print(pygame.mouse.get_pos())

    return P


def reset_world():
    """ Réinitialise le monde """
    cf.SPEED = cf.INITIAL_SPEED
    cf.SECONDS = 0
    cf.FRAMES = 0
    cf.sol = pygame.sprite.Group()
    cf.nuages = pygame.sprite.Group()
    cf.arbres = pygame.sprite.Group()
    wrld.initgen()
    return plyr.Player()


def event_handling(P, event):
    """ Effectue les mises à jour relatives à event,
    et renvoie le nouveau joueur.
    P: joueur
    event: événement """
    if event.type == cf.INC_SPEED:
        if cf.STATE == 2:  # Si on est in game
            cf.SPEED += 0.5

    if event.type == pygame.KEYDOWN:
        if cf.STATE == 2 and event.key == pygame.K_SPACE:  # Saut
            P.jump()

    if event.type == pygame.MOUSEBUTTONDOWN:

        if cf.STATE == 1 and mn.start_button.click(pygame.mouse.get_pos()):
            # Clic de la souris sur le bouton "Commencer"
            cf.STATE = 2
            wrld.stop_sol()  # Arrêt de la création du sol du menu

        elif cf.STATE == 1 and\
                mn.records_button.click(pygame.mouse.get_pos()):
            # Clic de la souris sur le bouton "Records"
            cf.STATE = 4

        elif cf.STATE == 3:
            if mn.return_button.click(pygame.mouse.get_pos()):
                # Clic de la souris sur le bouton "Retour"
                P = reset_world()
                cf.STATE = 1
            if mn.restart_button.click(pygame.mouse.get_pos()):
                # Clic sur recommencer, on réinitialise le monde
                P = reset_world()
                cf.STATE = 2
                wrld.stop_sol()

        elif cf.STATE == 4 and mn.return_button.click(pygame.mouse.get_pos()):
            # Clic de la souris sur le bouton "Records"
            cf.STATE = 1

    if event.type == pygame.VIDEORESIZE:
        screen_size = event.size
        ratio = min(screen_size[0]/cf.SCREEN_WIDTH,
                    screen_size[1]/cf.SCREEN_HEIGHT)
        new_screen_size = (ceil(ratio * cf.SCREEN_WIDTH),
                           ceil(ratio * cf.SCREEN_HEIGHT))
        cf.WINDOWSURF = pygame.display.set_mode(new_screen_size,
                                                flags=pygame.RESIZABLE)

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    return P