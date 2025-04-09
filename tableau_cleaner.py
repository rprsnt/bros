import streamlit as st

st.set_page_config(page_title="Nettoyeur Excel INCO", layout="centered")

st.title("🧼 Nettoyeur de tableau Excel (INCO)")

st.markdown("Colle ci-dessous ton tableau brut copié depuis Excel.")

input_text = st.text_area("📋 Ton tableau :", height=300)

if st.button("🔄 Nettoyer le tableau") and input_text.strip():
    def nettoyer(table: str) -> str:
        lignes = table.strip().split('\n')
        sortie = []

        for i, ligne in enumerate(lignes):
            cols = ligne.split('\t')

            # Supprime les colonnes "±" et leurs valeurs associées
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

            # Fusionne "Pour une portion", "30", "g"
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

    result = nettoyer(input_text)

    st.subheader("✅ Résultat à coller dans Excel :")
    st.text_area("Résultat :", value=result, height=300)
