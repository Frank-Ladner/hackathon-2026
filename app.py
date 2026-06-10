import streamlit as st

seite = st.sidebar.radio(
    "Menü",
    ["Startseite", "Informationen"],
)

if seite == "Startseite":
    st.title("Mein Hackathon Projekt")
    st.write("Die Umgebung funktioniert.")
else:
    st.title("Informationen")
    st.write("Diese App wurde für den Hackathon 2026 mit Streamlit erstellt.")
