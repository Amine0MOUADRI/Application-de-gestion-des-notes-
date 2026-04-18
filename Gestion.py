from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from FONCTIONS import *
from releve_note import generer_releve


def Gestion(file_path,data_dict):

    fenetre = Tk()
    fenetre.title(file_path)
    fenetre.configure(bg="#F4F6F9")
    fenetre.geometry("800x500")
    #fenetre.resizable(False,False)
    fenetre.iconbitmap("maroc.ico")

    lab_edit = Label(fenetre,text="Les données ont été correctement définies.",
                     bg="#F4F6F9",
                    fg="#000000",
                    font=("segoe UI", 14),
                    justify="center")
    lab_edit.pack()

    # stats
    moyenne , data_dict_v1 , moyenne_classe = dict_moyenne(data_dict)
    module_nbr = nbr_module(data_dict)
    eleves_nbr =len(data_dict)
    top =max(moyenne, key=moyenne.get)
    minimum = min(moyenne, key=moyenne.get)
   
    #==============================================

    header = Label(fenetre,
               text="       Panneau de Gestion et Analyse des élèves        ",
               bg="#1652A1",
               fg="#F4F6F9",
               font=("Arial", 18, "bold"),
               pady=15)
    header.pack(fill='x')

    #========Fonction Afficher=======
    def fonction_afficher():
        window = Toplevel(fenetre)
        window.title("Affichage des notes d'un Etudiant")
        window.iconbitmap("maroc.ico")
        window["bg"]="#F4F6F9"

        text = Label(window,
                     text="   Veuillez entrer ID ou le NOM de l'etudiant pour la verification",
                     bg="#1652A1",
                     fg="#F4F6F9",
                     font=("Arial", 18, "bold"))
        text.pack(fill="x")
        e = ttk.Entry(window)
        e.pack()
        
        
        def rech_etudiant():
            entrer = e.get()
            test = 0
            for etudiant in data_dict:
                premier_cle = next(iter(etudiant))
                a = str(etudiant[premier_cle])
                b = etudiant["NOM"]
                if entrer.lower() in [a.lower(), b.lower()]:
                    text["text"] = f"Voilà Les Statistique de l'Etudiant {etudiant['NOM']}"
                    test = 1
                    e.config(state="disabled")
                    recherche.config(text="Quiter",command=window.destroy)
                    for module , note in etudiant.items():
                        if module not in [etudiant["NOM"],etudiant[premier_cle],etudiant["moyenne"],etudiant["Validation"]]:
                            lab_affichage= Label(window,
                                                 text=f"    {module} : {note}",
                                                 font=("calibri", 16, "bold"),
                                                 bg="#F4F6F9")
                            lab_affichage.pack()
            if test == 0 :
                text["text"]="  L'étudiant n'existe pas, vous pouvez fermer la fenetre."

        recherche=ttk.Button(window,text="Rechercher",command=rech_etudiant)
        recherche.pack()
    #===========fin==============
    #voir détail d'un élève selectionner dans le tableau
    def  fonction_voir_detail():
        selected = tree.selection()

        if not selected:
            messagebox.showerror("Erreur", "Sélectionnez un élève")
            return

        index = tree.index(selected[0])
        etudiant = data_dict[index]

        window = Toplevel(fenetre)
        window.title("Affichage des notes d'un Etudiant")
        window.iconbitmap("maroc.ico")
        window["bg"]="#F4F6F9"

        text = Label(window,
                     text=f"Voilà Les Statistique de l'Etudiant {etudiant['NOM']}",
                     bg="#1652A1",
                     fg="#F4F6F9",
                     font=("Arial", 18, "bold"))
        text.pack(fill="x")
        premier_cle = next(iter(etudiant))

        for module , note in etudiant.items():
            if module not in [etudiant["NOM"],etudiant[premier_cle],etudiant["moyenne"],etudiant["Validation"]]:
                lab_affichage= Label(window,
                                     text=f"    {module} : {note}",
                                     font=("calibri", 16, "bold"),
                                     bg="#F4F6F9")
                lab_affichage.pack()
        ttk.Button(window,text="Quiter",command=window.destroy).pack()
    #===========fin==============
    # =======frame Label========
    frame = LabelFrame(fenetre,bg="#F4F6F9")
    frame.pack(fill="x")

    lab_top_note = Label(frame,
               text=f"      Note Maximale {moyenne[top]:.2f}     \nNOM : {top}",
               bg="#F4F6F9",
               fg="green",
               font=("calibri", 12, "bold"),
               pady=15)
    lab_top_note.grid(row=0,column=0)

    lab_min_note = Label(frame,
               text=f"      Note Minimale {moyenne[minimum]:.2f}     \nNOM : {minimum}",
               bg="#F4F6F9",
               fg="red",
               font=("calibri", 12, "bold"),
               pady=15)
    lab_min_note.grid(row=0,column=2)

    lab_moyenne_classe = Label(frame,
               text=f"      La moyenne du Classe est     \n     ( {moyenne_classe} / 20 )",
               bg="#F4F6F9",
               fg="#8A6E0B",
               font=("calibri", 12, "bold"),
               pady=15)
    lab_moyenne_classe.grid(row=0,column=1)

    Label(frame,text="                      ",bg="#F4F6F9").grid(row=0,column=3)

    btn_afficher = ttk.Button(frame,
                              text="Voir Détails",
                              command=fonction_voir_detail)
    btn_afficher.grid(row=0,column=4)
    # ===========================================

    #=========New fichier Excel=========
    def save_new_fichier():
        # Convertir en DataFrame
        df = pd.DataFrame(data_dict_v1)

        # Ouvrir la fenêtre "Enregistrer sous"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Fichier Excel", "*.xlsx")],
            title="Enregistrer le fichier Excel"
        )

        # Si l'utilisateur choisit un emplacement
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Succès", "Fichier Excel enregistré avec succès !")

    #============= fin ===============

    #  le Tableau
    columns = (" ID ","NOM", "Moyenne","Validation")

    tree = ttk.Treeview(fenetre, columns=columns, show="headings")

    tree.heading(" ID ", text=" ID ")
    tree.heading("NOM", text="Nom")
    tree.heading("Moyenne", text="Moyenne")
    tree.heading("Validation",text="Validation")
    tree.pack(fill="both", expand=True,anchor='ne')

    for etudiant in data_dict_v1:
        premier_cle = next(iter(etudiant))
        tree.insert("", "end" , values=(etudiant[premier_cle],etudiant["NOM"], etudiant["moyenne"], etudiant["Validation"]))
    

    #==================================================================================================
    Label(fenetre,text="                         ").pack()

    # Fonction
    def update_stats():
        moyenne , data_dict_v1, moyenne_classe= dict_moyenne(data_dict)
        
        top =max(moyenne, key=moyenne.get)
        minimum = min(moyenne, key=moyenne.get)
        lab_top_note["text"]=f"      Note Maximale {moyenne[top]:.2f}     \nNOM : {top}"
        lab_moyenne_classe['text']=f"      La moyenne du Classe est     \n     ( {moyenne_classe} / 20 )"
        lab_min_note["text"]=f"      Note Minimale {moyenne[minimum]:.2f}     \nNOM : {minimum}"

        module_nbr = nbr_module(data_dict)
        eleves_nbr =len(data_dict)
        lab_eleve_et_module['text']=f" Nombre des élèves : {eleves_nbr}     et      Nombre des Modules : {module_nbr}"

        btn_save_excel.config(command=save_new_fichier)

        #update_table
        for row in tree.get_children():
            tree.delete(row)
        for etudiant in data_dict_v1:
            premier_cle = next(iter(etudiant))
            tree.insert("", "end", values=(etudiant[premier_cle], etudiant.get('NOM'), etudiant['moyenne'], etudiant['Validation']))
        #palcer le clé moyenne dans dans la dernière colonne
        for etudiant in data_dict_v1:
            if "moyenne" in etudiant:
                valeur_moyenne = etudiant.pop("moyenne")
                etudiant['moyenne'] = valeur_moyenne
        
        for etudiant in data_dict_v1:
            if "Validation" in etudiant:
                cas_V = etudiant.pop("Validation")
                etudiant["Validation"] = cas_V
    
    #---------------------------------------------------

    # ===== partie des Menu et des Button de Gestion =======
    # Les commandes
