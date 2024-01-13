import streamlit as st
import pandas as pd
from PIL import Image

from lib.func_data import import_data, sec_to_time, avg_perc
from lib.func_page import partita_singola


def main():
    st.set_page_config(
    page_title="Basket Chiavenna - Statistiche",
    page_icon=":random:",
    layout="wide",
    initial_sidebar_state="collapsed"
    )
    st.markdown("# Basket Chiavenna - Statistiche")

    image = Image.open('file/logo.jpg')
    st.image(image, width= 150)

    st.markdown("<br>", unsafe_allow_html=True)

    data, df_results = import_data()

    col1, col2 = st.columns(2)
    list_season = list(set(list(data.season.values)))
    st.session_state.scelta_season = col1.radio("Stagione:", list_season, horizontal=True)

    list_team = list(set(list(data.loc[data.season == st.session_state.scelta_season].my_team.values)))
    st.session_state.scelta_team = col2.radio("Squadra BK Chiavenna:", list_team, horizontal=True)

    data = data.loc[ (data.my_team == st.session_state.scelta_team) & (data.season == st.session_state.scelta_season ) ]

    st.button("Statistiche partite", on_click=partita_singola)
    st.button("Statistiche aggregate")


    res_vis = df_results.loc[(df_results.Season == st.session_state.scelta_season) & (df_results.my_team == st.session_state.scelta_team)][["Squadra", "Data", "Luogo","Chiav", "Avversari", "W/L"]].reset_index(drop=True)
    st.markdown("### Risultati:")
    st.write(res_vis)
    

if __name__ == "__main__":
    main()