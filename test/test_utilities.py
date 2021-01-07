"""Fichier de test pour utilities."""

import os
from hypothesis import given
from hypothesis.strategies import integers, tuples, text
import main
import src.conf as cf
import src.utilities as ut
import src.platforms as plt
import src.sprites as spt
import src.player as plyr


# Test des collisions

@given(tuples(integers(min_value=0, max_value=100),
              integers(min_value=0, max_value=100)),
       tuples(integers(min_value=0, max_value=100),
              integers(min_value=0, max_value=100)),
       tuples(integers(min_value=0, max_value=100),
              integers(min_value=0, max_value=100)),
       tuples(integers(min_value=10, max_value=50),
              integers(min_value=10, max_value=50)))
def test_collisions(pos_prev, pos_next, pos_plat, size_plat):
    """Test pour la fonction de vérification des collisions."""
    player = plyr.Player()
    player.pos = ut.Vec(pos_prev)
    dummy_next = ut.create_rect([pos_next[0], pos_next[1],
                                player.width, player.height])
    plat = ut.create_rect([pos_plat[0], pos_plat[1],
                          size_plat[0], size_plat[1]])
    (vert, hor, new_pos) = ut.collide(player,
                                      ut.Vec(pos_next),
                                      plat)
    assert (vert or hor) == dummy_next.colliderect(plat)
    if new_pos is not None:
        dummy_next.topleft = new_pos
    assert not dummy_next.colliderect(plat)


def test_update():
    """Test pour la fonction update_pos_vel."""
    main.initialization(False)
    player = plyr.Player()
    # collision horizontale
    plat = plt.Platform((50, 50), (100, 40))
    ut.add_to_group(plat, spt.ground)
    player.pos = ut.Vec((40 - player.width, 50))
    player.vel = ut.Vec((20, 0))
    player.acc = ut.Vec((0, 0))
    ut.update_pos_vel(player, spt.ground)
    assert player.pos == ut.Vec((50 - player.width, 50))

    # collision verticale
    player.pos = ut.Vec((50, 40 - player.height))
    player.vel = ut.Vec((0, 20))
    player.acc = ut.Vec((0, 0))
    ut.update_pos_vel(player, spt.ground)
    assert player.pos == ut.Vec((50, 50 - player.height))


@given(text())
def test_onlydigits(string):
    """Test pour la fonction onlydigits."""
    digits = ut.onlydigits(string)
    assert digits == '' or digits.isnumeric()


@given(text())
def test_onlyalphanum(string):
    """Test pour la fonction onlyalphanum."""
    alphanum = ut.onlyalphanum(string)
    assert alphanum == '' or alphanum.isalnum()


@given(tuples(integers(0, 100), integers(0, 100)),
       integers(0, 100))
def test_gameobject(position, scroll):
    """Test pour la classe GameObject."""
    main.initialization(False)
    obj = ut.GameObject(
        position, scroll,
        ut.load_image(os.path.join(cf.ASSETS, "img", "mono", "mono0.png")))
    obj.update()
    spt.ground = ut.group_sprite_define()
    ut.add_to_group(obj, spt.ground)
    obj.pos = ut.Vec((-150, -150))
    obj.update()
    assert len(spt.ground) == 0
