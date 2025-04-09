import streamlit as st

st.set_page_config(page_title="Reformateur INCO", layout="centered")

st.title("🧼 Reformateur de tableau Excel INCO (structure stricte)")

st.markdown("""
Ce script :
- Supprime toutes les colonnes `±` **et** la valeur qui suit
- Fusionne `"Pour une portion :"`, `30`, `g` → `"Pour une portion de 30g"`
- Supprime les colonnes vides et les `#REF!`
- Respecte strictement la **structure et les alignements**
""")

input_text = st.text_area("📋 Colle ici ton tableau brut depuis Excel :", height=300)

def reformater(table: str) -> str:
    lignes = table.strip().split('\n')
    lignes_nettoyees = []

    for idx, ligne in enumerate(lignes):
        colonnes = ligne.split('\t')

        # Étape 1 : supprimer les colonnes ± et leurs valeurs
        i = 0
        clean = []
        while i < len(colonnes):
            if colonnes[i].strip() == '±':
                i += 2
            else:
                clean.append(colonnes[i])
                i += 1

        # Étape 2 : supprimer les colonnes vides ou contenant #REF!
        clean = [col for col in clean if col.strip() != '' and not col.strip().startswith('#REF!')]

        # Étape 3 : fusionner "Pour une portion :", "30", "g" → "Pour une portion de 30g"
        if idx == 1:  # ligne des en-têtes
            fusion = []
            i = 0
            while i < len(clean):
                if clean[i].strip().startswith("Pour une portion"):
                    fusion.append("Pour une portion de 30g")
                    i += 3
                else:
                    fusion.append(clean[i])
                    i += 1
            lignes_nettoyees.append('\t'.join(fusion))
        else:
            lignes_nettoyees.append('\t'.join(clean))

    return '\n'.join(lignes_nettoyees)

if st.button("🔄 Reformater") and input_text.strip():
    resultat = reformater(input_text)

    st.subheader("✅ Résultat tabulé à coller dans Excel :")
    st.text_area("🧾 Résultat brut :", value=resultat, height=300)

    # Tableau HTML (copiable dans Word / CKEditor)
    st.subheader("📋 Ou copie ce tableau visuel pour CKEditor / Word :")

    html = "<table border='1' cellspacing='0' cellpadding='4'>"
    for ligne in resultat.strip().split('\n'):
        html += "<tr>"
        for cellule in ligne.split('\t'):
            tag = "th" if ligne == resultat.strip().split('\n')[1] else "td"
            html += f"<{tag}>{cellule.strip()}</{tag}>"
        html += "</tr>"
    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)
    st.markdown("_👉 Sélectionne manuellement ce tableau, puis colle-le dans CKEditor ou Word._")
