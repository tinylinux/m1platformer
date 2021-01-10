# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Fichier de test pour platforms."""

from hypothesis import given
from hypothesis.strategies import integers, tuples
import rollnjump.main as main
import rollnjump.utilities as ut
import rollnjump.sprites as spt
import rollnjump.platforms as plt


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
