"""Fichier de test pour utilities."""

from hypothesis import given
from hypothesis.strategies import integers, tuples
import src.utilities as ut
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
