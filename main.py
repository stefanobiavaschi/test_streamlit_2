import streamlit as st
import pandas as pd
from PIL import Image

from lib.func_data import import_data, sec_to_time, avg_perc

def main():
    st.set_page_config(layout="wide")

    st.markdown("# Basket Chiavenna - Statistiche")

    image = Image.open('file/logo.jpg')
    st.image(image, width= 150)

    st.markdown("<br>", unsafe_allow_html=True)

    data, df_results = import_data()

    list_season = list(set(list(data.season.values)))
    scelta_season = st.radio("Stagione:", list_season, horizontal=True)

    list_team = list(set(list(data.loc[data.season == scelta_season].my_team.values)))
    scelta_team = st.radio("Squadra BK Chiavenna:", list_team, horizontal=True)

    data = data.loc[ (data.my_team == scelta_team) & (data.season == scelta_season ) ]

    scelta_media = st.radio("Visualizza:", [ "Partita singola", "Dati aggregati"], horizontal=True)


    if scelta_media == "Partita singola":
        list_other = list(set(list(data.loc[(data.my_team == scelta_team) & (data.season == scelta_season)].other_team.values)))
        scelta_other = st.radio("Nemico:", list_other, horizontal=True)

        list_date = list(set(list(data.loc[(data.my_team == scelta_team) & (data.season == scelta_season) & \
                                        (data.other_team == scelta_other)].date.values)))
        scelta_date = st.radio("Data:", list_date, horizontal=True)

        data_single = data.loc[(data.other_team == scelta_other) & (data.date == scelta_date)]

        data_single = data_single.drop(columns=["season","my_team", "other_team", "date", "PFD", "sec", "min_", "sec_"])
        data_single_players = data_single.loc[data_single.Giocatore != "Totale"]
        data_single_team = data_single.loc[data_single.Giocatore == "Totale"].reset_index(drop=True).drop(columns=['Nr','MIN'])

        res_vis = df_results.loc[(df_results.Season == scelta_season) & (df_results.my_team == scelta_team) & (df_results.Squadra == scelta_other) &\
             (df_results.Data == scelta_date) ][["Data","Luogo","Chiav", "Avversari", "W/L"]].reset_index(drop=True)
        st.markdown("### Risultati:")
        st.write(res_vis)
        st.markdown("### Statistiche giocatori:")
        st.write(data_single_players)
        st.markdown("### Statistiche squadra:")
        st.write(data_single_team)

    if scelta_media == "Dati aggregati":
        mrg_1 = data.loc[data.season == scelta_season].drop(columns=["Nr"]).groupby(["Giocatore"]).mean().reset_index().round(1)
        mrg_2 = data.loc[data.season == scelta_season].drop(columns=["Nr"]).groupby(["Giocatore"]).agg( {"MIN":"count"} ).reset_index().rename(columns={"MIN":"Nr_partite"})

        data_mean = mrg_1.merge(mrg_2, on=["Giocatore"])
        data_mean["MIN"] = data_mean.sec.apply(lambda x: sec_to_time(x) )

        data_mean['FG%'] = data_mean.apply(lambda row: avg_perc(row['FGM'], row['FGA']), axis=1)
        data_mean['3P%'] = data_mean.apply(lambda row: avg_perc(row['3PM'], row['3PA']), axis=1)
        data_mean['2P%'] = data_mean.apply(lambda row: avg_perc(row['2PM'], row['2PA']), axis=1)
        data_mean['FT%'] = data_mean.apply(lambda row: avg_perc(row['FTM'], row['FTA']), axis=1)
        chart_data = data_mean[[ 'Giocatore', 'sec', 'EFF' ]]
        chart_data['MIN'] = chart_data.sec // 60
        chart_data = chart_data.drop(columns=["sec"])
        
        data_mean = data_mean[['Giocatore', 'Nr_partite', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', '2PM', '2PA',
            '2P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'SR', 'PF', 'PIR', 'EFF' ]]

        data_mean_players = data_mean.loc[data_mean.Giocatore != "Totale"]
        data_mean_team = data_mean.loc[data_mean.Giocatore == "Totale"].reset_index(drop=True).drop(columns=['MIN'])

        res_vis = df_results.loc[(df_results.Season == scelta_season) & (df_results.my_team == scelta_team)][["Squadra", "Data", "Luogo","Chiav", "Avversari", "W/L"]].reset_index(drop=True)
        st.markdown("### Risultati:")
        st.write(res_vis)
        if (scelta_team == 'chiav_dr3') & (scelta_season == '23_24'):
            st.markdown(f""" Partite mancanti: \n
                    - 13/10/23: Besanese 66 - 52 Chiavenna (L)\n Biavaschi S. 20, Donà M. 10, Geronimi F 7, Nava S. 4, Maraffio L. 4, Scaramellini N. 3, Biavaschi A. 2, Lucantoni A, Martinucci S, Geronimi G, Allievi S """)
        # 
        if (scelta_team == 'chiav_u15') & (scelta_season == '23_24'):
            st.markdown(""" Partite mancanti: \n
                        - 16/11/23: Delebio 70 - 53 Chiavenna (L)\n Gainera L. 22, Cuneo B. 5, Del Giorgio D. 2, Barbaro A. 2, Cipriani P. 5, Sceffer M. 2, Martinucci M, Morelli E, Ravo A. 6, Morelli M. 3, Del Barba D. 6 """)
        # 
        st.markdown("### Statistiche giocatori:")
        st.write(data_mean_players)
        st.markdown("### Statistiche squadra:")
        st.write(data_mean_team)
        list_player = list(set(list(data.loc[(data.my_team == scelta_team) & (data.season == scelta_season)].Giocatore.values)))
        st.markdown("### Storico per voce statistica:")
        scelta_player = st.radio("Giocatore:", list_player, horizontal=True)
        list_feat = ['MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', '2PM', '2PA','2P%', 'FTM', 
                     'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'SR', 'PF', 'PIR', 'EFF' ]
        scelta_feat = st.radio("Voci statistiche:", list_feat, horizontal=True)
        st.markdown(f"Storico per {scelta_feat} - {scelta_player}:")
        st.line_chart(data.loc[(data.season == scelta_season) & (data.my_team == scelta_team) &  (data.Giocatore == scelta_player)], x="date", y=scelta_feat)
    

if __name__ == "__main__":
    main()