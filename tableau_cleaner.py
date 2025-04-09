from jinja2 import Template

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
            <th>Pour une portion de 30 g</th>
            <th>AR(*) par portion</th>
        </tr>
        {% for row in data %}
        <tr>
            {% for cell in row %}
            <td>{{ cell }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Fonction pour parser un tableau brut collé
def parse_raw_table(raw_text):
    # Séparer les lignes
    lines = raw_text.strip().split("\n")
    # Séparer les colonnes par tabulation ou espaces multiples
    data = [line.split("\t") for line in lines]
    return data

# Entrée utilisateur : collez ici le tableau brut
raw_table = """
Pour:\t100 g\tPour une portion de 30 g\tAR(*) par portion
Energie (kJ):\t1775\t527\t6%
(kcal):\t425\t126\t
Matières grasses (g):\t22\t6,6\t9%
dont acides gras saturés (g):\t3,3\t1,0\t5%
Glucides (g):\t48\t14\t5%
dont sucres (g):\t24\t7,2\t8%
Fibres alimentaires (g):\t6,2\t1,9\t-
Protéines (g):\t5,6\t1,7\t3%
Sel (g):\t0,50\t0,15\t3%
"""

# Traiter le tableau collé
data = parse_raw_table(raw_table)

# Générer le HTML
template = Template(html_template)
html_output = template.render(data=data)

# Sauvegarder dans un fichier
output_path = "etiquetage_nutritionnel.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"Le fichier HTML a été généré : {output_path
