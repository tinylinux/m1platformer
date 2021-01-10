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

Utilisation du générateur de modules
====================================

.. ATTENTION::
    le module ``tkinter`` est nécessaire à l'utilisation du générateur de modules

La première fenêtre vous demande le nombre de colonnes de la future grille de création de votre module
Celui-ci peut être augmenté et diminué avec les boutons à côté du nombre.
Lorsque ce nombre vous convient, il suffit de valider.

La seconde fenêtre est la fenêtre principale de création de votre module.
Elle se décompose en trois zones : 

- Le sélecteur d'obstacle

- La grille de création

- Les fonctionnalités tournées vers l'extérieur

Le sélecteur d'obstacle
***********************

Il permet de sélectionner à l'aide du clique gauche le type du prochain obstacle à placer, ou de permettre d'effacer des obstacles.

La grille de création
*********************

Lorsqu'un type d'obstacle est choisi dans le sélecteur, il suffit de délimiter les dimensions et l'emplacement du prochain obstacle à ajouter à l'aide de deux cliques gauches
sur la grille. À la création de l'obstacle, ses caractéristiques sont affichées dans la console.

.. ATTENTION::
    Deux obstacles peuvent se toucher mais ne peuvent se pas superposer. Le cas échéant, un message d'erreur "Collision" est affiché dans la console.

Il est aussi possible d'effacer un obstacle en choisissant la fonctionnalité dans le sélecteur et en faisant un clique gauche sur l'obstacle en question.

Les fonctionnalités tournées vers l'extérieur
*********************************************

Deux fonctionnalités sont présentes ici. En premier le bouton "Liste obstacles" qui affiche dans la console l'ensemble des caractéristiques des obstacles présents sur la grille.
En dessous, une zone de texte qui permet de rentrer un nom particulier de module, puis le bouton "Enregistrer"
qui permet d'enregistrer la grille sous forme d'un fichier ``y1_y2_nom.mdl`` avec ``y1`` la hauteur de l'obstacle le plus à gauche,
``y2`` celle de l'obstacle le plus à droite et ``nom`` le nom du module rentré dans la zone de texte précédente.