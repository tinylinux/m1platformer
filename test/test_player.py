"""Fichier de test pour player."""

from hypothesis import given
from hypothesis.strategies import integers
import main as mn
import src.sprites as spt
import src.conf as cf
import src.utilities as ut
import src.player as plyr
import src.gameloop as gml


# Test des collisions

# pylint: disable=too-many-arguments
@given(integers(min_value=0, max_value=100),
       integers(min_value=0, max_value=100),
       integers(min_value=0, max_value=100),
       integers(min_value=0, max_value=100),
       integers(min_value=0, max_value=100),
       integers(min_value=0, max_value=100),
       integers(min_value=10, max_value=50),
       integers(min_value=10, max_value=50))
def test_collisions(pos_prev_x, pos_prev_y,
                    pos_next_x, pos_next_y,
                    pos_plat_x, pos_plat_y,
                    width_plat, height_plat):
    """Test pour la fonction de vérification des collisions."""
    player = plyr.Player()
    player.pos = ut.Vec((pos_prev_x, pos_prev_y))
    dummy_next = ut.create_rect([pos_next_x, pos_next_y,
                                spt.p_WIDTH, spt.p_HEIGHT])
    plat = ut.create_rect([pos_plat_x, pos_plat_y,
                          width_plat, height_plat])
    (vert, hor, new_pos) = plyr.collide(player,
                                        ut.Vec((pos_next_x, pos_next_y)),
                                        plat)
    assert (vert or hor) == dummy_next.colliderect(plat)
    if new_pos is not None:
        dummy_next.topleft = new_pos
    assert not dummy_next.colliderect(plat)
# pylint: enable=too-many-arguments


# Test du saut du joueur

def test_jump():
    """Test pour la méthode de saut de la classe Player."""
    cf.NB_PLAYERS = 1
    _, player = mn.initialization(False)
    player = player[0]
    cf.STATE = cf.State.ingame
    # Lancement du saut
    player.jump()
    assert player.vel.y == -cf.V_JMP
    # Quelques tours de boucle
    for _ in range(10):
        gml.main_loop([player], False)
    # Vitesse finale, avec précision prise en compte
    assert player.vel.y <= -cf.V_JMP + 10 * cf.G + 0.001\
        and player.vel.y >= -cf.V_JMP + 10 * cf.G - 0.001
    # Vérification de la possibilité d'un double saut
    player.jump()
    assert player.vel.y == -cf.V_JMP
    gml.reset_world(False)


# Test du mouvement du joueur

@given(integers(min_value=0, max_value=100),
       integers(min_value=0, max_value=100))
def test_move(velx, vely):
    """Test pour la méthode move de la classe Player."""
    spt.ground = ut.group_sprite_define()
    player = plyr.Player()
    xinit, yinit = player.pos.x, player.pos.y
    player.vel = ut.Vec(velx, vely)
    player.move()
    vely += player.acc.y
    assert player.pos.x <= xinit + velx + 0.5 * player.acc.x + 0.001\
        and player.pos.x >= xinit + velx + 0.5 * player.acc.x - 0.001
    assert player.pos.y <= yinit + vely + 0.5 * player.acc.y + 0.001\
        and player.pos.y >= yinit + vely + 0.5 * player.acc.y - 0.001
    gml.reset_world(False)
