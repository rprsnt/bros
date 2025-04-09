import streamlit as st
import re

def parse_table(text):
    """
    Transforme le texte copié en une liste de listes.
    
    On tente d'abord de découper les colonnes par tabulation.
    Si aucune tabulation n'est détectée dans une ligne, on découpe par 
    séquences d'au moins deux espaces.
    """
    rows = text.strip().splitlines()
    table = []
    for row in rows:
        if "\t" in row:
            columns = row.split("\t")
        else:
            columns = re.split(r'\s{2,}', row)
        table.append(columns)
    return table

def merge_cells(table, row_index, start_col, num_cols):
    """
    Fusionne les cellules d'une même ligne.
    
    Pour la ligne d'indice `row_index`, fusionne les cellules allant de la colonne `start_col`
    à la colonne `start_col + num_cols - 1` en concaténant leur contenu séparé par un espace.
    
    Si la ligne ne comporte pas suffisamment de colonnes, affiche une erreur.
    Renvoie un dictionnaire merge_info avec la position (row_index, start_col) et le nombre
    de colonnes fusionnées (à utiliser pour l'attribut colspan en HTML).
    """
    merge_info = {}
    if row_index < len(table):
        row = table[row_index]
        if len(row) < start_col + num_cols:
            st.error(f"La ligne {row_index+1} ne contient pas assez de colonnes pour fusionner {num_cols} cellules à partir de la colonne {start_col+1}.")
            return merge_info
        # Concatène le contenu des cellules à fusionner
        merged_text = " ".join(cell.strip() for cell in row[start_col:start_col+num_cols])
        table[row_index][start_col] = merged_text
        # Supprime les cellules supplémentaires
        for _ in range(num_cols - 1):
            del table[row_index][start_col+1]
        merge_info[(row_index, start_col)] = num_cols
    return merge_info

def table_to_html(table, merge_info):
    """
    Convertit la liste de listes en code HTML, en gérant l'attribut colspan pour les fusions.
    """
    html = '<table border="1" style="border-collapse: collapse;">\n'
    for i, row in enumerate(table):
        html += "  <tr>\n"
        j = 0
        while j < len(row):
            if (i, j) in merge_info:
                colspan = merge_info[(i, j)]
                html += f'    <td colspan="{colspan}" style="padding:5px;">{row[j]}</td>\n'
                j += colspan
            else:
                html += f'    <td style="padding:5px;">{row[j]}</td>\n'
                j += 1
        html += "  </tr>\n"
    html += "</table>"
    return html

st.title("Conversion de données Excel en Tableau HTML")

st.markdown("### Instructions")
st.markdown("1. Copiez le contenu depuis Excel (le texte doit être sous forme tabulée ou avec des espaces multiples).")
st.markdown("2. Collez-le dans le champ ci-dessous.")
st.markdown("3. Cliquez sur **Convertir** pour générer le tableau HTML avec fusion des cellules.")

# Zone de texte pour coller les données
user_input = st.text_area("Collez ici votre texte :", height=300)

if st.button("Convertir"):
    if user_input.strip():
        # Transformer le texte collé en tableau (liste de listes)
        table = parse_table(user_input)
        st.write("Tableau brut :", table)
        
        # On fusionne la deuxième ligne (indice 1) pour les colonnes F2, G2 et H2.
        # En considérant A=colonne 1, F correspond à l'indice 5 (colonnes 6, 7, 8 = indices 5,6,7).
        merge_info = merge_cells(table, row_index=1, start_col=5, num_cols=3)
        st.write("Informations de fusion :", merge_info)
        
        # Conversion en HTML
        html_output = table_to_html(table, merge_info)
        
        st.markdown("### Tableau HTML généré")
        st.markdown(html_output, unsafe_allow_html=True)
        
        st.markdown("### Code HTML généré")
        st.code(html_output, language='html')
    else:
        st.error("Veuillez coller vos données avant de cliquer sur Convertir.")
