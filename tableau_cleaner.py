import streamlit as st

def parse_table(text):
    """
    Transforme le texte collé (avec retours à la ligne et tabulations)
    en une liste de listes.
    """
    rows = text.strip().splitlines()
    table = [row.split('\t') for row in rows]
    return table

def merge_cells(table, row_index, start_col, num_cols):
    """
    Fusionne les cellules d'une même ligne.
    
    Pour la ligne d'indice 'row_index', fusionne les cellules de la colonne 'start_col'
    à 'start_col + num_cols - 1' en concaténant leur contenu (séparé par un espace).
    Ensuite, les cellules en trop sont supprimées.
    
    Retourne un dictionnaire indiquant pour (row_index, start_col) le nombre de colonnes fusionnées.
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
    Convertit la liste de listes en tableau HTML.
    
    La fusion des cellules est gérée grâce à l'attribut colspan.
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
st.markdown("1. Copiez le contenu depuis Excel (texte tabulé).")
st.markdown("2. Collez-le ci-dessous dans le champ.")
st.markdown("3. Cliquez sur **Convertir** pour générer le tableau HTML.")

# Zone de texte pour coller le contenu Excel
user_input = st.text_area("Collez le texte ici :", height=300)

if st.button("Convertir"):
    if user_input.strip():
        # Transformer le texte en tableau (liste de listes)
        table = parse_table(user_input)
        # Fusionner la deuxième ligne (indice 1) pour les colonnes 6, 7, 8 (indices 5, 6, 7)
        merge_info = merge_cells(table, row_index=1, start_col=5, num_cols=3)
        # Générer le code HTML
        html_output = table_to_html(table, merge_info)
        
        st.markdown("### Tableau HTML généré")
        # Affiche le tableau HTML (attention : utilisation de unsafe_allow_html)
        st.markdown(html_output, unsafe_allow_html=True)
        
        st.markdown("### Code HTML")
        st.code(html_output, language='html')
    else:
        st.error("Veuillez coller vos données avant de cliquer sur Convertir.")
