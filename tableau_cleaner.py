import streamlit as st

st.set_page_config(page_title="INCO Energie/kcal", layout="centered")
st.title("Reformateur INCO — Bloc Energie / kcal")

input_text = st.text_area("Colle les 4 lignes :", height=300)

def render_table(lignes):
    c1 = [col.strip() for col in lignes[2].split('\t') if col.strip() and col.strip() != '±']
    c2 = [col.strip() for col in lignes[3].split('\t') if col.strip() and col.strip() != '±']

    html = "<table border='1' cellspacing='0' cellpadding='6' style='border-collapse: collapse;'>"

    # Ligne 1 : titre
    html += f"<tr><td colspan='5'><strong>{lignes[0].strip()}</strong></td></tr>"

    # Ligne 2 : en-tête avec fusion portion
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
    html += '<tr>' + ''.join(f'<th>{col}</th>' for col in fusion) + '</tr>'

    # Ligne 3 : Energie (kJ)
    html += f"<tr><td>Energie</td><td>{c1[0]}</td><td>{c1[1]}</td><td>{c1[3]}</td><td rowspan='2'>{c1[4]}</td></tr>"

    # Ligne 4 : (kcal)
    html += f"<tr><td></td><td>{c2[0]}</td><td>{c2[1]}</td><td>{c2[2]}</td></tr>"

    html += "</table>"
    return html

if st.button("Générer") and input_text.strip():
    lignes = input_text.strip().split('\n')
    st.markdown(render_table(lignes), unsafe_allow_html=True)
