from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from Gestion import Gestion

def charger_excel():
    
    file_path = filedialog.askopenfilename(
            title="Sélectionnez un fichier Excel",
            filetypes=[("Fichiers Excel", "*.xlsx *.xls")])
    if file_path:
        # sauvgarder les donner existe dans le ficier excel dans une liste des dictionnires
        df = pd.read_excel(file_path)
        data_dict = df.to_dict(orient='records')
    #----------------------------------------------------
        for etudiant in data_dict:
            for cle in list(etudiant.keys()):
                if cle.lower() in ['moyenne', 'validation']:
                    etudiant.pop(cle)
        L = []
        test = 0
        if not data_dict :
            messagebox.showwarning("Attention", "Aucun Etudiant dans ce fichier.")
        else :
            for cle in data_dict[0].keys() :
                if cle == "NOM":
                    test = 1
            if test == 0:
                messagebox.showwarning("Attention", "La colone qui concerne le NOM n'existe pas ou soit mal nommée. \n  \n Veuillez vérifier si elle existe et la nommer comme suit : 'NOM'")
            elif test == 1 :  
                for etudiant in data_dict:
                    premier_cle = next(iter(etudiant))
                    for note in etudiant.values():
                        if note not in [etudiant[premier_cle],etudiant['NOM']]:
                            L.append(note)

                if all(isinstance(note,(int, float)) and 0<= note <= 20 for note in L):
                    Gestion(file_path,data_dict)                               
                else:
                    messagebox.showwarning("Attention", "Vous avez entrer une ou des notes inacceptable !")
    elif not file_path:
        messagebox.showwarning("Attention", "Aucun fichier sélectionné.")
        return

    
def standar():
    data_dict=[]
    etudiant={}
    file_path = "Système Académique de Suivi et Gestion des Notes, des Etudiant et des Module"
    root = Tk()
    root.title("Application de gestion de notes")
    root.configure(bg="#F4F6F9")
    root.resizable(False,False)
    root.iconbitmap("maroc.ico")

    header = Label(root,
               text="Vous devez soumettre au moins un Etudiant et un Module",
               bg="#1652A1",
               fg="#F4F6F9",
               font=("Arial", 18, "bold"),
               pady=15)
    header.pack(fill="x")

    Label(root,text="                      ").pack()

    # ======= Frame ========
    frame = LabelFrame(root,bg="#F4F6F9")
    frame.pack(fill="x")

    Label(frame,text=" ID de l'Etudiant : ",
          font=("Arial", 14),
          bg="#F4F6F9").grid(row=1,column=0)
    
    Label(frame,text=" NOM de l'Etudiant : ",
          font=("Arial", 14),
          bg="#F4F6F9").grid(row=2,column=0)
    
    text_module=Label(frame,text=" NOM de Module : ",
          font=("Arial", 14),
          bg="#F4F6F9")
    text_module.grid(row=3,column=0)
    
    Label(frame,text=" La Note :",
          font=("Arial", 14),
          bg="#F4F6F9").grid(row=3,column=2)

    entrer_id=ttk.Entry(frame)
    entrer_nom_E=ttk.Entry(frame)
    entrer_nom_M=ttk.Entry(frame)
    entrer_note=ttk.Entry(frame)

    entrer_id.grid(row=1,column=1)
    entrer_nom_E.grid(row=2,column=1)
    entrer_nom_M.grid(row=3,column=1)
    entrer_note.grid(row=3,column=4)

    dict_module = {}

    def fonction_new_module():
        save_id=entrer_id.get()
        save_nom_E=entrer_nom_E.get()
        save_nom_M = entrer_nom_M.get()
        save_note = entrer_note.get()

        try :
            note = float(save_note)
            if 0 <= note <= 20 :
                dict_module.update({save_nom_M: save_note})
                etudiant.update([("ID",save_id),("NOM",save_nom_E)])
                etudiant.update(dict_module)
                entrer_id.config(state="disabled")
                entrer_nom_E.config(state="disabled")
                lab_comment["text"] = f"Le module {save_nom_M} a été ajouté avec succès, avec note de {save_note}"
                return 1
            else:
                lab_comment["text"] = f"Echec de la modification \n la Note {save_note} n'est pas compris entre 0 et 20 "
        except :
            lab_comment["text"] = f"Echec de la modification \n la Note inacceptable"

    btn_new_module = ttk.Button(frame,text="Ajouter un autre Module",command=fonction_new_module)
    btn_new_module.grid(row=4,column=0)
    #====== FIN frame =======

    def save_data():     
        x = fonction_new_module()
        if x == 1:
            data_dict.append(etudiant)        
            root.destroy()
            Gestion(file_path,data_dict)
        

    Label(root,text="                      ").pack()
    ttk.Button(root,text="ENREGISTRER",command=save_data).pack()
    Label(root,text="                      ").pack()
    lab_comment =Label(root,text=" ",font=("Arial", 12),bg="#F4F6F9")
    lab_comment.pack()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    root.mainloop()          #|
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
