import pygame
import pygame_menu

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    print("Game launched")
    raise ValueError
    pass

menu = pygame_menu.Menu(300, 400, 'Platformer',
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add_text_input('Pseudo : ', default='Joueur')
menu.add_selector('Difficulté : ', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quitter', pygame_menu.events.EXIT)