#/////////////////////// Ajout Etudiant \\\\\\\\\\\\\\\\\\\\\\\\\\
    def ajout_Etudiant():
        window = Toplevel(fenetre)
        window.title("Ajout d'un Etudiant à la liste")
        window.iconbitmap("maroc.ico")
        window.resizable(False,False)
        window["bg"]="#F4F6F9"

        text = Label(window,
                     text="   Veuillez entrer ID ou le NOM de l'etudiant pour la verification.",
                     bg="#2E8B57",
                     fg="#F4F6F9",
                     font=("Arial", 18, "bold"))
        text.grid(row=0,column=0,columnspan=2)
        e = ttk.Entry(window)
        e.grid(row=1,column=0)
        
        
        def rech_etudiant():
            entrer = e.get()
            test = 0

            # Vérification champ vide
            if not entrer.strip():
                text['text'] = "Veuillez entrer un nom de module valide."
                return
            
            for etudiant in data_dict:
                premier_cle = next(iter(etudiant))
                a = etudiant.get('NOM')
                b = str(etudiant[premier_cle])
                if entrer.lower().strip() in [a.lower(), b.lower()]:
                    text["text"]=f"  L'étudiant {etudiant["NOM"]} est inscrit, vous pouvez fermer la fenetre."
                    test = 1
                    break
                    
            if test == 0 :
                text["text"]="Aprés vérification, vous pourrez effectuer les étapes restantes."
                Label(window,text="---------------------------------------------------------------",bg="#F4F6F9").grid(row=3,column=0)

                entries = {}
                row = 4
                e.config(state="disabled")
                bt_recherche.config(text="Quiter",command=window.destroy)
                for key in data_dict[0].keys():
                    if key != 'moyenne' and key != 'Validation':
                        lab_id = Label(window,
                                text=f" {key} :",
                                bg="#F4F6F9",
                                font=("Arial", 12, "bold"))
                        e_id = ttk.Entry(window)
                        lab_id.grid(row=row,column=0)
                        e_id.grid(row=row,column=1)
                        row +=1
                        entries[key]=e_id

                def save_data():
                    new_student = {}
                    index = 0
                    try:
                        for key, entry in entries.items():
                            index += 1
                            new_student[key] = entry.get()
                            if index > 2 :
                                dd = entry.get().strip()
                                note = float(dd)
                                if note >= 0 and note <= 20 :
                                    new_student[key] = note
                                else : 
                                    messagebox.showerror("Erreur", f"La note {note} n'est pas compris entre 0 et 20.")
                                    return
                        data_dict.append(new_student)
                        window.destroy()
                        lab_edit['text']="L'élève a été ajouté avec succès."
                        update_stats()
                        
                    except ValueError :
                        messagebox.showerror("Erreur", "Une Erreur saisie")
                        return

                btn_save = ttk.Button(window,
                                      text="Enregistrer",
                                      command=save_data)
                btn_save.grid(row=row)


        bt_recherche = ttk.Button(window,
                              text="recherche",
                              command=rech_etudiant,)
        bt_recherche.grid(row=2,column=0)

