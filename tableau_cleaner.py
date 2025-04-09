import streamlit as st

st.set_page_config(page_title="Nettoyeur Excel INCO", layout="centered")

st.title("🧼 Nettoyeur de tableau Excel (INCO)")

st.markdown("""
Colle ici un tableau brut copié depuis Excel.  
👉 On enlève les `±`, on fusionne les colonnes de la portion,  
et tu pourras **copier le résultat dans le presse-papier** pour le recoller directement dans Excel.
""")

input_text = st.text_area("📋 Colle ici ton tableau :", height=300)

def nettoyer(table: str) -> str:
    lignes = table.strip().split('\n')
    sortie = []

    for i, ligne in enumerate(lignes):
        cols = ligne.split('\t')

        # Supprimer ± et la valeur suivante
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

    st.subheader("✅ Résultat à copier dans Excel :")
    st.text_area("🧾 Résultat :", value=result, height=300, key="result_area")

    st.markdown("""
        <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert("✅ Résultat copié dans le presse-papier !");
            });
        }

        const btn = document.getElementById("copy-btn");
        if (btn) {
            btn.onclick = function() {
                const text = document.getElementById("result_area").value;
                copyToClipboard(text);
            }
        }
        </script>
        <button id="copy-btn" style="
            background-color:#4CAF50;
            color:white;
            padding:10px 15px;
            border:none;
            border-radius:5px;
            cursor:pointer;
            font-weight:bold;
            margin-top:10px;
        ">📋 Copier dans le presse-papier</button>
    """, unsafe_allow_html=True)
