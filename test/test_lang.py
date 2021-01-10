# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Fichier de test pour lang."""

import os
import rollnjump.conf as cf
import rollnjump.lang as lg

lg.FILE = os.path.join(os.path.dirname(__file__), "test_lang.txt")
open(lg.FILE, 'w').close()


def test_init():
    """Test pour init_lang."""
    lg.init_lang()


def test_get_set():
    """Test pour get_lang et set_lang."""
    lg.init_lang()
    lg.get_lang()
    assert cf.LANG == ""
    assert cf.STATE == cf.State.languages
    lg.set_lang("fr")
    lg.get_lang()
    assert cf.LANG == "fr"
    lg.set_lang("en")
    lg.get_lang()
    assert cf.LANG == "en"


def test_changbuttons():
    """Test pour changbuttonslang."""
    lg.changbuttonslang("fr")
    lg.changbuttonslang("en")
