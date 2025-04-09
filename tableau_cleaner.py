import streamlit as st

st.set_page_config(page_title="Formateur de tableau INCO", layout="centered")

st.title("🧼 Reformateur INCO – Copier / Nettoyer / Coller dans Excel")

st.markdown("""
Colle ci-dessous un tableau brut copié depuis Excel.  
Le format est toujours le même :  
- Les colonnes ± et leurs valeurs seront supprimées  
- Les 3 colonnes "Pour une portion :", "30", "g" seront fusionnées  
- Tu obtiendras un texte **tabulé**, recollable dans Excel en tableau  
""")

input_text = st.text_area("📋 Colle ton tableau ici :", height=300)

def reformater(table: str) -> str:
    lignes = table.strip().split('\n')
    lignes_nettoyees = []

    for idx, ligne in enumerate(lignes):
        colonnes = ligne.split('\t')

        # Étape 1 : supprimer toutes les colonnes ± et celle qui suit
        i = 0
        clean = []
        while i < len(colonnes):
            if colonnes[i].strip() == "±":
                i += 2  # on saute ± et sa valeur
            else:
                clean.append(colonnes[i])
                i += 1

        # Étape 2 : fusionner "Pour une portion :", "30", "g"
        if idx == 1:  # ligne d'en-tête
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

    st.subheader("✅ Résultat : à coller dans Excel (Ctrl+V / Cmd+V)")
    st.text_area("🧾 Résultat prêt :", value=resultat, height=300)
