"""Fichier gérant le Konami Code."""

import os
import rollnjump.conf as cf
import rollnjump.utilities as ut


def pos(t):
    """
    Donne la position de l'image en x en fonction du temps d'écran.
    """
    return (t - 100)**3 // 1000


def konamicredits():
    """
    Fonction qui permet d'afficher les credits dans le mode bonus.
    """

    sta = cf.KONAMICAN % 220
    idp = (cf.KONAMICAN // 220) % 5

    cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                        "credits",
                        "music.png")), (382, 642))

    if idp == 0:
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "credits",
                            "sa.png")), (878, 342))
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "credits",
                            "hats.png")), (pos(sta), 84))
        cf.BlueSky = (190, 0, 0)
        cf.KONAMICAN += 1

    elif idp == 1:
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "credits",
                            "hb.png")), (890, 342))
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "credits",
                            "sunglasses.png")), (pos(sta), 84))
        cf.BlueSky = (127, 255, 0)
        cf.KONAMICAN += 1

    elif idp == 2:
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "credits",
                            "mc.png")), (779, 342))
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "credits",
                            "rubiks.png")), (pos(sta), 88))
        cf.BlueSky = (250, 128, 114)
        cf.KONAMICAN += 1

    elif idp == 3:
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "credits",
                            "rl.png")), (1000, 342))
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "credits",
                            "sword.png")), (pos(sta), 80))
        cf.BlueSky = (255, 255, 0)
        cf.KONAMICAN += 1

    else:
        cf.DISPLAYSURF.blit(ut.load_image(os.path.join(cf.UI,
                            "credits",
                            "thx.png")), (778, 259))
        cf.BlueSky = (0, 170, 251)
        cf.KONAMICAN += 1


def konamibutton(event):
    """
    Permet de gérer les évènements pour le KonamiCode.

    Parameters
    ----------
    event : Event
        Evènement à traiter
    """

    if 0 <= cf.KONAMISTEP <= 1 and\
        event.key == ut.keyidentifier("up"):

        cf.KONAMISTEP += 1

    elif 2 <= cf.KONAMISTEP <= 3 and\
        event.key == ut.keyidentifier("down"):

        cf.KONAMISTEP += 1

    elif cf.KONAMISTEP in [4,6] and\
        event.key == ut.keyidentifier("left"):

        cf.KONAMISTEP += 1

    elif cf.KONAMISTEP in [5,7] and\
        event.key == ut.keyidentifier("right"):

        cf.KONAMISTEP += 1

    elif cf.KONAMISTEP == 8 and\
        event.key == ut.keyidentifier("b"):

        cf.KONAMISTEP += 1

    elif cf.KONAMISTEP == 9 and\
        event.key == ut.keyidentifier("a"):

        if cf.KONAMISTATE:
            cf.KONAMISTATE = False
            cf.KONAMISTEP = 0
            cf.MUSIC = os.path.join(cf.ASSETS, 'music', 'monozik.ogg')
            cf.BlueSky = (0, 170, 251)
            cf.ITEM_PROBA_MIN = 3
            cf.ITEM_PROBA_MAX = 7
            ut.load_music(cf.MUSIC)
            ut.play_music()
        else:
            cf.KONAMISTATE = True
            cf.KONAMISTEP = 0
            cf.MUSIC = os.path.join(cf.ASSETS, 'music', 'jojo.ogg')
            cf.BlueSky = (190, 0, 0)
            cf.ITEM_PROBA_MIN = 0
            cf.ITEM_PROBA_MAX = 0
            ut.load_music(cf.MUSIC)
            ut.play_music()

    else:
        cf.KONAMISTEP = 0
