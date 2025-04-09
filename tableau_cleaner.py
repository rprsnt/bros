import streamlit as st

st.set_page_config(page_title="Reformateur INCO (test)", layout="centered")
st.title("🧼 Reformateur INCO — Test lignes 1 à 4")

st.markdown("""
Ce test traite **les 4 premières lignes** du tableau INCO :
1. Titre fusionné sur 4 colonnes
2. Ligne d'en-tête avec "Pour une portion : 30g"
3. Ligne "Energie" avec AR
4. Ligne "(kcal)" sans AR
""")

input_text = st.text_area("📋 Colle ici ton tableau brut depuis Excel :", height=300)

def reformater(table: str) -> str:
    lignes = table.strip().split('\n')
    lignes_nettoyees = []

    for ligne in lignes:
        colonnes = ligne.split('\t')

        # Supprimer les colonnes ± et leurs valeurs
        i = 0
        clean = []
        while i < len(colonnes):
            if colonnes[i].strip() == '±':
                i += 2
            else:
                clean.append(colonnes[i].strip())
                i += 1

        # Supprimer les colonnes vides ou "#REF!"
        clean = [c for c in clean if c and not c.startswith('#REF!')]

        if "ETIQUETAGE NUTRITIONNEL INCO" in clean[0]:
            titre = clean[0]
            lignes_nettoyees.append(f'<tr><td colspan="4"><strong>{titre}</strong></td></tr>')

        elif "Pour une portion" in ''.join(clean):
            # Fusionner "Pour une portion :", valeur, g
            fusion = []
            j = 0
            while j < len(clean):
                if clean[j].startswith("Pour une portion") and j+2 < len(clean):
                    fusion.append(f"Pour une portion de {clean[j+1]}{clean[j+2]}")
                    j += 3
                else:
                    fusion.append(clean[j])
                    j += 1
            row = ''.join([f"<th>{cell}</th>" for cell in fusion])
            lignes_nettoyees.append(f"<tr>{row}</tr>")

        elif "Energie" in clean[0] and "(kJ)" in clean[1]:
            if len(clean) >= 5:
                lignes_nettoyees.append(
                    f"<tr><td>{clean[0]}</td><td>{clean[1]}</td><td>{clean[2]}</td><td>{clean[4]}</td></tr>"
                )

        elif "(kcal)" in clean[0]:
            # ligne indentée, sans AR
            if len(clean) >= 3:
                ar = clean[3] if len(clean) > 3 else ''
                lignes_nettoyees.append(
                    f"<tr><td></td><td>{clean[0]}</td><td>{clean[1]}</td><td>{ar}</td></tr>"
                )

    # Génération du tableau HTML
    html = "<table border='1' cellspacing='0' cellpadding='4'>" + ''.join(lignes_nettoyees) + "</table>"
    return html

if st.button("🔄 Tester les 4 premières lignes") and input_text.strip():
    resultat = reformater(input_text)
    st.markdown("### 🧪 Résultat visuel")
    st.markdown(resultat, unsafe_allow_html=True)