#/////////////////////// Ajout Module \\\\\\\\\\\\\\\\\\\\\\\\\\
        
    def ajout_Module():
        window = Toplevel(fenetre)
        window.iconbitmap("maroc.ico")
        window.title("Ajout d'un Module à la liste")
        window.geometry("600x400")
        window.resizable(False, False)

        #source = https://youtu.be/0WafQCaok6g?si=sP20Sht4cv8Pv89j
        # ===== Scrollable Frame =====
        canvas = Canvas(window)
        scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
        frame = Frame(canvas, bg="#F4F6F9")

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ===== UI =====
        text = Label(frame,
                    text="Veuillez entrer le NOM du Module pour la vérification.",
                    bg="#2E8B57",
                    fg="#F4F6F9",
                    font=("Arial", 16, "bold"),
                    pady=10)
        text.grid(row=0, column=0, columnspan=2, sticky="ew")

        e = ttk.Entry(frame, width=30)
        e.grid(row=1, column=0, padx=10, pady=10)

        List_note = []


        def rech_module():

            entrer = e.get().strip()

            # Vérification champ vide
            if not entrer:
                text['text'] = "Veuillez entrer un nom de module valide."
                return

            # Vérification existence
            if entrer.lower() in (cle.lower() for cle in data_dict[0].keys()):
                text['text'] = "Le Module existe déjà."
                return

            text["text"] = "Entrez les notes pour chaque étudiant :"

            row = 3

            for etudiant in data_dict:
                nom = etudiant.get('NOM')

                lab_nom = Label(frame,
                                text=f"Note de {nom} :",
                                bg="#F4F6F9",
                                font=("Arial", 12))
                lab_nom.grid(row=row, column=0, padx=10, pady=5, sticky="w")

                e_note = ttk.Entry(frame)
                e_note.grid(row=row, column=1, padx=10, pady=5)

                List_note.append(e_note)
                row += 1

            def save_data():
                for i, etudiant in enumerate(data_dict):
                    try:
                        note = float(List_note[i].get())
                        if 0 <= note <= 20 :
                            etudiant[entrer] = note
                        else :
                            text['text'] = f"{note} n'est pas compris entre 0 et 20"
                            return
                    except :
                        text['text'] = "Veuillez entrer uniquement des nombres."
                        return

                    

                window.destroy()
                lab_edit['text'] = "Module ajouté avec succès."
                update_stats()

            btn_save = ttk.Button(frame, text="Enregistrer", command=save_data)
            btn_save.grid(row=row, column=0, columnspan=2, pady=15)

        bt_recherche = ttk.Button(frame, text="Rechercher", command=rech_module)
        bt_recherche.grid(row=2, column=0, pady=5)

