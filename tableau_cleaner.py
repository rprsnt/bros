import streamlit as st

st.set_page_config(page_title="INCO Bloc Énergie Final", layout="centered")
st.title("Reformateur INCO — Bloc Énergie Final")

input_text = st.text_area("Collez ici exactement 4 lignes (Titre, En-tête, Ligne Énergie, Ligne (kcal)) :", height=300)

def process_line(line_parts):
    result = []
    skip = False
    for part in line_parts:
        if skip:
            skip = False
            continue
        if part.strip() == '±':
            skip = True
            continue
        if part.strip():
            result.append(part.strip())
    return result

def generate_table(lines):
    # On attend exactement 4 lignes en entrée.
    # Ligne 0 : Titre complet
    titre = lines[0].strip()
    # Ligne 1 : En-tête
    en_tete_parts = lines[1].split('\t')
    header = []
    i = 0
    while i < len(en_tete_parts):
        current = en_tete_parts[i].strip()
        if current.startswith("Pour une portion") and i + 2 < len(en_tete_parts):
            # Fusionner "Pour une portion :", la valeur et l'unité.
            header.append(f"Pour une portion de {en_tete_parts[i+1].strip()}{en_tete_parts[i+2].strip()}")
            i += 3
        else:
            if current:
                header.append(current)
            i += 1
    # On s'assure d'avoir exactement 4 colonnes pour l'en-tête en ajoutant une colonne vide pour AR (*)
    while len(header) < 4:
        header.append("")
    
    # Ligne 2 : Énergie (kJ)
    energy_parts = process_line(lines[2].split('\t'))
    # On suppose que energy_parts donne : 
    # ["Energie (kJ) :", "1775", "527", "6%"] 
    # (le "6%" sera utilisé pour la fusion verticale)
    
    # Ligne 3 : (kcal)
    kcal_parts = process_line(lines[3].split('\t'))
    # On suppose que kcal_parts donne :
    # ["(kcal) :", "425", "126"]
    
    # Construction du tableau HTML à 5 colonnes
    # La 5e colonne est réservée à AR, avec le "6%" fusionné sur 2 lignes.
    html = "<table border='1' cellspacing='0' cellpadding='6' style='border-collapse: collapse;'>"
    # Ligne de titre (sur 5 colonnes)
    html += f"<tr><td colspan='5'><strong>{titre}</strong></td></tr>"
    # En-tête : on place les 4 colonnes de header et on ajoute une 5e colonne vide
    html += "<tr>" + "".join(f"<th>{col}</th>" for col in header) + "<th>AR(*) par portion</th></tr>"
    # Ligne Énergie
    # Colonne 1 : "Energie (kJ) :"
    # Colonne 2 : première valeur (100 g) => energy_parts[1]
    # Colonne 3 : deuxième valeur (portion) => energy_parts[2]
    # Colonne 4 : on laisse vide (pour respecter la structure)
    # Colonne 5 : "6%" (fusionné sur 2 lignes)
    if len(energy_parts) < 4:
        return "<p>⛔️ Ligne Énergie incomplète</p>"
    html += f"<tr><td>{energy_parts[0]}</td><td>{energy_parts[1]}</td><td>{energy_parts[2]}</td><td></td><td rowspan='2'>{energy_parts[3]}</td></tr>"
    # Ligne (kcal)
    # Colonne 1 : vide (indenté)
    # Colonne 2 : (kcal) :
    # Colonne 3 : première valeur (100 g) => kcal_parts[1]
    # Colonne 4 : deuxième valeur (portion) => kcal_parts[2]
    if len(kcal_parts) < 3:
        return "<p>⛔️ Ligne (kcal) incomplète</p>"
    html += f"<tr><td></td><td>{kcal_parts[0]}</td><td>{kcal_parts[1]}</td><td>{kcal_parts[2]}</td></tr>"
    html += "</table>"
    return html

if st.button("Générer") and input_text.strip():
    lines = input_text.strip().split('\n')
    if len(lines) < 4:
        st.error("Merci de coller exactement 4 lignes.")
    else:
        st.markdown(generate_table(lines), unsafe_allow_html=True)
