import streamlit as st

st.set_page_config(page_title="Test Energie + kcal (fusion 6%)", layout="centered")
st.title("🧼 Reformateur INCO — Energie + kcal avec fusion verticale du %")

input_text = st.text_area("📋 Colle ici les deux lignes (Energie + kcal) :", height=200)

def parser(lignes: list[str]) -> str:
    if len(lignes) < 2:
        return "<p>⛔️ Il faut coller les deux lignes Energie et kcal</p>"

    # Nettoyage des deux lignes
    c1 = [col.strip() for col in lignes[0].split('\t') if col.strip() and col.strip() != '±']
    c2 = [col.strip() for col in lignes[1].split('\t') if col.strip() and col.strip() != '±']

    if len(c1) < 5 or len(c2) < 3:
        return "<p>⛔️ Données insuffisantes</p>"

    # Création du tableau HTML
    html = '<table border="1" cellspacing="0" cellpadding="6" style="border-collapse: collapse;">'

    # Ligne 1
    html += "<tr>"
    html += f"<td>Energie</td><td>{c1[0]}</td><td>{c1[1]}</td><td>{c1[3]}</td><td rowspan='2'>{c1[4]}</td>"
    html += "</tr>"

    # Ligne 2
    html += "<tr>"
    html += f"<td></td><td>{c2[0]}</td><td>{c2[1]}</td><td>{c2[2]}</td>"
    html += "</tr>"

    html += "</table>"
    return html

if st.button("🔄 Générer le tableau") and input_text.strip():
    lignes = input_text.strip().split('\n')
    resultat = parser(lignes)
    st.markdown("### ✅ Résultat")
    st.markdown(resultat, unsafe_allow_html=True)
