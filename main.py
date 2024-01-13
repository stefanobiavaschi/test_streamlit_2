import streamlit as st
import pandas as pd
from PIL import Image

from lib.func_data import import_data, sec_to_time, avg_perc
from lib.func_page import singola, home, aggregato


def main():
    st.set_page_config(
    page_title="Basket Chiavenna - Statistiche 📈",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
    )
    st.markdown("# Basket Chiavenna - Statistiche")

    image = Image.open('file/logo.jpg')
    st.image(image, width= 150)

    st.markdown("<br>", unsafe_allow_html=True)


    # Definizione delle pagine
    pages = {
        "home": home,
        "singola": singola,
        "aggregato": aggregato,
    }

    # Inizializzazione della sessione
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Esegui la pagina corrispondente
    pages[st.session_state.page]()



if __name__ == "__main__":
    main()