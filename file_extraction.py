from pdfquery import PDFQuery
import re

def extraire_type_fin(ligne: str):
    # Cherche un ou plusieurs mots en majuscules à la fin de la chaîne
    # [A-ZÀ-ÖØ-Ý] prend en compte les lettres avec accents
    match = re.search(r'([A-ZÀ-ÖØ-Ý][A-ZÀ-ÖØ-Ý\s\-]+)$', ligne.strip())
    if match:
        valeur = match.group(1).strip()
        # On s'assure qu'il y a au moins 2 lettres et que c'est bien tout en majuscules
        if valeur.isupper() and len(valeur) >= 2:
            return valeur
    return None

pdf = PDFQuery('./data/theatre1.pdf')
pdf.load()

assert pdf.pq is not None
text_elements = pdf.pq('LTTextLineHorizontal')

# Récupération de toutes les lignes du document
text = [pdf.pq(t).text() for t in text_elements]

week = ['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']

# Récupération des dates des sorties
for i in range(len(text)):
    if any(day in text[i].lower() for day in week):
        print("Trouvé à l'index", i, text[i])
        print("Et le titre", i+1, text[i+1])
        if i+2 < len(text):
            type_spectacle = extraire_type_fin(text[i+2])
            if type_spectacle is not None:
                print("Et le type", i+2, type_spectacle)
        print("\n")


