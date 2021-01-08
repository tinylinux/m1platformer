"""Fichier de test pour player."""

from hypothesis import given
from hypothesis.strategies import integers
import rollnjump.main as main
import rollnjump.sprites as spt
import rollnjump.conf as cf
import rollnjump.utilities as ut
import rollnjump.player as plyr
import rollnjump.gameloop as gml
import rollnjump.item as it


# Test du saut du joueur

def test_jump():
    """Test pour la méthode de saut de la classe Player."""
    cf.NB_PLAYERS = 1
    _, player = main.initialization(False)
    player = player[0]
    cf.STATE = cf.State.ingame
    # Lancement du saut
    player.jump()
    assert player.vel.y == -cf.V_JMP
    # Quelques tours de boucle
    for _ in range(10):
        gml.main_loop([player], False)
    # Vitesse finale, avec précision prise en compte
    assert player.vel.y <= -cf.V_JMP + 10 * cf.G + 0.001\
        and player.vel.y >= -cf.V_JMP + 10 * cf.G - 0.001
    # Vérification de la possibilité d'un double saut
    player.jump()
    assert player.vel.y == -cf.V_JMP


# Test du mouvement du joueur

@given(integers(min_value=0, max_value=100),
       integers(min_value=0, max_value=100))
def test_move(velx, vely):
    """Test pour la méthode move de la classe Player."""
    main.initialization(False)
    spt.ground = ut.group_sprite_define()
    player = plyr.Player()
    xinit, yinit = player.pos.x, player.pos.y
    player.vel = ut.Vec(velx, vely)
    player.move()
    vely += player.acc.y
    assert player.pos.x <= xinit + velx + 0.5 * player.acc.x + 0.001\
        and player.pos.x >= xinit + velx + 0.5 * player.acc.x - 0.001
    assert player.pos.y <= yinit + vely + 0.5 * player.acc.y + 0.001\
        and player.pos.y >= yinit + vely + 0.5 * player.acc.y - 0.001

    player.timer = 1
    player.state = "little"
    player.move()
    assert player.state == "normal"
    player.state = "fast"
    player.move()
    assert player.vel.x == cf.V_ITEM["fast"]
    player.pos.x = (3 * cf.SCREEN_WIDTH) // 4
    player.move()
    assert player.vel.x == 0
    player.state = "slow"
    player.move()
    assert player.vel.x == cf.V_ITEM["slow"]
    player.pos.x = -player.width // 2
    player.move()
    assert player.vel.x == 0

    player.state = "normal"
    item = it.Item()
    item.pos = player.pos
    item.update()
    ut.add_to_group(item, spt.items)
    player.vel = ut.Vec((0, 0))
    player.acc = ut.Vec((0, 0))
    player.move()
    assert player.state != "normal"


def test_change_state():
    """Test pour la méthode change_state."""
    main.initialization(False)
    player = plyr.Player()
    player.change_state('little')
    assert player.width, player.height == cf.SIZE["little"]
    player.change_state('big')
    assert player.width, player.height == cf.SIZE["big"]


def test_end_item():
    """Test pour la méthode end_item."""
    main.initialization(False)
    player = plyr.Player()
    player.vel.x = cf.V_ITEM['fast']
    player.change_state('little')
    player.end_item()
    assert player.width, player.height == cf.SIZE["normal"]
    assert player.vel.x == 0
    player.vel.x = cf.V_ITEM['slow']
    player.change_state('big')
    player.end_item()
    assert player.width, player.height == cf.SIZE["normal"]
    assert player.vel.x == 0
