import streamlit as st

st.set_page_config(page_title="Nettoyeur Excel INCO", layout="centered")

st.title("🧼 Nettoyeur de tableau Excel (INCO)")
st.markdown("""
Colle ci-dessous un tableau brut copié depuis Excel.  
👉 Le script supprimera les colonnes `±`, fusionnera les colonnes "Pour une portion : 30 g",  
et affichera un **résultat propre** que tu peux **recoller directement dans Excel**.
""")

input_text = st.text_area("📋 Ton tableau brut (copié depuis Excel) :", height=300)

def nettoyer(table: str) -> str:
    lignes = table.strip().split('\n')
    sortie = []

    for i, ligne in enumerate(lignes):
        cols = ligne.split('\t')

        # Supprimer les colonnes "±" et leurs valeurs
        clean = []
        skip = False
        for col in cols:
            if col.strip() == '±':
                skip = True
                continue
            if skip:
                skip = False
                continue
            clean.append(col)

        # Fusionner "Pour une portion", "30", "g"
        if i == 1:  # ligne d'en-tête
            fusion = []
            j = 0
            while j < len(clean):
                if clean[j].startswith("Pour une portion"):
                    fusion.append("Pour une portion (30 g)")
                    j += 3
                else:
                    fusion.append(clean[j])
                    j += 1
            sortie.append('\t'.join(fusion))
        else:
            sortie.append('\t'.join(clean))

    return '\n'.join(sortie)

if st.button("🔄 Nettoyer le tableau") and input_text.strip():
    result = nettoyer(input_text)

    st.subheader("✅ Résultat prêt à coller dans Excel :")
    st.code(result, language='text')

    # Ajouter un bouton de copie dans le presse-papier
    st.markdown(f"""
    <button onclick="navigator.clipboard.writeText(`{result}`)" style="
        background-color:#4CAF50;
        color:white;
        padding:10px 15px;
        border:none;
        border-radius:5px;
        cursor:pointer;
        font-weight:bold;
    ">
        📋 Copier dans le presse-papier
    </button>
    """, unsafe_allow_html=True)
