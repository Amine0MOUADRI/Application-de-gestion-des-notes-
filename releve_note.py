import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Image
from tkinter import Tk, filedialog

def generer_releve(etudiant):


    root = Tk()
    root.withdraw()
    root.iconbitmap("maroc.ico")
    fichier = filedialog.asksaveasfilename(
    defaultextension=".pdf",
    filetypes=[("PDF files", "*.pdf")],
    initialfile=f"releve_{etudiant['NOM']}.pdf",
    title="Choisir l'emplacement pour enregistrer le PDF")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    premier_cle = next(iter(etudiant))   #||
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    doc = SimpleDocTemplate(fichier, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    
    logo = Image("LOGO_FP.jpg", width=500, height=100)  
    elements.append(logo)
    elements.append(Spacer(1,80))

    universite = Paragraph("UNIVERSITÉ MOULAY ISMAÏL", styles["Title"])
    faculte=Paragraph("Faculté Polydisciplinaire - Errachidia", styles["Title"])
    elements.append(universite)
    elements.append(faculte)

    elements.append(Spacer(1,40))
    titre = Paragraph("RELEVÉ DE NOTES", styles["Normal"])
    elements.append(titre)


    info = Paragraph(f"ID : {etudiant[premier_cle]}<br/>Nom : {etudiant['NOM']}<br/>Filière : Informatique Appliquée", styles["Normal"])
    elements.append(info)
    elements.append(Spacer(1,20))

    data = [["    Module      ", "  Note / 20   "]]

    for cle,valeur in etudiant.items():

        if cle not in [premier_cle,"NOM","moyenne","Validation"]:
            data.append([cle, valeur])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.grey),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("FONTSIZE",(0,0),(-1,-1),12)
    ]))

    elements.append(table)
    elements.append(Spacer(1,40))

    if etudiant['moyenne'] >= 18:
        mention='Très Bien avec félicitations'
    elif etudiant['moyenne'] >= 16:
        mention='Très Bien'
    elif etudiant['moyenne'] >= 13:
        mention='Bien'
    elif etudiant['moyenne'] >= 11:
        mention='Assez Bien'
    elif etudiant['moyenne'] >= 8:
        mention='insuffisant'
    elif etudiant['moyenne'] >= 0:
        mention='Très insuffisant'

    if etudiant['moyenne'] >= 10:
        validation = "Validé"
    elif etudiant['moyenne'] < 10:
        validation = "Non validé"

    resultat= Paragraph(f"Moyenne : {etudiant['moyenne']} / 20<br/>Mention  : {mention}<br/>Validation  : {validation}", styles["Title"])
    elements.append(resultat)
    

    doc.build(elements)
