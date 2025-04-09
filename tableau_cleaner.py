import streamlit as st

st.set_page_config(page_title="INCO — Tableau Final", layout="centered")
st.title("Reformateur INCO — Tableau Final")

input_text = st.text_area(
    "Collez ici EXACTEMENT 4 lignes, chacune séparée par des tabulations :\n"
    "1) Titre (aucune tabulation dans cette ligne)\n"
    "2) En-tête (4 colonnes attendues, par exemple : Pour: [TAB] 100 g [TAB] Pour une portion de 30g [TAB] AR(*) par portion)\n"
    "3) Ligne Énergie (5 colonnes attendues, par exemple : Energie [TAB] (kJ) : [TAB] 1775 [TAB] 527 [TAB] 6%)\n"
    "4) Ligne (kcal) (4 colonnes attendues, par exemple : (kcal) : [TAB] 425 [TAB] 126 [TAB] <vide> )",
    height=250
)

def build_table(lines):
    # Lignes d'entrée
    title = lines[0].strip()
    header_line = lines[1].split('\t')
    energy_line = lines[2].split('\t')
    kcal_line = lines[3].split('\t')
    
    # Pour sécuriser le nombre de colonnes
    # On travaille sur un tableau à 5 colonnes au total.
    # Pour la ligne d'en-tête, on attend 4 colonnes, et on ajoute une colonne vide pour l'AR.
    header = [cell.strip() for cell in header_line if cell.strip()]
    while len(header) < 4:
        header.append("")
    # On ajoute une 5e colonne pour l'AR (à afficher dans le bloc de données)
    
    # Pour la ligne Énergie, on attend 5 colonnes :
    #   Col1 : "Energie", Col2 : "(kJ) :", Col3 : valeur 100g, Col4 : valeur portion, Col5 : AR (ex. "6%")
    energy = [cell.strip() for cell in energy_line if cell.strip()]
    while len(energy) < 5:
        energy.append("")
    # Pour la ligne (kcal), on attend 3 cellules (pour les valeurs) et une cellule d'intitulé,
    # mais on souhaite que la première cellule soit vide (indentation) et que la 5e colonne soit déléguée au "6%" déjà affiché.
    kcal = [cell.strip() for cell in kcal_line if cell.strip()]
    # Si la ligne (kcal) n'a que 3 cellules, on l'interprète comme : [intitulé (kcal) :, valeur 100g, valeur portion]
    if len(kcal) == 3:
        kcal = [""] + kcal  # insère une cellule vide en début de ligne
    while len(kcal) < 4:
        kcal.append("")
    
    # Construction du tableau HTML
    html = []
    html.append('<table border="1" cellspacing="0" cellpadding="6" style="border-collapse: collapse;">')
    # Ligne Titre : fusion sur 5 colonnes
    html.append(f'<tr><td colspan="5"><strong>{title}</strong></td></tr>')
    # Ligne En-tête : 4 colonnes + 1 colonne "AR(*) par portion"
    html.append("<tr>")
    for cell in header:
        html.append(f"<th>{cell}</th>")
    html.append("<th>AR(*) par portion</th>")
    html.append("</tr>")
    # Ligne Énergie : 5 colonnes, la 5e cellule (AR) avec rowspan=2
    html.append("<tr>")
    html.append(f"<td>{energy[0]}</td>")  # Doit être "Energie"
    html.append(f"<td>{energy[1]}</td>")  # Doit être "(kJ) :"
    html.append(f"<td>{energy[2]}</td>")  # Valeur 100g
    html.append(f"<td>{energy[3]}</td>")  # Valeur portion
    html.append(f"<td rowspan='2'>{energy[4]}</td>")  # AR (ex. "6%")
    html.append("</tr>")
    # Ligne (kcal) : 4 colonnes (la 5e est fusionnée)
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
        st.markdown(build_table(lines), unsafe_allow_html=True)