#/////////////////////// suprime Etudiant \\\\\\\\\\\\\\\\\\\\\\\\\\ suppression
    
    def suprime_Etudiant():
        window = Toplevel(fenetre)
        window.title("suppressuion d'un Etudiant à la liste")
        window.iconbitmap("maroc.ico")
        window["bg"]="#F4F6F9"
        window.resizable(False,False)
    

        text = Label(window,
                     text="   Veuillez entrer ID ou NOM de l'etudiant pour la verification.",
                     bg="#751818",
                     fg="#F4F6F9",
                     font=("Arial", 18, "bold"))
        text.grid(row=0,column=0,columnspan=2)
        e = ttk.Entry(window)
        e.grid(row=1,column=0)

        def rech_etudiant():
            entrer = e.get()
            test = 0
            for i in range(len(data_dict)):
                    premier_cle = next(iter(data_dict[i]))
                    etudiant = data_dict[i]
                    a = str(etudiant[premier_cle])
                    b = etudiant["NOM"]
                    if  entrer.lower() in [a.lower(), b.lower()]:
                        text["text"]="Le processus de vérification a été couronné de succès."
                        test = 1
                        index = i
                        lab_sure = Label(window,text=F"Etes-vous sur d'avoir supprimé {etudiant["NOM"]} ?",bg="#F4F6F9")
                        lab_sure.grid(row=3,columnspan=2)
                        def oui():
                            data_dict.pop(index)
                            window.destroy()
                            lab_edit['text']=" L'élève a été suprimé avec succès."
                            update_stats()

                        def non():
                            window.destroy()
                        btn_oui =ttk.Button(window,text="OUI",command=oui)
                        btn_non =ttk.Button(window,text="NON",command=non)
                        btn_oui.grid(row=4,column=0)
                        btn_non.grid(row=4,column=1)
       
            if test == 0 :
                text["text"]="  L'étudiant n'est pas inscrit, vous pouvez fermer la fenetre."
                messagebox.showerror("Erreur", "Étudiant non trouvé")
                window.destroy()


        bt_recherche = ttk.Button(window,
                              text="recherche",
                              command=rech_etudiant,)
        bt_recherche.grid(row=2,column=0)

