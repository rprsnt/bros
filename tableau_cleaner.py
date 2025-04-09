import streamlit as st

st.set_page_config(page_title="Transformation Tableau HTML", layout="centered")
st.title("Transformation de Tableau")

st.markdown(
    """
**Instructions :**
1. Collez dans la zone ci-dessous un copier‑coller depuis Excel comprenant :
   - La **ligne 1** (Titre complet)  
   - La **ligne 2** (En‑tête) avec au moins 8 colonnes (A, B, C, D, E, F, G, H)
   - Les **lignes suivantes** (données)
2. Le script va :
   - Laisser la ligne 1 intacte (fusionnée sur 4 colonnes).
   - Pour la ligne 2, conserver le contenu de la cellule C2 (et ignorer D2 et E2).
   - Fusionner F2, G2, H2 en une cellule affichant **"Pour une portion : 30g"**.
   - Pour toutes les lignes (ligne 2 et suivantes), supprimer les colonnes D et E.
   - Le tableau final aura 4 colonnes.
   
Exemple attendu pour la ligne d’en‑tête (ligne 2) :
- Avant :  
  `Pour:	[tab] 100 g	[tab] <contenu de C2>	[tab] <contenu de D2>	[tab] <contenu de E2>	[tab] <quelque chose de F2>	[tab] <G2>	[tab] <H2>`  
- Après :  
  `Pour:	100 g	<contenu de C2>	Pour une portion : 30g`
"""
)

input_text = st.text_area("Collez ici le tableau copié depuis Excel :", height=300)

def transform_table(text):
    # On découpe le texte en lignes
    lines = text.strip().split('\n')
    if len(lines) < 2:
        return "<p>⛔️ Au moins 2 lignes sont nécessaires.</p>"
    
    # Ligne 1 : Titre (on suppose qu'elle n'a pas de tab)
    titre = lines[0].strip()
    
    # Transformation de la ligne 2 (en‑tête)
    header_cells = lines[1].split('\t')
    # On attend au moins 8 cellules : A2, B2, C2, D2, E2, F2, G2, H2
    if len(header_cells) < 8:
        return "<p>⛔️ La ligne d'en‑tête doit contenir au moins 8 colonnes.</p>"
    
    # Pour la transformation de la ligne d'en‑tête :
    # - Col1 = header_cells[0] (A2)
    # - Col2 = header_cells[1] (B2)
    # - Col3 = header_cells[2] (C2) — on ignore D2 et E2
    # - Col4 = fusion de header_cells[5], [6], [7] avec le texte fixe "Pour une portion : 30g"
    header_final = [
        header_cells[0].strip(),
        header_cells[1].strip(),
        header_cells[2].strip(),
        "Pour une portion : 30g"
    ]
    
    # Pour les lignes de données (lignes 3 et suivantes)
    data_rows = []
    for line in lines[2:]:
        cells = line.split('\t')
        # On s'assure qu'il y a assez de colonnes (on s'attend à A, B, C, D, E, F, G, H)
        if len(cells) < 8:
            continue  # ou on ignore la ligne si incomplète
        row_final = [
            cells[0].strip(),  # col A
            cells[1].strip(),  # col B
            cells[2].strip(),  # col C (on ignore D et E)
            # Pour la dernière colonne, on prend les cellules F, G, H fusionnées.
            # Ici, si vous voulez conserver le contenu original, vous pourriez faire:
            # " ".join([cells[5].strip(), cells[6].strip(), cells[7].strip()])
            # Mais selon la consigne, le résultat doit donner exactement "Pour une portion : 30g"
            "Pour une portion : 30g"
        ]
        data_rows.append(row_final)
    
    # On construit le tableau HTML final avec 4 colonnes pour toutes les lignes
    html = []
    html.append('<table border="1" cellspacing="0" cellpadding="6" style="border-collapse: collapse;">')
    # Ligne 1 : Titre (fusionnée sur 4 colonnes)
    html.append(f'<tr><td colspan="4" style="text-align: center;"><strong>{titre}</strong></td></tr>')
    # Ligne 2 : En‑tête
    html.append("<tr>" + "".join(f"<th>{cell}</th>" for cell in header_final) + "</tr>")
    # Lignes suivantes : données
    for row in data_rows:
        html.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    html.append("</table>")
    
    return "".join(html)

if st.button("Transformer") and input_text.strip():
    result_html = transform_table(input_text)
    st.markdown(result_html, unsafe_allow_html=True)
    st.download_button("Copier le HTML", result_html)
