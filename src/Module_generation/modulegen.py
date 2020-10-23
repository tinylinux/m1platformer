import tkinter as tk

NB_LIGNES = 30
NB_COLONNES = 20
TAILLE_CARREAUX = 10

class ModuleGenerator(tk.Tk):
    def __init__(self):
        """Constructeur de l'application"""

        # Création de la fenêtre de sélection du nombre de colonnes du futur canvas de travail
        self.fenetre_nb_col = tk.Tk()
        self.nb_lignes = NB_LIGNES
        self.nb_colonnes = NB_COLONNES

        self.instructions = tk.Label(self.fenetre_nb_col, text = "Choisissez le nombre de colonnes")
        self.instructions.pack(side = tk.TOP, padx = 5, pady = 5)
            # Création du sélecteur du nombre de colonnes
        self.select_nb_col = tk.Frame(self.fenetre_nb_col)

                #Création de l'affichage
        self.affiche_nb_colonnes = tk.StringVar(self.select_nb_col, str(self.nb_colonnes))
        self.nb_col_label = tk.Label(self.select_nb_col, textvariable=self.affiche_nb_colonnes)

                # Création des bouttons d'incrémentation et de décrémentation
        self.add_col_button = tk.Button(self.select_nb_col, text = "^", command = self.add_col)
        self.rmv_col_button = tk.Button(self.select_nb_col, text = "v", command = self.rmv_col)
        
                # Affichage du sélecteur
        self.nb_col_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_col_button.pack(side = tk.TOP, padx = 5, pady = 5)
        self.rmv_col_button.pack(side = tk.TOP, padx = 5, pady = 5)
        self.select_nb_col.pack(side = tk.LEFT, pady = 5)

            # Création du boutton de validation
        self.valider_button = tk.Button(self.fenetre_nb_col, text = "Valider", command = self.valid_nb_col)
        self.valider_button.pack(side = tk.RIGHT)



    def add_col(self):
        if self.nb_colonnes < 30 :
            self.nb_colonnes += 1
            self.affiche_nb_colonnes.set(str(self.nb_colonnes))

    def rmv_col(self):
        if self.nb_colonnes > 2 :
            self.nb_colonnes -= 1
            self.affiche_nb_colonnes.set(str(self.nb_colonnes))

    def lunch(self):
        self.fenetre_nb_col.mainloop()

    def valid_nb_col(self):

        self.fenetre_nb_col.destroy()

        # Crétion de la fenêtre principale de travail
        self.fenetre_principale = tk.Tk()

            # Crétion du sélecteur d'obstacle
        self.obstacles_fonctions = {"Plateforme" : self.plateforme_creation, "Bâtiment" : self.batiment_creation}
        self.select_obstacle = tk.Frame(self.fenetre_principale)
        self.select_obstacle.pack(side = tk.RIGHT, padx = 5, pady = 5)
        self.obstacle_current = tk.StringVar(self.fenetre_principale, "Plateforme")

        for obstacle in self.obstacles_fonctions.keys():
            button = tk.Radiobutton(self.select_obstacle, text = obstacle,
                                    variable = self.obstacle_current, value = obstacle)
            button.pack(side = tk.TOP, padx = 5, pady = 5)
        
            # Création du canvas
        self.taille_carreaux = TAILLE_CARREAUX
        self.canvas = tk.Canvas(self.fenetre_principale, bg = "white",
                                height = self.taille_carreaux * self.nb_lignes,
                                width = self.taille_carreaux * self.nb_colonnes)
        self.canvas.pack(side = tk.LEFT)

        self.carreaux = [[self.canvas.create_rectangle(i * self.taille_carreaux, j * self.taille_carreaux,
                                                  (i + 1) * self.taille_carreaux, (j + 1) * self.taille_carreaux)
                     for i in range(self.nb_colonnes)] for j in range(self.nb_lignes)]

        self.occupation_carreaux = [[False for i in range(self.nb_colonnes)] for j in range(self.nb_lignes)]

        self.clic_coords = [0,0,0,0]
        self.clic1 = True

        self.canvas.bind('<ButtonRelease>', self.clic)

        self.fenetre_principale.mainloop()

    def clic(self, mouse):
        i = mouse.y // self.taille_carreaux
        j = mouse.x // self.taille_carreaux

        if self.clic1:
            self.clic_coords[0] = i
            self.clic_coords[1] = j
            self.clic1 = False
        else:
            self.clic_coords[2] = i
            self.clic_coords[3] = j
            self.obstacles_fonctions[self.obstacle_current.get()]()
            self.clic1 = True

    def plateforme_creation(self):
        i0,j0 = self.clic_coords[0], self.clic_coords[1]
        i1,j1 = self.clic_coords[2], self.clic_coords[3]
        print("une plateforme de ("+str(i0)+","+str(j0)+") à ("+str(i1)+","+str(j1)+")")

    def batiment_creation(self):
        i0,j0 = self.clic_coords[0], self.clic_coords[1]
        i1,j1 = self.clic_coords[2], self.clic_coords[3]
        print("un bâtiment de "+str(j0)+" à "+str(j1)+" à la hauteur "+str(i0))



       

if __name__ == "__main__":
    app = ModuleGenerator()
    app.lunch()