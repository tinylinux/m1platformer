""" Fichier de test """

from hypothesis import given
from hypothesis.strategies import integers
import src.sprites as spt
import src.player as pl
from src.utilities import Vec
from src.utilities import create_rect


# Test des collisions

player = pl.Player()

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
    """Test pour la fonction de vérification des collisions"""
    dummy_next = create_rect([pos_next_x, pos_next_y,
                              player.width, player.height])
    plat = create_rect([pos_plat_x, pos_plat_y,
                        width_plat, height_plat])
    (vert, hor, new_pos) = player.collide(Vec((pos_prev_x, pos_prev_y)),
                                          Vec((pos_next_x, pos_next_y)),
                                          plat)
    assert (vert or hor) == dummy_next.colliderect(plat)
    if new_pos is not None:
        dummy_next.topleft = new_pos
    assert not dummy_next.colliderect(plat)
# pylint: enable=too-many-arguments
