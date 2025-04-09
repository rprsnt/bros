import streamlit as st

st.set_page_config(page_title="Reformateur INCO", layout="centered")

st.title("🧼 Reformateur de tableau Excel INCO")

st.markdown("""
Ce script :
- Supprime les colonnes `±` et leurs valeurs
- Supprime les colonnes vides et les `#REF!`
- Fusionne les **3 colonnes** "Pour une portion :", valeur, unité (ex : `30`, `g`) **sans modifier leur contenu**
- Reproduit fidèlement un tableau **à 4 colonnes** :
    - Colonne 1 : intitulé complet
    - Colonne 2 : 100 g
    - Colonne 3 : portion
    - Colonne 4 : AR (si présent)
⚠️ Aucun texte n’est modifié. Le script suit uniquement la structure.
""")

input_text = st.text_area("📋 Colle ici ton tableau Excel brut :", height=300)

def reformater(table: str) -> str:
    lignes = table.strip().split('\n')
    lignes_nettoyees = []

    for idx, ligne in enumerate(lignes):
        colonnes = ligne.split('\t')

        # Supprimer ± et sa valeur
        i = 0
        clean = []
        while i < len(colonnes):
            if colonnes[i].strip() == '±':
                i += 2
            else:
                clean.append(colonnes[i])
                i += 1

        # Supprimer colonnes vides et #REF!
        clean = [c for c in clean if c.strip() and not c.strip().startswith('#REF!')]

        # Ligne d'en-tête (avec "Pour une portion :", valeur, g)
        if idx == 1:
            fusion = []
            j = 0
            while j < len(clean):
                if clean[j].strip().startswith("Pour une portion") and j + 2 < len(clean):
                    portion_fusion = f"{clean[j].strip()} {clean[j+1].strip()}{clean[j+2].strip()}"
                    fusion.append(portion_fusion)
                    j += 3
                else:
                    fusion.append(clean[j].strip())
                    j += 1
            lignes_nettoyees.append('\t'.join(fusion))
            continue

        # Données classiques → structure à 4 colonnes : label, val100g, valportion, AR
        if len(clean) >= 4:
            lignes_nettoyees.append('\t'.join([clean[0], clean[1], clean[2], clean[3]]))
        elif len(clean) == 3:
            lignes_nettoyees.append('\t'.join([clean[0], clean[1], clean[2], '']))
        else:
            continue

    return '\n'.join(lignes_nettoyees)

if st.button("🔄 Reformater") and input_text.strip():
    resultat = reformater(input_text)

    st.subheader("✅ Résultat brut (collable dans Excel) :")
    st.text_area("🧾 Résultat :", value=resultat, height=300)

    st.subheader("📋 Aperçu du tableau (copiable dans CKEditor, Word...) :")

    html = "<table border='1' cellspacing='0' cellpadding='4'>"
    for ligne in resultat.strip().split('\n'):
        html += "<tr>"
        for cellule in ligne.split('\t'):
            html += f"<td>{cellule.strip()}</td>"
        html += "</tr>"
    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)
    st.markdown("_Sélectionne ce tableau à la main pour le copier dans CKEditor ou Word._")
