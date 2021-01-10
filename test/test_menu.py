# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Fichier de test pour menu."""

import os
from hypothesis import given
from hypothesis.strategies import integers, tuples, characters, text
import rollnjump.main as main
import rollnjump.utilities as ut
import rollnjump.conf as cf
import rollnjump.menu as mn


@given(tuples(integers(0, 100), integers(0, 100)),
       tuples(integers(0, 100), integers(0, 100)),
       tuples(integers(0, 100), integers(0, 100)),
       text(characters(min_codepoint=33, max_codepoint=687)))
def test_buttontext(position, size, mouse, label):
    """Test pour la classe ButtonText."""
    main.initialization(False)
    button = mn.ButtonText(position, size, label)
    button.print(mouse)


@given(tuples(integers(0, 100), integers(0, 100)),
       tuples(integers(0, 100), integers(0, 100)),
       tuples(integers(0, 100), integers(0, 100)))
def test_buttonimage(position, size, mouse):
    """Test pour la classe ButtonImage."""
    main.initialization(False)
    button = mn.ButtonImage(position, size,
                            os.path.join(cf.UI, "multiplayer.png"),
                            os.path.join(cf.UI, "multiplayerpushed.png"))
    button.print(mouse)
    button.print(position)
    button.changlang("fr")
    assert button.lang == "fr"
    button.changlang("en")
    assert button.lang == "en"


@given(tuples(integers(0, 100), integers(0, 100)),
       tuples(integers(0, 100), integers(0, 100)))
def test_inputzone(position, size):
    """Test pour la classe InputZone."""
    main.initialization(False)
    zone = mn.InputZone(position, size)
    zone.print()
    assert not zone.selected
    zone.select()
    assert zone.selected
    zone.deselect()
    assert not zone.selected
    zone.select()
    zone.read(ut.K_s)
    zone.read(ut.K_SPACE)
    assert zone.input == "S "
    zone.read(ut.K_BACKSPACE)
    assert zone.input == "S"
    zone.read(ut.K_BACKSPACE)
    zone.deselect()
    zone.read(ut.K_s)
    assert zone.input == ""


@given(tuples(integers(0, 100), integers(0, 100)))
def test_print_image(position):
    """Test pour la fonction print_image."""
    main.initialization(False)
    mn.print_image(os.path.join(cf.UI, "credits.png"), position)


@given(text(characters(min_codepoint=33, max_codepoint=687)),
       tuples(integers(0, 100), integers(0, 100)))
def test_print_text(printed_text, position):
    """Test pour la fonction print_text."""
    main.initialization(False)
    mn.print_text(printed_text, position)
