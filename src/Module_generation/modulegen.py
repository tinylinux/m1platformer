import tkinter as tk

class ModuleGenerator(tk.Tk):
    def __init__(self):
        """Constructeur de l'application"""
        tk.Tk.__init__(self)
        self.carreau_size = 10
        self.nb_carreaux_x = tk.IntVar()
        self.nb_carreaux_x.set(10)
        self.nb_carreaux_y = 30
        # Création du canvas
        self.canv = tk.Canvas(self, bg = "white", height=self.carreau_size*self.nb_carreaux_y, width = self.carreau_size*self.nb_carreaux_x.get())
        self.canv.pack(side = tk.LEFT)
        carreaux = [[self.canv.create_rectangle(i*self.carreau_size, j*self.carreau_size, (i+1)*self.carreau_size, (j+1)*self.carreau_size, fill = "#FFFFFF")
                     for i in range(self.nb_carreaux_x.get())] for j in range(self.nb_carreaux_y)]

        # Changement nombre de cellule
        self.canv.bind("<Up>", self.incr)
        self.canv.bind("<Down>", self.decr)

    def incr(self,key):
        nb_carreaux_x = self.nb_carreaux_x.get()
        if nb_carreaux_x < 100:
            self.nb_carreaux_x.set(nb_carreaux_x + 1)

    def decr(self,key):
        nb_carreaux_x = self.nb_carreaux_x.get()
        if nb_carreaux_x > 3:
            self.nb_carreaux_x.set(nb_carreaux_x - 1)
       

if __name__ == "__main__":
    app = ModuleGenerator()
    app.title("Generateur de modules")
    app.mainloop()