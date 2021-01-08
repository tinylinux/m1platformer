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