#/////////////////////// suprime Module \\\\\\\\\\\\\\\\\\\\\\\\\\
    def suprime_Module():
        window = Toplevel(fenetre)
        window.title("suppressuion d'un Module à la liste")
        window.iconbitmap("maroc.ico")
        window["bg"]="#F4F6F9"
        window.resizable(False,False)
    

        text = Label(window,
                     text="   Veuillez entrer le NOM du Module pour la verification.",
                     bg="#751818",
                     fg="#F4F6F9",
                     font=("Arial", 18, "bold"))
        text.grid(row=0,column=0,columnspan=2)
        e = ttk.Entry(window)
        e.grid(row=1,column=0)

        def rech_module():
            entrer = e.get()
            a = list(data_dict[0].keys())
            b = []
            for k in a :
                if k not in [a[0],a[1],a[-1],a[-2]]:
                    b.append(k.lower())
            if entrer.lower()  not in b :
                lab_edit['text']=f'Le Module {entrer} n\'existe pas, essayer à nouveau.'
                messagebox.showerror("Erreur", "Module non trouvé")
                window.destroy()
            else :
                index = 0
                for g in range(len(b)):
                    if entrer.lower() == b[g]:
                        index = 2 + g

                text["text"]="Le processus de vérification a été couronné de succès."

                lab_sure = Label(window,text=f"Etes-vous sur d'avoir supprimé le module {entrer} ?",bg="#F4F6F9")
                lab_sure.grid(row=3,columnspan=2)

                def spr_module():
                    for i in range(len(data_dict)):
                        data_dict[i].pop(a[index])
                    window.destroy()
                    lab_edit['text']="Le Module a été suprimé avec succès."
                    update_stats()

                def non_spr_module():
                    window.destroy()
                oui = ttk.Button(window,text="OUI",command=spr_module)
                non = ttk.Button(window,text="NON",command=non_spr_module)
                oui.grid(row=4,column=0)
                non.grid(row=4,column=1)


        bt_recherche = ttk.Button(window,
                              text="recherche",
                              command=rech_module,)
        bt_recherche.grid(row=2,column=0)
    
