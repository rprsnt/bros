import streamlit as st

st.set_page_config(page_title="Reformateur INCO — Energie + kcal correct", layout="centered")
st.title("🧼 Reformateur INCO — Bloc Energie/kcal avec AR fusionné")

st.markdown("""
Ce script traite les 4 lignes :
- Titre sur toute la largeur (colspan=4)
- En-tête avec fusion "Pour une portion de XXg"
- Energie (kJ) sur une ligne
- (kcal) : sur la ligne suivante
- Le "6%" est fusionné verticalement sur 2 lignes (rowspan=2)
""")

input_text = st.text_area("📋 Colle ici les 4 lignes :", height=300)

def parser(lignes: list[str]) -> str:
    if len(lignes) < 4:
        return "<p>⛔️ Merci de coller exactement les 4 lignes</p>"

    lignes_nettoyees = []

    # 1. Ligne titre
    titre = lignes[0].strip()
    lignes_nettoyees.append(f'<tr><td colspan="4"><strong>{titre}</strong></td></tr>')

    # 2. Ligne en-tête
    en_tete = lignes[1].split('\t')
    fusion = []
    i = 0
    while i < len(en_tete):
        if en_tete[i].strip().startswith("Pour une portion") and i + 2 < len(en_tete):
            fusion.append(f"Pour une portion de {en_tete[i+1].strip()}{en_tete[i+2].strip()}")
            i += 3
        else:
            if en_tete[i].strip():
                fusion.append(en_tete[i].strip())
            i += 1
    lignes_nettoyees.append('<tr>' + ''.join([f'<th>{cell}</th>' for cell in fusion]) + '</tr>')

    # 3. Ligne Energie
    c1 = [col.strip() for col in lignes[2].split('\t') if col.strip() and col.strip() != '±']
    c2 = [col.strip() for col in lignes[3].split('\t') if col.strip() and col.strip() != '±']

    if len(c1) < 5 or len(c2) < 3:
        return "<p>⛔️ Données incomplètes</p>"

    lignes_nettoyees.append(
        f"<tr><td>{c1[0]}</td><td>{c1[1]}</td><td>{c1[3]}</td><td rowspan='2'>{c1[4]}</td></tr>"
    )
    lignes_nettoyees.append(
        f"<tr><td>{c2[0]}</td><td>{c2[1]}</td><td>{c2[2]}</td></tr>"
    )

    html = "<table border='1' cellspacing='0' cellpadding='6' style='border-collapse: collapse;'>" + ''.join(lignes_nettoyees) + "</table>"
    return html

if st.button("🔄 Générer le tableau") and input_text.strip():
    lignes = input_text.strip().split('\n')
    resultat = parser(lignes)
    st.markdown("### ✅ Résultat")
    st.markdown(resultat, unsafe_allow_html=True)
