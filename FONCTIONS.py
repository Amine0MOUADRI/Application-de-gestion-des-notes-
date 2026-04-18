from tkinter import *
from tkinter import ttk

def dict_moyenne(data_dict):
    moyenne = {}
    validtion ={}
    list_moy=[]
    for etudiant in data_dict:
        L=[]
        k=0
        premier_cle = next(iter(etudiant))
        for cle in etudiant.keys():
            if cle in ["NOM","moyenne","Validation",premier_cle]:
                k=1
            else:
                L.append(float(etudiant[cle]))            

    
        moy=sum(L)/len(L)
        list_moy.append(moy)
        moyenne.update({etudiant.get('NOM'):moy})
        if moy >= 10:
            validtion.update({"✅ Validé":etudiant.get('NOM')})
        else:
            validtion.update({"❌ Non validé":etudiant.get('NOM')})
        # ajout du moyenne
        
        for cle, valeur in moyenne.items():
            if cle == etudiant.get('NOM'): 
                note = round(valeur, 3)  
                etudiant.update({"moyenne":note})


        for cle, valeur in validtion.items():
            if valeur == etudiant.get('NOM'):
                etudiant.update({"Validation":cle})
    
    moy_classe = sum(list_moy)/len(list_moy)
    moyenne_classe = round(moy_classe, 3)

    return moyenne, data_dict , moyenne_classe

def nbr_module(data_dict):
    nbr_mdl = -2
    for i in data_dict[0].values():
        nbr_mdl +=1
    nbr_mdl-=2
    return nbr_mdl

def style_button():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Modern.TButton",
                font=("Arial", 12, "bold"),
                padding=10,
                foreground="white",
                background="#1652A1",
                borderwidth=0)

    style.map("Modern.TButton",
          background=[("active", "#101F33")])