#/////////////////////// Edit de Notes \\\\\\\\\\\\\\\\\\\\\\\\\\
    def gestion_des_notes():
        window = Toplevel(fenetre)
        window.title("Mise à jour des résultats Académiques")
        window.iconbitmap("maroc.ico")
        window["bg"]="#F4F6F9"
        window.resizable(False,False)
    

        text = Label(window,
                     text="  Gestion et modification des Notes",
                     bg="#7E1E8B",
                     fg="#F4F6F9",
                     font=("Arial", 18, "bold"))
        text.grid(row=0,column=0,columnspan=2)
        text_ID = Label(window,
                     text="\n ID ou NOM :",
                     bg="#F4F6F9",
                     fg="#200823",
                     font=("segoe UI", 11, "bold"))
        text_module = Label(window,
                     text="\n MODULE :",
                     bg="#F4F6F9",
                     fg="#200823",
                     font=("segoe UI", 11, "bold"))
        text_note = Label(window,
                     text=" nouvelle NOTE :",
                     bg="#F4F6F9",
                     fg="#200823",
                     font=("segoe UI", 11, "bold"))
        lab_comment = Label(window,
                     text="",
                     bg="#F4F6F9",
                     fg="#200823",
                     font=("segoe UI", 11, "bold"))
        e_id = ttk.Entry(window)
        e_module = ttk.Entry(window)
        e_note = ttk.Entry(window)
        text_ID.grid(row=1,column=0)
        text_module.grid(row=1,column=1)
        e_id.grid(row=2,column=0)
        e_module.grid(row=2,column=1)
        text_note.grid(row=3,column=1)
        e_note.grid(row=4,column=1)
        lab_comment.grid(row=6,column=0,columnspan=2)
        def mise_a_jour():
            id_etudiant = e_id.get()
            matiere = e_module.get()
            try :
                nouvelle_note=float(e_note.get())
                test1 =0
                test2 =0
                for etudiant in data_dict:  
                    x = etudiant['NOM']
                    y = str(etudiant[premier_cle])
                    if id_etudiant.lower() in [x.lower(), y.lower()]:
                        test1=1
                        a = list(data_dict[0].keys())
                        b = []
                        for k in a :
                            if k not in [a[0],a[1],a[-1],a[-2]]:
                                b.append(k.lower())
                        if matiere.lower() in b:
                            test2=1
                            for g in range(len(b)):
                                if matiere.lower() == b[g]:
                                    index = 2 + g
                            if nouvelle_note <= 20 and nouvelle_note >= 0:
                                etudiant[a[index]]=nouvelle_note
                                lab_comment["text"]=f"La modification a été avec succès \n ID : {id_etudiant} , Module : {matiere}"
                                lab_edit['text']=f"Edit dans ID : {id_etudiant} , Module : {matiere} "
                                update_stats()
                                
                            else :
                                lab_comment["text"]=f"Echec de la modification \n la Note {nouvelle_note} inacceptable"
                            
                if test1 ==0 :
                    lab_comment["text"]=f"Echec de la modification \n ID ou NOM : {id_etudiant} est faux"
                if test1 ==1 and test2 == 0:
                    lab_comment["text"]=f"Echec de la modification \n Module : {matiere} est faux"
            except :
                lab_comment["text"]=f"{e_note.get()} n'est pas une note !"
            

        btn_note= ttk.Button(window,text=" Mise à jour ",command=mise_a_jour)
        btn_note.grid(row=4,column=0)


#/////////////////////// Releve de notes \\\\\\\\\\\\\\\\\\\\\\\\\\
    def fonction_releve():
        window = Toplevel(fenetre)
        window.title("Téléchargement du relevé de notes des élèves")
        window.iconbitmap("maroc.ico")
        window["bg"]="#F4F6F9"
        window.resizable(False,False)
    

        header = Label(window,
                     text="Importer le relevé des notes des élèves",
                     bg="#1E8B84",
                     fg="#F4F6F9",
                     font=("Arial", 20, "bold"))
        header.pack(fill="x")


        text= Label(window,
                     text="Veuillez entrer l'ID ou le NOM de L'élèves",
                     bg="#F4F6F9",
                     fg="#200823",
                     font=("segoe UI", 13, "bold"))
        text.pack()

        entrer = ttk.Entry(window)
        entrer.pack()
        
        def chargement_relever():
            nom_ou_id = entrer.get()
            for etudiant in data_dict_v1:
                premier_cle = next(iter(etudiant))
                valeur = str(etudiant[premier_cle])
                a = etudiant["NOM"]
                if nom_ou_id.lower() in [valeur.lower(), a.lower()]:
                    window.destroy()
                    generer_releve(etudiant)
                    lab_edit["text"]=f"Téléchargement du releve de l'élève : {nom_ou_id}"
                else:
                    text["text"]="l'ID ou le NOM de L'élèves est INCORRECT"

        btn = ttk.Button(window,text="Télécharger",command=chargement_relever)
        btn.pack()
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

