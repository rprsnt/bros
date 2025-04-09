
import streamlit as st

st.set_page_config(page_title="Reformateur INCO", layout="centered")
st.title("🧼 Reformateur INCO (test lignes 1 à 4)")

st.markdown("""
Ce script teste les 4 premières lignes :
1. Titre fusionné sur 4 colonnes
2. Ligne d’en-tête structurée
3. Ligne "Energie (kJ)"
4. Ligne "(kcal)"
""")

input_text = st.text_area("📋 Colle ici ton tableau brut :", height=300)

def reformater(table: str) -> str:
    lignes = table.strip().split('\n')
    lignes_nettoyees = []

    for idx, ligne in enumerate(lignes):
        colonnes = ligne.split('\t')

        # Supprimer les colonnes ± et les valeurs qui les suivent
        i = 0
        clean = []
        while i < len(colonnes):
            if colonnes[i].strip() == '±':
                i += 2
            else:
                clean.append(colonnes[i].strip())
                i += 1

        # Supprimer colonnes vides ou "#REF!"
        clean = [c for c in clean if c and not c.startswith('#REF!')]

        if idx == 0:
            # Ligne titre sur 4 colonnes fusionnées
            titre = clean[0]
            lignes_nettoyees.append(f'<tr><td colspan="4"><strong>{titre}</strong></td></tr>')
        elif idx == 1:
            # En-tête avec fusion "Pour une portion : x g"
            fusion = []
            j = 0
            while j < len(clean):
                if clean[j].startswith("Pour une portion") and j+2 < len(clean):
                    portion = f"Pour une portion de {clean[j+1]}{clean[j+2]}"
                    fusion.append(portion)
                    j += 3
                else:
                    fusion.append(clean[j])
                    j += 1
            row = ''.join([f"<th>{cell}</th>" for cell in fusion])
            lignes_nettoyees.append(f"<tr>{row}</tr>")
        elif idx == 2:
            # Ligne Energie (kJ)
            if len(clean) >= 5:
                lignes_nettoyees.append(
                    f"<tr><td>{clean[0]}</td><td>{clean[1]}</td><td>{clean[2]}</td><td>{clean[4]}</td></tr>"
                )
        elif idx == 3:
            # Ligne (kcal) sans AR
            if len(clean) >= 4:
                lignes_nettoyees.append(
                    f"<tr><td></td><td>{clean[0]}</td><td>{clean[1]}</td><td>{clean[3] if len(clean) > 3 else ''}</td></tr>"
                )

    html = "<table border='1' cellspacing='0' cellpadding='4'>" + ''.join(lignes_nettoyees) + "</table>"
    return html

if st.button("🔄 Tester les 4 premières lignes") and input_text.strip():
    resultat = reformater(input_text)
    st.markdown("### 🧪 Résultat visuel")
    st.markdown(resultat, unsafe_allow_html=True)
