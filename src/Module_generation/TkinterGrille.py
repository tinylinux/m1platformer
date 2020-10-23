##modules

from tkinter import * 
from tkinter.messagebox import *

##global variables

#permet de définir la dimension d'une salle
def faire_quadrillage():
    globals()["Lnp"]=[20,20]
    globals()["Leffacer"]=[0,0]
    globals()["Lmur"]=[0,0]
    globals()["Lgroupe"]=[0,0]
    globals()["Lobstacles"]=[]
    globals()["tabrecap"]=[]        #Le + important ! C'est le tableau où l'on stocke les données saisies à l'écran
    
    globals()["fenetre"] = Tk()
    
    globals()["value"]= StringVar(fenetre,"3")
    
    globals()["valentree"]=StringVar(fenetre,"20")

    globals()["entree"]= Entry(fenetre, textvariable=valentree, width=30)
    entree.pack(side=LEFT, padx=5, pady=5)
    
    globals()["lignes"]=Radiobutton(fenetre, text="nombre de lignes", variable=value,value=1)
    lignes.pack(side=TOP, padx=5, pady=5)
    
    globals()["colonnes"]=Radiobutton(fenetre, text="nombre de colonnes", variable=value,value=2)
    colonnes.pack(side=TOP, padx=5, pady=5)
    
    globals()["carre"]=Radiobutton(fenetre, text="carré", variable=value,value=3)
    carre.pack(side=TOP, padx=5, pady=5)
    
    #utilise recupere
    globals()["bouton1"]= Button(fenetre, text="Valider", command=recupere)
    bouton1.pack(side=TOP, padx=5, pady=5)
    
    #utilise quitter
    globals()["boutondes"]= Button(fenetre, text="suivant", command=quitter)
    boutondes.pack(side=BOTTOM, padx=5, pady=5)
    
    fenetre.mainloop()
    return

##fonctions utilisées par faire quadrillage:

#on récupère les infos de n et p
def recupere():
    if int(value.get())==1:    #nbre de lignes
        Lnp[0]=int(entree.get())
    elif int(value.get())==2:  #nbre de colonnes
        Lnp[1]=int(entree.get())
    elif int(value.get())==3:  #carré
        Lnp[0]=Lnp[1]=int(entree.get())

#permet de quitter la fenêtre principale et d'en afficher une autre
def quitter():
    fenetre.destroy()
    for i in range (Lnp[1]):
        Lranger=[]
        for e in range(Lnp[0]):
            Lranger.append([])
        tabrecap.append(Lranger)
    seconde_fenetre()

##deuxième fenetre:

#définir les portes, obstacles et personnes dans la salle
def seconde_fenetre():
    
    globals() ["pix"] = 16    #Taille d'une case en pixels (nombre pair)
    globals() ["rap"] = 0.9    #rapport taille obstacle / taille case
    
    globals()["fenetre2"]= Tk()
    
    #utilise callback, creermur
    globals()["canvas"] = Canvas(fenetre2, width=Lnp[0]*pix+20, height=Lnp[1]*pix+20)
    canvas.bind("<ButtonRelease>", creermur)    #<ButtonRelease> c'est relâcher le clic de souris
    canvas.bind("<Button-1>", callback)         #<Button-1> c'est le clic de souris
    canvas.pack(side=LEFT)
    
    for colonnes in range(Lnp[0]+1):
        canvas.create_line(colonnes*pix+pix,pix,colonnes*pix+pix,Lnp[1]*pix+pix)
    for lignes in range(Lnp[1]+1):
        canvas.create_line(pix,lignes*pix+pix,Lnp[0]*pix+pix,lignes*pix+pix)

    globals()["value2"]=StringVar(fenetre2,"4")
    
    globals()["mur"]=Radiobutton(fenetre2,text="gros obstacle",variable=value2,value=2)
    mur.pack(side=TOP)
    
    globals()["effacer"]=Radiobutton(fenetre2,text="effacer",variable=value2,value=4)
    effacer.pack(side=TOP)
    
    globals()["fini"]=Button(fenetre2,text="terminer",command=fin)
    fini.pack(side=TOP)
    
    #utilise recommence
    globals()["recommencer"]=Button(fenetre2,text="recommencer au départ",command=recommence)
    recommencer.pack(side=BOTTOM)

    fenetre2.mainloop()
    
    return

##fonctions utilisées par seconde fenetre:

def recommence():
    #choisir d'autres dimensions de salle
    fenetre2.destroy()
    faire_quadrillage()
    
def fin():
    #fenetre2.destroy()
    print(tabrecap)


def callback(event):
    """ permet de récupérer les données du clic de souris
        et d'afficher en fonction les personnes, porte et obstacles.
        besoin de clic de souris """
    
    x=int(event.x)  #x et y sont les coordonnées de la souris
    y=int(event.y)
    x-=(x%pix)      #On se ramène à en haut à gauche de la case, 
    y-=(y%pix)      #quelque soit le pixel exact qu'on ait cliqué
    
    if int(value2.get())==4:               #effacer
        Leffacer[0],Leffacer[1]=(x//pix)-1,(y//pix)-1
    
    elif int(value2.get())==2:               #obstacle
        if x>=pix and x<=Lnp[0]*pix and y>=pix and y<=Lnp[1]*pix:
            Lmur[0],Lmur[1]=(x//pix)-1,(y//pix)-1

def creermur(event):
    x=int(event.x)
    y=int(event.y)
    x-=(x%pix)
    y-=(y%pix)
    if int(value2.get())==2:                     #obstacles
        #vérifie que c'est dans la grille et on le place
        if x>=pix and x<=Lnp[0]*pix and y>=pix and y<=Lnp[1]*pix:
            if (Lmur[0]*pix+pix)>x:
                z=x
                x=Lmur[0]*pix+pix
                Lmur[0]=(z//pix)-1
            if (Lmur[1]*pix+pix)>y:
                z=y
                y=Lmur[1]*pix+pix
                Lmur[1]=(z//pix)-1
            for i in range (Lmur[0],(x//pix)):
                for e in range(Lmur[1],(y//pix)):
                    if tabrecap[e][i]!=[] and ((e+1)*pix,(i+1)*pix) == (tabrecap[e][i][1],tabrecap[e][i][2]):
                        canvas.delete(tabrecap[e][i][0])
                    tabrecap[e][i]=[canvas.create_rectangle((i+2-rap)*pix,(e+2-rap)*pix,(i+1+rap)*pix,(e+1+rap)*pix,fill="red"),(e+1)*pix,(i+1)*pix,-1]
    if int(value2.get())==4:                         #effacer
        #vérifie que c'est dans la grille
        if x>=pix and x<=Lnp[0]*pix and y>=pix and y<=Lnp[1]*pix:
            if (Leffacer[0]*pix+pix)>x:
                z=x
                x=Leffacer[0]*pix+pix
                Leffacer[0]=(z//pix)-1
            if (Leffacer[1]*pix+pix)>y:
                z=y
                y=Leffacer[1]*pix+pix
                Leffacer[1]=(z//pix)-1
            for i in range (Leffacer[0],(x//pix)):
                for e in range(Leffacer[1],(y//pix)):
                    if tabrecap[e][i]!=[] and (e*pix+pix,i*pix+pix) == (tabrecap[e][i][1],tabrecap[e][i][2]):
                        canvas.delete(tabrecap[e][i][0])
                    tabrecap[e][i]=[]
        
##DEBUT (fenetre tkinter)
faire_quadrillage()

