import streamlit as st

st.set_page_config(page_title="INCO — Tableau Final", layout="centered")
st.title("Reformateur INCO — Tableau Final")

input_text = st.text_area(
    "Collez ici EXACTEMENT 4 lignes, chacune séparée par des tabulations :\n"
    "1) Titre (aucune tabulation dans cette ligne)\n"
    "2) En-tête (4 colonnes attendues, par exemple : Pour: [TAB] 100 g [TAB] Pour une portion : [TAB] AR(*) par portion)\n"
    "   Attention : si le collage depuis Excel vous fournit plus de 4 cellules sur cette ligne (ex. : Pour: [TAB] 100 g [TAB] Pour une portion : [TAB] 30 [TAB] g [TAB] AR(*) par portion),\n"
    "   la portion commençant par « Pour une portion » sera automatiquement fusionnée avec les 2 cellules suivantes.\n"
    "3) Ligne Énergie (5 colonnes attendues, par exemple : Energie [TAB] (kJ) : [TAB] 1775 [TAB] 527 [TAB] 6%)\n"
    "4) Ligne (kcal) (4 colonnes attendues, par exemple : (kcal) : [TAB] 425 [TAB] 126 [TAB] <vide>)",
    height=250
)

def merge_header_cells(header):
    """
    Cherche dans la liste header une cellule dont le contenu commence par "pour une portion"
    (insensible à la casse) et, si trouvée et suivie d'au moins 2 autres cellules, les fusionne.
    Par exemple, si header vaut:
        ["Pour:", "100 g", "Pour une portion :", "30", "g", "Autre"],
    alors le résultat sera:
        ["Pour:", "100 g", "Pour une portion : 30 g", "Autre"].
    """
    for i, cell in enumerate(header):
        if cell.lower().startswith("pour une portion"):
            if len(header) >= i + 3:
                merged = " ".join(header[i:i+3])
                header[i] = merged
                # Supprimer les deux cellules suivantes
                del header[i+1:i+3]
            break
    return header

def build_table(lines):
    # Traitement de la première ligne : le titre
    title = lines[0].strip()
    
    # Traitement de la deuxième ligne (En-tête)
    raw_header = lines[1].split('\t')
    # On retire les cellules vides éventuelles
    header = [cell.strip() for cell in raw_header if cell.strip()]
    # Si la ligne contient plus de 4 cellules, on tente de fusionner les cellules relatives à "Pour une portion"
    if len(header) > 4:
        header = merge_header_cells(header)
    # Ajustement pour s'assurer d'avoir exactement 4 cellules
    if len(header) > 4:
        header = header[:4]
    elif len(header) < 4:
        while len(header) < 4:
            header.append("")
    
    # Traitement de la troisième ligne (Ligne Énergie)
    energy_line = lines[2].split('\t')
    energy = [cell.strip() for cell in energy_line if cell.strip()]
    while len(energy) < 5:
        energy.append("")
    
    # Traitement de la quatrième ligne (Ligne (kcal))
    kcal_line = lines[3].split('\t')
    kcal = [cell.strip() for cell in kcal_line if cell.strip()]
    # Si seulement 3 cellules, on insère une cellule vide en début pour l'indentation
    if len(kcal) == 3:
        kcal = [""] + kcal
    while len(kcal) < 4:
        kcal.append("")
    
    # Construction du tableau HTML
    html = []
    html.append('<table border="1" cellspacing="0" cellpadding="6" style="border-collapse: collapse;">')
    # Ligne Titre : fusion sur 5 colonnes
    html.append(f'<tr><td colspan="5"><strong>{title}</strong></td></tr>')
    
    # Ligne En-tête : 4 colonnes issues de la donnée + 1 colonne fixe "AR(*) par portion"
    html.append("<tr>")
    for cell in header:
        html.append(f"<th>{cell}</th>")
    html.append("<th>AR(*) par portion</th>")
    html.append("</tr>")
    
    # Ligne Énergie : 5 colonnes, la 5ᵉ cellule (AR) avec rowspan=2
    html.append("<tr>")
    html.append(f"<td>{energy[0]}</td>")  # Doit être "Energie"
    html.append(f"<td>{energy[1]}</td>")  # Doit être "(kJ) :"
    html.append(f"<td>{energy[2]}</td>")  # Valeur 100g
    html.append(f"<td>{energy[3]}</td>")  # Valeur portion
    html.append(f"<td rowspan='2'>{energy[4]}</td>")  # AR (ex. "6%")
    html.append("</tr>")
    
    # Ligne (kcal) : 4 colonnes (la 5ᵉ est déléguée à la cellule en rowspan)
    html.append("<tr>")
    html.append(f"<td>{kcal[0]}</td>")  # Doit être vide (indentation)
    html.append(f"<td>{kcal[1]}</td>")  # Doit être "(kcal) :"
    html.append(f"<td>{kcal[2]}</td>")  # Valeur 100g
    html.append(f"<td>{kcal[3]}</td>")  # Valeur portion
    html.append("</tr>")
    html.append("</table>")
    
    return "".join(html)

if st.button("Construire le tableau") and input_text.strip():
    lines = input_text.strip().split('\n')
    if len(lines) != 4:
        st.error("Veuillez coller exactement 4 lignes.")
    else:
        html_table = build_table(lines)
        st.markdown(html_table, unsafe_allow_html=True)
