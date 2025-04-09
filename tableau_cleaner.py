import streamlit as st

st.set_page_config(page_title="Reformateur INCO", layout="centered")
st.title("🧼 Reformateur de tableau Excel INCO")

st.markdown("""
Ce script :
- Supprime les colonnes `±` et leurs valeurs
- Supprime les colonnes vides et les `#REF!`
- Fusionne les 3 colonnes `"Pour une portion :"`, `30`, `g` **en une seule**, sans modifier leur contenu
- Conserve les unités (kJ, kcal, g) dans la **colonne 1 uniquement**
- Produit un tableau à **4 colonnes fixes** : Label – 100g – Portion – AR
""")

input_text = st.text_area("📋 Colle ici ton tableau brut depuis Excel :", height=300)

def reformater(table: str) -> str:
    lignes = table.strip().split('\n')
    lignes_nettoyees = []

    for idx, ligne in enumerate(lignes):
        colonnes = ligne.split('\t')

        # Étape 1 : suppression de ± et de la valeur suivante
        i = 0
        clean = []
        while i < len(colonnes):
            if colonnes[i].strip() == '±':
                i += 2
            else:
                clean.append(colonnes[i])
                i += 1

        # Étape 2 : suppression des colonnes vides et #REF!
        clean = [c for c in clean if c.strip() and not c.strip().startswith('#REF!')]

        # Étape 3 : ligne d'en-tête à traiter à part (fusion "Pour une portion :", val, unité)
        if idx == 1:
            fusion = []
            j = 0
            while j < len(clean):
                if clean[j].strip().startswith("Pour une portion") and j + 2 < len(clean):
                    texte = f"{clean[j].strip()} {clean[j+1].strip()}{clean[j+2].strip()}"
                    fusion.append(texte)
                    j += 3
                else:
                    fusion.append(clean[j].strip())
                    j += 1
            lignes_nettoyees.append('\t'.join(fusion))
            continue

        # Étape 4 : compléter pour avoir toujours 4 colonnes
        if len(clean) == 4:
            lignes_nettoyees.append('\t'.join([c.strip() for c in clean]))
        elif len(clean) == 3:
            lignes_nettoyees.append('\t'.join([clean[0].strip(), clean[1].strip(), clean[2].strip(), '']))
        else:
            continue  # ignorer les lignes incomplètes ou mal formées

    return '\n'.join(lignes_nettoyees)

if st.button("🔄 Reformater") and input_text.strip():
    resultat = reformater(input_text)

    st.subheader("✅ Résultat brut (Excel) :")
    st.text_area("🧾 Résultat :", value=resultat, height=300)

    st.subheader("📋 Tableau visuel (CKEditor / Word) :")

    html = "<table border='1' cellspacing='0' cellpadding='4'>"
    for ligne in resultat.strip().split('\n'):
        html += "<tr>"
        for cellule in ligne.split('\t'):
            html += f"<td>{cellule.strip()}</td>"
        html += "</tr>"
    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)
    st.markdown("_👉 Sélectionne ce tableau avec ta souris, puis colle-le dans Word ou CKEditor._")
