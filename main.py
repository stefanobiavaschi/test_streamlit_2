import streamlit as st
import pandas as pd
import os, urllib

from lib.func_data import import_data

list_path =[r"data/stats-chiav_DR3_23_24-vs-Brembate-22-10-2023.csv",
r"data/stats-chiav_U14_22_23-vs-Pontida-05-03-2023.csv",
r"data/stats-chiav_U15_23_24-vs-Annone-22-10-2023.csv",
r"data/stats-chiav_U17_22_23-vs-Mandello-30-04-2023.csv",
r"data/stats-chiav_U17_22_23-vs-Morbegno_u17-19-02-2023.csv",
r"data/stats-chiav_U17_22_23-vs-Rovagnate-29-01-2023.csv",
r"data/stats-chiav_1D_22_23-vs-Sondrio-05-03-2023.csv"
]


def main():
    st.set_page_config(layout="wide")

    st.markdown("# Basket Chiavenna - Statistiche")
    st.markdown(
        """
        Seleziona una squadra basket chiavenna ed una squadra dei nemici
        """
    )
    st.markdown("<br>", unsafe_allow_html=True)


    data = import_data(list_path)

    list_season = list(set(list(data.season.values)))
    scelta_season = st.radio("Seleziona stagione:", list_season)


    list_team = list(set(list(data.loc[data.season == scelta_season].my_team.values)))
    scelta_team = st.radio("Seleziona squadra BK Chiavenna:", list_team)

    list_other = list(set(list(data.loc[(data.my_team == scelta_team) & (data.season == scelta_season)].other_team.values)))
    scelta_other = st.radio("Seleziona un nemico:", list_other)

    data = data.loc[data.my_team == scelta_team]
    data = data.loc[data.other_team == scelta_other]

    data = data.drop(columns=["season","my_team", "other_team", "date"])
    st.write(data)


if __name__ == "__main__":
    main()
