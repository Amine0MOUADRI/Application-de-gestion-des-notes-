from tkinter import *
from tkinter import ttk
from data_loader import *
from FONCTIONS import style_button

root = Tk()
root.title("Système Académique de Suivi et Gestion des Notes")
root.geometry("600x400")
root.configure(bg="#F4F6F9")
root.resizable(False,False)
root.iconbitmap("maroc.ico")
header = Label(root,
               text="Initialisation des Données via un Fichier Excel",
               bg="#1652A1",
               fg="#F4F6F9",
               font=("Arial", 18, "bold"),
               pady=15)
header.pack(fill="x")

explication = Label(root,
                    text="\n\n\nVeuillez importer un fichier Excel (.xlsx)\n"
                         "contenant les colonnes suivantes :\n\n"
                         " ID   |   NOM*   | module 1 | module 2 | ....\n\n",
                    bg="#F4F6F9",
                    fg="#00113A",
                    font=("Arial", 14),
                    justify="center")

explication.pack()

#style button
style = style_button()
#----------------------
Label(root,text="                      ",bg="#F4F6F9").pack()

# =======frame Button========
frame = LabelFrame(root,bg="#F4F6F9")
frame.pack(fill="x")

Label(frame,text="                      ",bg="#F4F6F9").grid(row=0,column=0)
Label(frame,text="                                             ",bg="#F4F6F9").grid(row=0,column=2)

btn_excel = ttk.Button(frame,
                   text="Choisir le fichier",
                   
                   command=charger_excel,
                   style="Modern.TButton")
btn_excel.grid(row=0,column=1)

btn_standar = ttk.Button(frame,
                   text="Sans fichier Excel",
                   
                   command=standar,
                   style="Modern.TButton")
btn_standar.grid(row=0,column=3)

#====== FIN frame =======

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
root.mainloop()              #|
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~