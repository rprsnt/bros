import streamlit as st

def parse_table(text):
    """
    Transforme le texte collé (avec des retours à la ligne et des tabulations)
    en une liste de listes, chaque sous-liste représentant une ligne.
    """
    rows = text.strip().splitlines()
    table = [row.split('\t') for row in rows]
    return table

def merge_cells(table, row_index, start_col, num_cols):
    """
    Fusionne les cellules d'une même ligne.
    
    Pour la ligne d'indice 'row_index', les cellules de la colonne 'start_col' 
    jusqu'à 'start_col + num_cols - 1' sont fusionnées en une seule cellule.
    Le contenu est la concaténation des contenus initiaux, séparée par un espace.
    
    Renvoie un dictionnaire enregistrant pour (row_index, start_col) le nombre
    de colonnes fusionnées (sera utilisé lors de l'affichage HTML).
    """
    merge_info = {}
    if row_index < len(table) and start_col < len(table[row_index]):
        merged_text = " ".join(cell.strip() for cell in table[row_index][start_col:start_col+num_cols])
        table[row_index][start_col] = merged_text
        # Supprimer les cellules supplémentaires
        for _ in range(num_cols - 1):
            del table[row_index][start_col+1]
        merge_info[(row_index, start_col)] = num_cols
    return merge_info

def table_to_html(table, merge_info):
    """
    Convertit la liste de listes en un tableau HTML.
    
    Les informations de fusion sont utilisées pour ajouter l'attribut colspan
    aux cellules fusionnées.
    """
    html = '<table border="1" style="border-collapse: collapse;">\n'
    for i, row in enumerate(table):
        html += "  <tr>\n"
        col_index = 0
        while col_index < len(row):
            if (i, col_index) in merge_info:
                colspan = merge_info[(i, col_index)]
                html += f'    <td colspan="{colspan}" style="padding:5px;">{row[col_index]}</td>\n'
                col_index += colspan
            else:
                html += f'    <td style="padding:5px;">{row[col_index]}</td>\n'
                col_index += 1
        html += "  </tr>\n"
    html += "</table>"
    return html

st.title("Conversion de données Excel en Tableau HTML")

st.markdown("### Instructions")
st.markdown("1. Copiez le contenu depuis Excel (il doit être sous forme de texte tabulé).")
st.markdown("2. Collez-le ci-dessous dans le champ prévu.")
st.markdown("3. Cliquez sur **Convertir** pour voir le résultat.")

# Zone de texte pour le copier-coller
user_input = st.text_area("Collez le texte copié depuis Excel ici :", height=300)

if st.button("Convertir"):
    if user_input.strip():
        # Conversion du texte en tableau (liste de listes)
        table = parse_table(user_input)
        
        # Fusionner la deuxième ligne (indice 1) pour les colonnes 6, 7, et 8 (indices 5,6,7)
        merge_info = merge_cells(table, row_index=1, start_col=5, num_cols=3)
        
        # Génération du code HTML
        html_output = table_to_html(table, merge_info)
        
        st.markdown("### Tableau HTML généré")
        # Affiche le tableau HTML dans une zone intégrée
        st.components.v1.html(html_output, height=400)
        
        st.markdown("### Code HTML")
        st.code(html_output, language='html')
    else:
        st.error("Veuillez coller vos données Excel avant de cliquer sur Convertir.")
