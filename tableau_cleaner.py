import sys

def parse_table(text):
    """
    Transforme le texte collé (avec des retours à la ligne et des tabulations)
    en une liste de listes où chaque sous-liste représente une ligne.
    """
    rows = text.strip().splitlines()
    table = [row.split('\t') for row in rows]
    return table

def merge_cells(table, row_index, start_col, num_cols):
    """
    Fusionne les cellules d'une même ligne.
    
    Pour la ligne d'indice 'row_index', les cellules de la colonne 'start_col' jusqu'à 
    'start_col + num_cols - 1' seront fusionnées en une seule cellule.
    
    Le contenu de la nouvelle cellule sera la concaténation des contenus originaux,
    séparés par un espace. Ensuite, on supprime les cellules redondantes.
    
    Renvoie un dictionnaire de fusion indiquant pour (row_index, start_col) 
    le nombre de colonnes fusionnées.
    """
    merge_info = {}
    if row_index < len(table) and start_col < len(table[row_index]):
        # Concaténer les cellules à fusionner
        merged_text = " ".join(cell.strip() for cell in table[row_index][start_col:start_col+num_cols])
        # Remplacer le contenu de la première cellule par le texte fusionné
        table[row_index][start_col] = merged_text
        # Supprimer les cellules supplémentaires qui viennent d'être fusionnées
        for _ in range(num_cols - 1):
            del table[row_index][start_col+1]
        # Enregistrer l'information de fusion pour l'affichage HTML (colspan)
        merge_info[(row_index, start_col)] = num_cols
    return merge_info

def table_to_html(table, merge_info):
    """
    Convertit la liste de listes en un tableau HTML.
    
    Les informations de fusion sont utilisées pour ajouter un attribut colspan aux
    cellules fusionnées.
    """
    html = '<table border="1">\n'
    for i, row in enumerate(table):
        html += "  <tr>\n"
        col_index = 0
        while col_index < len(row):
            # Vérifier si cette cellule a été fusionnée à partir de la fonction merge_cells.
            if (i, col_index) in merge_info:
                colspan = merge_info[(i, col_index)]
                html += f'    <td colspan="{colspan}">{row[col_index]}</td>\n'
                col_index += colspan
            else:
                html += f'    <td>{row[col_index]}</td>\n'
                col_index += 1
        html += "  </tr>\n"
    html += "</table>"
    return html

def main():
    """
    Lecture du texte collé depuis l'entrée standard, application de la fusion
    puis affichage du tableau HTML généré.
    
    Pour tester : 
    - Exécutez le script et collez le texte (par copier-coller depuis Excel), 
      puis terminez par Ctrl+D (ou Ctrl+Z sous Windows).
    """
    print("Collez votre texte provenant d'Excel et terminez par Ctrl+D (Linux/Mac) ou Ctrl+Z (Windows):")
    pasted_text = sys.stdin.read()
    table = parse_table(pasted_text)
    
    # Fusionner la cellule de la deuxième ligne (index 1), colonnes F2, G2, et H2.
    # En Excel, F = 6ème colonne, G = 7ème, H = 8ème, ce qui correspond ici à l'indice 5.
    merge_info = merge_cells(table, row_index=1, start_col=5, num_cols=3)
    
    html = table_to_html(table, merge_info)
    print("\nTableau HTML généré:")
    print(html)

if __name__ == '__main__':
    main()
