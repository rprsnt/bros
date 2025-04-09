import streamlit as st

st.set_page_config(page_title="Reformateur INCO", layout="centered")

st.title("🧼 Reformateur de tableau Excel INCO")

st.markdown("""
Colle ci-dessous un tableau brut copié depuis Excel.  
Ce script :
- Supprime les colonnes `±` et leurs valeurs
- Fusionne `"Pour une portion :"`, `30`, `g` en `"Pour une portion de 30g"`
- Affiche un résultat que tu peux coller :
  - dans **Excel** depuis le bloc texte
  - dans **CKEditor / Word** depuis le tableau affiché
""")

input_text = st.text_area("📋 Colle ici ton tableau brut :", height=300)

def reformater(table: str) -> str:
    lignes = table.strip().split('\n')
    lignes_nettoyees = []

    for idx, ligne in enumerate(lignes):
        colonnes = ligne.split('\t')

        # Étape 1 : supprimer les colonnes "±" et leur valeur
        i = 0
        clean = []
        while i < len(colonnes):
            if colonnes[i].strip() == "±":
                i += 2
            else:
                clean.append(colonnes[i])
                i += 1

        # Étape 2 : fusionner "Pour une portion :", "30", "g"
        if idx == 1:  # ligne d'en-tête
            fusion = []
            j = 0
            while j < len(clean):
                if clean[j].strip().startswith("Pour une portion"):
                    fusion.append("Pour une portion de 30g")
                    j += 3
                else:
                    fusion.append(clean[j])
                    j += 1
            lignes_nettoyees.append('\t'.join(fusion))
        else:
            lignes_nettoyees.append('\t'.join(clean))

    return '\n'.join(lignes_nettoyees)

if st.button("🔄 Reformater") and input_text.strip():
    resultat = reformater(input_text)

    # Affichage brut pour Excel
    st.subheader("✅ Résultat tabulé à coller dans Excel :")
    st.text_area("🧾 Résultat brut :", value=resultat, height=300)

    # Génération HTML pour CKEditor / Word
    st.subheader("📋 Ou copie ce tableau pour CKEditor ou Word :")

    html = "<table border='1' cellspacing='0' cellpadding='4'>"
    for ligne in resultat.strip().split('\n'):
        html += "<tr>"
        for cellule in ligne.split('\t'):
            tag = "th" if "Pour" in cellule or "Energie" in cellule else "td"
            html += f"<{tag}>{cellule.strip()}</{tag}>"
        html += "</tr>"
    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)
    st.markdown("_👉 Sélectionne manuellement ce tableau avec ta souris, puis copie-colle dans CKEditor._")
