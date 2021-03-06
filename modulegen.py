﻿# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Module de l'application de création de modules de terrain."""

import os
import tkinter as tk
import rollnjump.conf as cf


TAILLE_CARREAUX = 10
NB_LIGNES = (cf.SCREEN_HEIGHT - 90) // TAILLE_CARREAUX
NB_COLONNES = 100
NB_COLONNES_MAX = 150
NB_COLONNES_MIN = 2

SCALE_FACTOR_Y = TAILLE_CARREAUX
SCALE_FACTOR_X = 20


def minmax(fst, snd):
    """Renvoie le min et le max des arguments."""
    return min(fst, snd), max(fst, snd)


class ModuleGenerator:
    """Application de création de modules de terrain."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        """Constructeur de l'application."""
        # Création de la fenêtre de sélection du nombre de colonnes du futur
        # canevas de travail
        self.fenetre_nb_col = tk.Tk()
        self.nb_lignes = NB_LIGNES
        self.nb_colonnes = NB_COLONNES

        self.instructions = tk.Label(self.fenetre_nb_col,
                                     text="Choisissez le nombre de colonnes")
        self.instructions.pack(side=tk.TOP, padx=5, pady=5)
        # Création du sélecteur du nombre de colonnes
        self.select_nb_col = tk.Frame(self.fenetre_nb_col)

        # Création de l'affichage
        self.affiche_nb_colonnes = tk.StringVar(self.select_nb_col,
                                                str(self.nb_colonnes))
        self.nb_col_label = tk.Label(self.select_nb_col,
                                     textvariable=self.affiche_nb_colonnes)

        # Création des bouttons d'incrémentation et de décrémentation
        self.add_col_button = tk.Button(self.select_nb_col, text="^",
                                        command=self.add_col)
        self.rmv_col_button = tk.Button(self.select_nb_col, text="v",
                                        command=self.rmv_col)

        # Affichage du sélecteur
        self.nb_col_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_col_button.pack(side=tk.TOP, padx=5, pady=5)
        self.rmv_col_button.pack(side=tk.TOP, padx=5, pady=5)
        self.select_nb_col.pack(side=tk.LEFT, pady=5)

        # Création du boutton de validation
        self.valider_button = tk.Button(self.fenetre_nb_col, text="Valider",
                                        command=self.valid_nb_col)
        self.valider_button.pack(side=tk.RIGHT)

    def add_col(self):
        """Augmente le nombre de colonnes de 1 si possible."""
        if self.nb_colonnes < NB_COLONNES_MAX:
            self.nb_colonnes += 1
            self.affiche_nb_colonnes.set(str(self.nb_colonnes))

    def rmv_col(self):
        """Diminue le nombre de colonnes de 1 si possible."""
        if self.nb_colonnes > NB_COLONNES_MIN:
            self.nb_colonnes -= 1
            self.affiche_nb_colonnes.set(str(self.nb_colonnes))

    def launch(self):
        """Lance l'application."""
        self.fenetre_nb_col.mainloop()

    def valid_nb_col(self):
        """Passe à la fenêtre de création des obstacles."""
        self.fenetre_nb_col.destroy()

        # Création de la fenêtre principale de travail
        self.fenetre_principale = tk.Tk()

        # Création du canvas
        self.taille_carreaux = TAILLE_CARREAUX
        self.canvas = tk.Canvas(self.fenetre_principale, bg="white",
                                height=self.taille_carreaux * self.nb_lignes,
                                width=self.taille_carreaux * self.nb_colonnes)
        self.canvas.pack(side=tk.LEFT)

        self.carreaux = [[self.canvas.create_rectangle(
            j * self.taille_carreaux, i * self.taille_carreaux,
            (j + 1) * self.taille_carreaux, (i + 1) * self.taille_carreaux)
            for j in range(self.nb_colonnes)] for i in range(self.nb_lignes)]

        # Tableau pour savoir si une case est déjà occupée
        self.occupation_carreaux = [[-1 for j in range(self.nb_colonnes)]
                                    for i in range(self.nb_lignes)]

        # Création du sélecteur d'obstacle
        self.obstacle_creation = {"Plateforme": self.plateforme_creation,
                                  "Batiment": self.batiment_creation}
        self.obstacle_suppression = {"Plateforme": self.plateforme_suppression,
                                     "Batiment": self.batiment_suppression}
        self.select_obstacle = tk.Frame(self.fenetre_principale)
        self.select_obstacle.pack(side=tk.TOP, padx=5, pady=5)
        self.obstacle_current = tk.StringVar(self.fenetre_principale,
                                             "Plateforme")

        for obstacle in self.obstacle_creation:
            button = tk.Radiobutton(self.select_obstacle, text=obstacle,
                                    variable=self.obstacle_current,
                                    value=obstacle)
            button.bind('<Button-1>', self.cancel_selection)
            button.pack(side=tk.TOP, padx=5, pady=5)
        button = tk.Radiobutton(self.select_obstacle, text="Effacer",
                                variable=self.obstacle_current,
                                value="Effacer")
        button.pack(side=tk.TOP, padx=5, pady=5)

        # Liste des obstacles du module
        self.obstacles = {}

        # Affichage de la liste des obstacles
        self.obstacles_button = tk.Button(self.fenetre_principale,
                                          text="Liste obstacles",
                                          command=self.liste_obstacles)
        self.obstacles_button.pack(side=tk.TOP, padx=5, pady=5)

        # Enregistrement module
        self.nom_module = tk.StringVar(self.fenetre_principale, "module")
        self.entree_nom_module = tk.Entry(self.fenetre_principale,
                                          textvariable=self.nom_module)
        self.entree_nom_module.pack(side=tk.TOP, padx=5, pady=5)
        self.enregistrement_button = tk.Button(self.fenetre_principale,
                                               text="Enregistrer",
                                               command=self.enregistrement)
        self.enregistrement_button.pack(side=tk.TOP, padx=5, pady=5)

        # Mémoire des clics de la souris
        self.clic_coords = [0, 0, 0, 0]
        self.clic1 = True

        self.canvas.bind('<Button-1>', self.clic_left_canvas)
        # self.canvas.bind('<Button-3>', self.cancel_selection)

        self.fenetre_principale.mainloop()

    def liste_obstacles(self):
        """Affiche la liste des obstacles présents."""
        print(self.obstacles)

    def cancel_selection(self, mouse):
        """Annule la sélection du premier clique."""
        self.canvas.itemconfigure(
            self.carreaux[self.clic_coords[0]][self.clic_coords[1]],
            fill="white")
        self.clic1 = True
        if self.obstacle_current.get() == "Effacer":
            i = mouse.y // self.taille_carreaux
            j = mouse.x // self.taille_carreaux
            obstacleid = self.occupation_carreaux[i][j]
            if obstacleid != -1:
                obstacle = self.obstacles[obstacleid]
                del self.obstacles[obstacleid]
                self.canvas.delete(obstacleid)
                self.obstacle_suppression[obstacle[0]](obstacle)

    def clic_left_canvas(self, mouse):
        """Action de clic gauche sur une case du canvas."""
        if self.obstacle_current.get() != "Effacer":
            # Récupération des coordonnées de la souris dans la grille
            # du canevas
            i = mouse.y // self.taille_carreaux
            j = mouse.x // self.taille_carreaux

            if self.clic1:
                if self.occupation_carreaux[i][j] == -1:
                    self.canvas.itemconfigure(self.carreaux[i][j],
                                              fill="green")
                    self.clic_coords[0] = i
                    self.clic_coords[1] = j
                    self.clic1 = False
            else:
                self.clic_coords[2] = i
                self.clic_coords[3] = j
                self.canvas.itemconfigure(
                    self.carreaux[self.clic_coords[0]][self.clic_coords[1]],
                    fill="white")
                self.obstacle_creation[self.obstacle_current.get()]()
                self.clic1 = True
        else:
            self.cancel_selection(mouse)

    def plateforme_creation(self):
        """Création d'une plateforme aux coordonnées self.clic_coords."""
        i_0, i_1 = minmax(self.clic_coords[0], self.clic_coords[2])
        j_0, j_1 = minmax(self.clic_coords[1], self.clic_coords[3])
        isfree = True
        for i in range(i_0, i_1 + 1):
            for j in range(j_0, j_1 + 1):
                if self.occupation_carreaux[i][j] != -1:
                    isfree = False
        if isfree:
            print("une plateforme est créée de (" + str(i_0) + "," + str(j_0) + ")\
                  à (" + str(i_1) + "," + str(j_1) + ")")
            rect = self.canvas.create_rectangle(
                j_0 * self.taille_carreaux, i_0 * self.taille_carreaux,
                (j_1 + 1) * self.taille_carreaux,
                (i_1 + 1) * self.taille_carreaux,
                fill="yellow")
            for i in range(i_0, i_1 + 1):
                for j in range(j_0, j_1 + 1):
                    self.occupation_carreaux[i][j] = rect
            self.obstacles[rect] = ["Plateforme", (i_0, j_0),
                                    (i_1 + 1, j_1 + 1)]
        else:
            print("Collision: Impossible de créer la plateforme")

    def batiment_creation(self):
        """Création d'un batiment aux coordonnées self.clic_coords."""
        i_0 = self.clic_coords[0]
        j_0, j_1 = minmax(self.clic_coords[1], self.clic_coords[3])
        isfree = True
        for i in range(i_0, self.nb_lignes):
            for j in range(j_0, j_1 + 1):
                if self.occupation_carreaux[i][j] != -1:
                    isfree = False
        if isfree:
            print("un batiment est créé de " + str(j_0) + " à " + str(j_1)
                  + " à la hauteur " + str(i_0))
            rect = self.canvas.create_rectangle(
                j_0 * self.taille_carreaux,
                i_0 * self.taille_carreaux,
                (j_1 + 1) * self.taille_carreaux,
                self.nb_lignes * self.taille_carreaux, fill="grey")
            for i in range(i_0, self.nb_lignes):
                for j in range(j_0, j_1 + 1):
                    self.occupation_carreaux[i][j] = rect
            self.obstacles[rect] = ["Batiment", (i_0, j_0), (i_0 + 1, j_1 + 1)]
        else:
            print("Collision: Impossible de créer le batiment")

    def plateforme_suppression(self, obstacle):
        """Suppression de la plateforme [obstacle]."""
        i_0, j_0 = obstacle[1]
        i_1, j_1 = obstacle[2]
        for i in range(i_0, i_1):
            for j in range(j_0, j_1):
                self.occupation_carreaux[i][j] = -1

    def batiment_suppression(self, obstacle):
        """Suppression du bâtiment [obstacle]."""
        i_0, j_0 = obstacle[1]
        j_1 = obstacle[2][1]
        for i in range(i_0, self.nb_lignes):
            for j in range(j_0, j_1):
                self.occupation_carreaux[i][j] = -1

    def enregistrement(self):
        """Enregistre le module du canvas vers un fichier .mdl."""
        liste0 = list(self.obstacles.values())
        liste0 = sorted(liste0, key=lambda obstacle: obstacle[1][1])
        xmin = liste0[0][1][1]
        liste0 = [[plft[0], (plft[1][0] * SCALE_FACTOR_Y,
                             (plft[1][1] - xmin) * SCALE_FACTOR_X),
                            (plft[2][0] * SCALE_FACTOR_Y,
                             (plft[2][1] - xmin) * SCALE_FACTOR_X)]
                  for plft in liste0]
        yfirst = liste0[0][1][0]
        ylast = max(enumerate(liste0),
                    key=lambda obstacle:
                    (obstacle[1][2][1], obstacle[1][1][0]))[1][1][0]
        string = "\n".join([";".join([str(a) for a in li]) for li in liste0])
        print("Enregistrement de " + os.path.join("src", "modules", str(yfirst)
              + "_" + str(ylast) + "_" + self.nom_module.get() + ".mdl"))
        file = open(os.path.join(cf.SRC, "modules",
                                 str(yfirst) + "_" + str(ylast)
                    + "_" + self.nom_module.get() + ".mdl"), "w")
        file.write(str(self.nb_lignes * SCALE_FACTOR_Y) + "\n")
        file.write(string + "\n")
        file.close()


if __name__ == "__main__":
    app = ModuleGenerator()
    app.launch()
