# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Fichier de test pour worldgen."""

from hypothesis import given
from hypothesis.strategies import integers
import rollnjump.main as main
import rollnjump.utilities as ut
import rollnjump.conf as cf
import rollnjump.sprites as spt
import rollnjump.worldgen as wrld


def test_platform_creation():
    """Test pour la fonction platform_creation."""
    bloc1 = ["Plateforme", "(280, 0)", "(320, 600)"]
    wrld.platform_creation(bloc1, 10, 10)
    bloc2 = ["Batiment", "(350, 0)", "(360, 460)"]
    wrld.platform_creation(bloc2, 10, 10)


def test_initgen():
    """Test pour la fonction initgen."""
    # Initgen est appelée dans initialization
    main.initialization(False)
    assert len(spt.clouds) == 4
    assert len(spt.trees) == 4
    assert len(spt.ground) > 0


@given(integers(0, 100), integers(0, 100))
def test_genere_module(xoffset, yoffset):
    """Test pour la fonction genere_module."""
    main.initialization(False)
    bloc = ["Plateforme", "(280, 0)", "(320, 600)"]
    plat = wrld.platform_creation(bloc, xoffset, yoffset)
    wrld.genere_module(plat)


def test_stop_ground():
    """Test pour la fonction stop_ground."""
    main.initialization(False)
    wrld.stop_ground()
    for bloc in spt.ground:
        assert not bloc.FLAG_creation


def test_update():
    """Test pour la fonction update."""
    main.initialization(False)
    wrld.stop_ground()
    for _ in range(100):
        wrld.update()
    cf.FLAG_ITEM = False
    cf.SECONDS = 10
    cf.NEW_ITEM_TIME = 10
    item_num = len(spt.items)
    wrld.update()
    assert len(spt.items) == item_num + 1
    spt.ground = ut.group_sprite_define()
    wrld.update()
