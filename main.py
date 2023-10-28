import streamlit as st
import pandas as pd
import os, urllib

from lib.func_data import import_data, sec_to_time, displayPDF

list_path =[
    r"data/stats-chiav_dr3_23_24-vs-brembate-22-10-2023.csv",
    r"data/stats-chiav_u14_22_23-vs-pontida-05-03-2023.csv",
    r"data/stats-chiav_u15_23_24-vs-annone-22-10-2023.csv",
    r"data/stats-chiav_u17_22_23-vs-mandello-30-04-2023.csv",
    r"data/stats-chiav_u17_22_23-vs-morbegno-19-02-2023.csv",
    r"data/stats-chiav_u17_22_23-vs-rovagnate-29-01-2023.csv",
    r"data/stats-chiav_prd_22_23-vs-sondrio-05-03-2023.csv",
    r"data/stats-chiav_u15_23_24-vs-lambrugo-28-10-2023.csv"
]


def main():
    st.set_page_config(layout="wide")

    st.markdown("# Basket Chiavenna - Statistiche")
    st.markdown(
        """
        ... Lavori in corso .... 
        """
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # displayPDF('file/logo.pdf')


    data, df_results = import_data(list_path)

    list_season = list(set(list(data.season.values)))
    scelta_season = st.radio("Stagione:", list_season, horizontal=True)


    list_team = list(set(list(data.loc[data.season == scelta_season].my_team.values)))
    scelta_team = st.radio("Squadra BK Chiavenna:", list_team, horizontal=True)

    data = data.loc[ data.my_team == scelta_team ]

    scelta_media = st.radio("Visualizza:", [ "Partita singola", "Dati medi", "Dati al minuto" ], horizontal=True)


    if scelta_media == "Partita singola":
        list_other = list(set(list(data.loc[(data.my_team == scelta_team) & (data.season == scelta_season)].other_team.values)))
        scelta_other = st.radio("Nemico:", list_other, horizontal=True)

        list_date = list(set(list(data.loc[(data.my_team == scelta_team) & (data.season == scelta_season) & \
                                        (data.other_team == scelta_other)].date.values)))
        scelta_date = st.radio("Data:", list_date, horizontal=True)

        data_single = data.loc[(data.other_team == scelta_other) & (data.date == scelta_date)]

        data_single = data_single.drop(columns=["season","my_team", "other_team", "date", "PFD", "sec", "min_", "sec_"])
        st.write(data_single)

    if scelta_media == "Dati medi":
        mrg_1 = data.groupby(["Nr", "Giocatore"]).mean().reset_index()
        mrg_2 = data.groupby(["Nr", "Giocatore"]).agg( {"MIN":"count"} ).reset_index().rename(columns={"MIN":"Nr_partite"})

        data_mean = mrg_1.merge(mrg_2, on=["Nr", "Giocatore"])
        data_mean["MIN"] = data_mean.sec.apply(lambda x: sec_to_time(x) )

        data_mean = data_mean[['Nr', 'Giocatore', 'Nr_partite', 'MIN', 'PTS', 'FGM', 'FGA', '3PM', '3PA', '2PM', '2PA',
            'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'SR', 'PF', 'PIR', 'EFF' ]]
        st.write(data_mean)

    if scelta_media == "Dati al minuto":
        st.markdown(
            """
            ... Lavori in corso pt.2 ....  =)
            """
        )
    


if __name__ == "__main__":
    main()