import streamlit as st
import pandas as pd
import os, urllib

from lib.func_data import import_data

list_path =[
    r"data/stats-chiav_dr3_23_24-vs-brembate-22-10-2023.csv",
    r"data/stats-chiav_u14_22_23-vs-pontida-05-03-2023.csv",
    r"data/stats-chiav_u15_23_24-vs-annone-22-10-2023.csv",
    r"data/stats-chiav_u17_22_23-vs-mandello-30-04-2023.csv",
    r"data/stats-chiav_u17_22_23-vs-morbegno-19-02-2023.csv",
    r"data/stats-chiav_u17_22_23-vs-rovagnate-29-01-2023.csv",
    r"data/stats-chiav_prd_22_23-vs-sondrio-05-03-2023.csv"
]


def main():
    st.set_page_config(layout="wide")

    st.markdown("# Basket Chiavenna - Statistiche")
    st.markdown(
        """
        :=)
        """
    )
    st.markdown("<br>", unsafe_allow_html=True)


    data = import_data(list_path)

    list_season = list(set(list(data.season.values)))
    scelta_season = st.radio("Stagione:", list_season)


    list_team = list(set(list(data.loc[data.season == scelta_season].my_team.values)))
    scelta_team = st.radio("Squadra BK Chiavenna:", list_team)

    list_other = list(set(list(data.loc[(data.my_team == scelta_team) & (data.season == scelta_season)].other_team.values)))
    scelta_other = st.radio("Nemico:", list_other)

    data = data.loc[data.my_team == scelta_team]
    data = data.loc[data.other_team == scelta_other]

    data = data.drop(columns=["season","my_team", "other_team", "date"])
    st.write(data)


if __name__ == "__main__":
    main()
