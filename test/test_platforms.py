"""Fichier de test pour platforms."""

from hypothesis import given
from hypothesis.strategies import integers, tuples
import main
import src.utilities as ut
import src.sprites as spt
import src.platforms as plt


def test_ground():
    """Test pour la classe Ground."""
    main.initialization(False)
    spt.ground = ut.group_sprite_define()
    plat = plt.Ground(0)
    plat.update()
    assert len(spt.ground) == 1
    plat.stop_creation()
    assert not plat.FLAG_creation


@given(tuples(integers(0, 100), integers(0, 100)),
       tuples(integers(0, 100), integers(0, 100)))
def test_platform(pos, dim):
    """Test pour la classe Platform."""
    main.initialization(False)
    plt.Platform(pos, dim)
