import pandas as pd
from jinja2 import Template

# Charger le fichier Excel
file_path = "votre_fichier.xlsx"
data = pd.read_excel(file_path)

# Modèle HTML
html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Étiquetage Nutritionnel</title>
</head>
<body>
    <table border="1">
        <caption>ETIQUETAGE NUTRITIONNEL INCO POUR PAYS CE (Règlement UE N° 1169/2011 du 25-10-2011)</caption>
        <tr>
            <th>Pour:</th>
            <th>100 g</th>
            <th>Pour une portion de 30g</th>
            <th>AR(*) par portion</th>
        </tr>
        {% for row in data %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Convertir le tableau en liste de dictionnaires pour le modèle
data_dict = data.values.tolist()

# Créer le HTML
template = Template(html_template)
html_output = template.render(data=data_dict)

# Sauvegarder dans un fichier
output_path = "etiquetage_nutritionnel.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"Le fichier HTML a été généré : {output_path}")
