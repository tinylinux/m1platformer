..
   Roll 'n' Jump
   Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
   Matteo Chencerel, Rida Lali
   To the extent possible under law, the author(s) have dedicated all
   copyright and related and neighboring rights to this software to the
   public domain worldwide. This software is distributed without any warranty.
   You should have received a copy of the CC0 Public Domain Dedication along
   with this software. If not, see
   <http://creativecommons.org/publicdomain/zero/1.0/>.

Utilities
=========

.. automodule:: rollnjump.utilities
   :members: keyname, load_image, load_music, play_music,
            pause_music, unpause_music,
            initialize_window, resize_window,
            initialize_clock, make_event, get_events,
            group_sprite_define, add_to_group,
            resize, resize_list, contact,
            collide_group, update_screen,
            get_screen_size, create_rect, draw_rect,
            mouse_pos, quit_game, font, update_pos_vel,
            collide, onlydigits, onlyalphanum
   :show-inheritance:

Événements
**********
.. autodata:: INC_SPEED
   :annotation:
.. autodata:: KEYDOWN
   :annotation:
.. autodata:: MOUSEBUTTONDOWN
   :annotation:
.. autodata:: VIDEORESIZE
   :annotation:
.. autodata:: QUIT
   :annotation:

Touches
*******
.. autodata:: K_SPACE
   :annotation:
.. autodata:: K_RETURN
   :annotation:
.. autodata:: K_s
   :annotation:
.. autodata:: K_u
   :annotation:
.. autodata:: K_BACKSPACE
   :annotation:

Classes
*******
.. autodata:: Vec
   :annotation:
.. autodata:: Sprite
   :annotation:
.. autoclass:: GameObject
   :members:
   :show-inheritance: