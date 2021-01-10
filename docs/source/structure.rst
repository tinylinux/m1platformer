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

Stucture de l'application
=========================

Voici les différents modules python utilisés par l'application **Roll 'n' Jump** :

* ``main.py`` :
   Fichier principal de lancement et d'initialisation de l'application.
* ``background.py`` :
   Gère les objets de décors tels que les nuages et les arbres.
   Contient les classes des nuages et des arbres.
* ``conf.py`` :
   Rassemble l'ensemble des variables configurables et accessibles à tous les fichiers.
   *Ne doit pas importer ``utilities``.*
* ``gameloop.py`` :
   Contient la boucle générale du jeu.
   Gère la mise à jour du jeu et les événements provenant de l'utilisateur.
   C'est ici que les différentes phases et menus du jeu sont détéctés, via la variable ``cf.STATE``.
* ``item.py`` :
   Gère les objets ``item``. Contient la classe des items.
* ``key.py`` :
   Gère la capture de touche pour configurer les saut des joueurs.
* ``lang.py`` :
   Gère les différentes langues mise en place, ainsi que sa configuration.
* ``menu.py`` :
   Gère les différents boutons et menus du jeu. Contient les classes des bouttons avec image ou texte,
   ainsi que celle des zones de saisie. Y sont définis tous les bouttons des différents menus.
* ``platforms.py`` :
   Contient les classes des objets sur lesquels roulent les joueurs. Ces objets sont le sol
   (celui pendant entre autre le menu principal) et les plateformes (plateformes flottantes et bâtiments).
* ``player.py`` :
   Gère la classe des joueurs.
* ``score.py`` :
   Gère le score et le tableau des records.
* ``sprites.py`` :
   Définie les différents objet à l'écran. On y trouve le chargement des images attachées
   aux objets et les dimensions des plateformes du sol.
* ``utilities.py``  :
   Rassemble l'ensemble des fonctions provenant de pygame,
   et d'autres fonctions utiles et non spécifiques à un fichier.
* ``worldgen.py`` :
   Permet la génération du monde et des sections de monde appelées modules
   et stockées dans le dossier ``modules``. Permet le préchargement de ces modules
   et met à jour l'ensemble des objets mouvants.