#Les Fonctions du Button de Gestion
    def fonction_ajout():
        window = Toplevel(fenetre)
        window.title("Ajout d'un Etudiant ou Module")
        window.iconbitmap("maroc.ico")
        window["bg"]="#F4F6F9"
        window.resizable(False,False)

        header = Label(window,
                     text="          Choisissez d'Ajout un élève ou un module        ",
                     bg="#CEBF3A",
                     fg="#F4F6F9",
                     font=("Arial", 20, "bold"))
        header.grid(row=0,columnspan=3)

        Label(window,text="                  ").grid(row=1,column=0)

        ttk.Button(window,text="élève",command=ajout_Etudiant).grid(row=2,column=0)
        Label(window,text="     OU      ",bg="#F4F6F9").grid(row=2,column=1)
        ttk.Button(window,text="Module",command=ajout_Module).grid(row=2,column=2)

        Label(window,text="                  ").grid(row=3,column=0)

    def supprimer_etudiant_selectioner():
        selected = tree.selection()

        if not selected:
            messagebox.showerror("Erreur", "Sélectionnez un élève")
            return

        index = tree.index(selected[0])
        data_dict.pop(index)

        update_stats()

    def releve_eleve_selectionner():
        selected = tree.selection()

        if not selected:
            messagebox.showerror("Erreur", "Sélectionnez un élève")
            return

        index = tree.index(selected[0])
        etudiant = data_dict[index]
        generer_releve(etudiant)
        lab_edit["text"]=f"Téléchargement du releve de l'élève : {etudiant['NOM']}"

    def gestion_des_notes_par_selection():
        selected = tree.selection()

        if not selected:
            messagebox.showerror("Erreur", "Sélectionnez un élève")
            return

        index = tree.index(selected[0])
        etudiant = data_dict[index]

        window = Toplevel(fenetre)
        window.title("Affichage des notes d'un Etudiant")
        window.iconbitmap("maroc.ico")
        window["bg"]="#F4F6F9"
        window.resizable(False,False)
    

        text = Label(window,
                     text="  Gestion et modification des Notes",
                     bg="#7E1E8B",
                     fg="#F4F6F9",
                     font=("Arial", 18, "bold"))
        text.grid(row=0,column=0,columnspan=2)
        text_ID = Label(window,
                     text="\n L'étudiant :",
                     bg="#F4F6F9",
                     fg="#200823",
                     font=("segoe UI", 11, "bold"))
        text_module = Label(window,
                     text="\n MODULE :",
                     bg="#F4F6F9",
                     fg="#200823",
                     font=("segoe UI", 11, "bold"))
        text_note = Label(window,
                     text=" nouvelle NOTE :",
                     bg="#F4F6F9",
                     fg="#200823",
                     font=("segoe UI", 11, "bold"))
        lab_comment = Label(window,
                     text="",
                     bg="#F4F6F9",
                     fg="#200823",
                     font=("segoe UI", 11, "bold"))
        nom_etudiant = Label(window,
                     text=etudiant['NOM'],
                     bg="#F4F6F9",
                     fg="#200823",
                     font=("segoe UI", 11, "bold"))
        e_module = ttk.Entry(window)
        e_note = ttk.Entry(window)
        text_ID.grid(row=1,column=0)
        text_module.grid(row=1,column=1)
        nom_etudiant.grid(row=2,column=0)
        e_module.grid(row=2,column=1)
        text_note.grid(row=3,column=1)
        e_note.grid(row=4,column=1)
        lab_comment.grid(row=6,column=0,columnspan=2)
        def mise_a_jour():
            matiere = e_module.get()
            try :
                nouvelle_note=float(e_note.get())
                test2 =0
                a = list(data_dict[0].keys())
                b = []
                for k in a :
                    if k not in [a[0],a[1],a[-1],a[-2]]:
                        b.append(k.lower())
                if matiere.lower() in b:
                    test2=1

                    for g in range(len(b)):
                        if matiere.lower() == b[g]:
                            index = 2 + g
                    if nouvelle_note <= 20 and nouvelle_note >= 0:
                        etudiant[a[index]]=nouvelle_note
                        lab_comment["text"]=f"La modification a été avec succès \n ID : {etudiant['NOM']} , Module : {matiere}"
                        lab_edit['text']=f"Edit dans ID : {etudiant['NOM']} , Module : {matiere} "
                        update_stats()
                                
                    else :
                        lab_comment["text"]=f"Echec de la modification \n la Note {nouvelle_note} inacceptable"
                            
                if test2 == 0:
                    lab_comment["text"]=f"Echec de la modification \n Module : {matiere} est faux"
            except :
                lab_comment["text"]=f"{e_note.get()} n'est pas une note !"
       
        btn_note= ttk.Button(window,text="Mise à jour",command=mise_a_jour)
        btn_note.grid(row=4,column=0)

