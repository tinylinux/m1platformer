# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Fichier de test pour key."""

import os
import rollnjump.key as ky
import rollnjump.utilities as ut
import rollnjump.player as plyr


ky.FILE = os.path.join(os.path.dirname(__file__), "test_commands.txt")


def test_keys():
    """Test pour les fonctions du module key."""
    ky.init_com()
    keys = [ut.K_SPACE, ut.K_u, ut.K_RETURN, ut.K_s]
    ky.set_keys(keys)
    assert plyr.JUMP_KEYS == keys
    plyr.JUMP_KEYS = []
    ky.get_keys()
    assert plyr.JUMP_KEYS == keys
