import streamlit as st

st.set_page_config(page_title="Nettoyeur de tableau Excel", layout="centered")

st.title("🧼 Nettoyeur de tableau Excel (INCO)")
st.markdown("""
Colle ici un tableau brut depuis Excel :  
- Supprime automatiquement les colonnes `±`  
- Fusionne les colonnes `Pour une portion : 30 g`  
- Résultat directement recollable dans Excel  
""")

input_text = st.text_area("📋 Colle ton tableau ici :", height=300)

def nettoyer_tableau_excel(colle_brut: str) -> str:
    lignes = colle_brut.strip().split('\n')
    lignes_nettoyees = []

    for i, ligne in enumerate(lignes):
        colonnes = ligne.split('\t')

        # Supprimer les colonnes "±" et leur valeur suivante
        colonnes_sans_ecarts = []
        skip = False
        for col in colonnes:
            if col.strip() == '±':
                skip = True
                continue
            if skip:
                skip = False
                continue
            colonnes_sans_ecarts.append(col)

        # Fusionner les colonnes "Pour une portion", "30", "g"
        if i == 0:
            nouvelle_ligne = []
            j = 0
            while j < len(colonnes_sans_ecarts):
                if colonnes_sans_ecarts[j].startswith("Pour une portion"):
                    nouvelle_ligne.append("Pour une portion (30 g)")
                    j += 2
                else:
                    nouvelle_ligne.append(colonnes_sans_ecarts[j])
                j += 1
        else:
            nouvelle_ligne = []
            j = 0
            while j < len(colonnes_sans_ecarts):
                if j + 2 < len(colonnes_sans_ecarts) and colonnes_sans_ecarts[j + 1] == '30' and colonnes_sans_ecarts[j + 2] == 'g':
                    nouvelle_ligne.append(colonnes_sans_ecarts[j])
                    j += 3
                else:
                    nouvelle_ligne.append(colonnes_sans_ecarts[j])
                    j += 1

        lignes_nettoyees.append('\t'.join(nouvelle_ligne))

    return '\n'.join(lignes_nettoyees)

if input_text:
    resultat = nettoyer_tableau_excel(input_text)
    st.subheader("✅ Résultat prêt à coller dans Excel :")
    st.text_area("Résultat", value=resultat, height=300)
