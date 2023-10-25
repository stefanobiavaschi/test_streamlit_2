import streamlit as st
import pandas as pd
import os, urllib

from lib.func_data import import_data

list_path =[r"data/stats-chiav_u15_23_24-vs-annone-22-10-2023.csv",
             r"data/stats-chiav_dr3_23_34-vs-brembate-22-10-2023.csv"
            ]


def main():
    st.set_page_config(layout="wide")

    st.markdown("# Basket Chiavenna - Statistiche")
    st.markdown(
        """
        Seleziona una squadra basket chiavenna ed una squadra avversaria
        """
    )
    st.markdown("<br>", unsafe_allow_html=True)


    data = import_data(list_path)

    list_team = list(set(list(data.my_team.values)))
    scelta_team = st.radio("Scegli un'opzione:", list_team)

    list_other = list(set(list(data.loc[data.my_team == scelta_team].other_team.values)))
    scelta_other = st.radio("Scegli un'opzione:", list_other)

    data = data.loc[data.my_team == scelta_team]
    data = data.loc[data.other_team == scelta_other]

    data = data.drop(columns=["my_team", "other_team", "date"])
    st.write(data)


if __name__ == "__main__":
    main()
