import streamlit as st

st.set_page_config(page_title="Reformateur INCO — Titre + Energie + kcal", layout="centered")
st.title("🧼 Reformateur INCO")

st.markdown("Ce script affiche le titre, l’en-tête, et le bloc Énergie/kcal avec `6%` fusionné.")

input_text = st.text_area("📋 Colle ici les 4 lignes (titre, en-tête, énergie, kcal) :", height=300)

def parser(lignes: list[str]) -> str:
    if len(lignes) < 4:
        return "<p>⛔️ Il faut coller les 4 lignes</p>"

    lignes_nettoyees = []

    # Titre
    titre = lignes[0].strip()
    lignes_nettoyees.append(f'<tr><td colspan="5"><strong>{titre}</strong></td></tr>')

    # En-tête (fusion portion)
    colonnes = lignes[1].split('\t')
    clean = [c.strip() for c in colonnes if c.strip()]
    fusion = []
    i = 0
    while i < len(clean):
        if clean[i].startswith("Pour une portion") and i+2 < len(clean):
            fusion.append(f"Pour une portion de {clean[i+1]}{clean[i+2]}")
            i += 3
        else:
            fusion.append(clean[i])
            i += 1
    lignes_nettoyees.append('<tr>' + ''.join([f'<th>{c}</th>' for c in fusion]) + '</tr>')

    # Ligne énergie
    c1 = [col.strip() for col in lignes[2].split('\t') if col.strip() and col.strip() != '±']
    # Ligne kcal
    c2 = [col.strip() for col in lignes[3].split('\t') if col.strip() and col.strip() != '±']

    if len(c1) < 5 or len(c2) < 3:
        return "<p>⛔️ Données énergie/kcal incomplètes</p>"

    # Ligne 1 : Energie
    lignes_nettoyees.append(
        f"<tr><td>Energie</td><td>{c1[0]}</td><td>{c1[1]}</td><td>{c1[3]}</td><td rowspan='2'>{c1[4]}</td></tr>"
    )
    # Ligne 2 : kcal
    lignes_nettoyees.append(
        f"<tr><td></td><td>{c2[0]}</td><td>{c2[1]}</td><td>{c2[2]}</td></tr>"
    )

    html = "<table border='1' cellspacing='0' cellpadding='6' style='border-collapse: collapse;'>" + ''.join(lignes_nettoyees) + "</table>"
    return html

if st.button("🔄 Générer le tableau") and input_text.strip():
    lignes = input_text.strip().split('\n')
    resultat = parser(lignes)
    st.markdown("### ✅ Résultat")
    st.markdown(resultat, unsafe_allow_html=True)