#=========================================
    # =======frame Button========
    frame = LabelFrame(fenetre,bg="#F4F6F9")
    frame.pack(fill="x")

    Label(frame,text="                  ").grid(row=0,column=0)


    btn_save_excel =  ttk.Button(frame,text="Exporter vers Excel",command=save_new_fichier)
    btn_save_excel.grid(row=0,column=1)
    

    Label(frame,text="                                                                               ").grid(row=0,column=3)


    btn_ajout = ttk.Button(frame,text="Ajout",command=fonction_ajout)
    btn_suprime=ttk.Button(frame,text="Suprimer par selection",command=supprimer_etudiant_selectioner)
    btn_edit=ttk.Button(frame,text="Edit",command=gestion_des_notes_par_selection)
    btn_releve=ttk.Button(frame,text="Releve",command=releve_eleve_selectionner)
    btn_suprime.grid(row=0,column=4)
    btn_ajout.grid(row=0,column=6)
    btn_edit.grid(row=0,column=5)
    btn_releve.grid(row=0,column=2)

    #=============================

    lab_eleve_et_module = Label(fenetre,
               text=f" Nombre des élèves : {eleves_nbr}     et      Nombre des Modules : {module_nbr}",
               bg="#F4F6F9",
               fg="#1E3A5F",
               font=("calibri", 12, "bold"),
               pady=15)
    lab_eleve_et_module.pack(anchor='center')

    # définition et affichage des menu
    my_menu = Menu(fenetre)
    ajout = Menu(my_menu,tearoff=0)
    ajout.add_command(label="Ajouter un Etudiant",command=ajout_Etudiant)
    ajout.add_separator()
    ajout.add_command(label="ajouter un Module",command=ajout_Module)

    suppression=Menu(fenetre,tearoff=0)
    suppression.add_command(label="Suppression d'un Etudiant",command=suprime_Etudiant)
    suppression.add_separator()
    suppression.add_command(label="Suppression d'un Module",command=suprime_Module)

    edit=Menu(fenetre,tearoff=0)
    edit.add_command(label="Gestion dynamique des notes",command=gestion_des_notes)

    releve=Menu(fenetre,tearoff=0)
    releve.add_command(label="Télécharger le relevé des notes",command=fonction_releve)

    afficher=Menu(fenetre,tearoff=0)
    afficher.add_command(label="Afficher les statistique d'un Etudiant",command=fonction_afficher)

    my_menu.add_cascade(label="Suppression",menu=suppression)
    my_menu.add_cascade(label="Ajout",menu=ajout)
    my_menu.add_cascade(label="Edit",menu=edit)
    my_menu.add_cascade(label="Relevé",menu=releve)
    my_menu.add_cascade(label="Afficher",menu=afficher)
    fenetre.config(menu=my_menu)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    fenetre.mainloop()       #|
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~