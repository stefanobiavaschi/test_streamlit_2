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

    scelta_media = st.radio("Visualizza:", [ "Partita singola", "Dati medi", "Dati al minuto" ], horizontal=True)


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

    if scelta_media == "Dati medi":
        mrg_1 = data.loc[data.season == scelta_season].groupby(["Nr", "Giocatore"]).mean().reset_index().round(1)
        mrg_2 = data.loc[data.season == scelta_season].groupby(["Nr", "Giocatore"]).agg( {"MIN":"count"} ).reset_index().rename(columns={"MIN":"Nr_partite"})

        data_mean = mrg_1.merge(mrg_2, on=["Nr", "Giocatore"])
        data_mean["MIN"] = data_mean.sec.apply(lambda x: sec_to_time(x) )

        data_mean['FG%'] = data_mean.apply(lambda row: avg_perc(row['FGM'], row['FGA']), axis=1)
        data_mean['3P%'] = data_mean.apply(lambda row: avg_perc(row['3PM'], row['3PA']), axis=1)
        data_mean['2P%'] = data_mean.apply(lambda row: avg_perc(row['2PM'], row['2PA']), axis=1)
        data_mean['FT%'] = data_mean.apply(lambda row: avg_perc(row['FTM'], row['FTA']), axis=1)
        chart_data = data_mean[[ 'Giocatore', 'sec', 'EFF' ]]
        chart_data['MIN'] = chart_data.sec // 60
        chart_data = chart_data.drop(columns=["sec"])
        
        data_mean = data_mean[['Nr', 'Giocatore', 'Nr_partite', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', '2PM', '2PA',
            '2P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'SR', 'PF', 'PIR', 'EFF' ]]

        data_mean_players = data_mean.loc[data_mean.Giocatore != "Totale"]
        data_mean_team = data_mean.loc[data_mean.Giocatore == "Totale"].reset_index(drop=True).drop(columns=['Nr','MIN'])

        res_vis = df_results.loc[(df_results.Season == scelta_season) & (df_results.my_team == scelta_team)][["Squadra", "Data", "Luogo","Chiav", "Avversari", "W/L"]].reset_index(drop=True)
        st.markdown("### Risultati:")
        st.write(res_vis)
        st.markdown("### Statistiche giocatori:")
        st.write(data_mean_players)
        st.markdown("### Statistiche squadra:")
        st.write(data_mean_team)
        list_player = list(set(list(data.loc[(data.my_team == scelta_team) & (data.season == scelta_season)].Giocatore.values)))
        scelta_player = st.radio("Giocatore:", list_player, horizontal=True)
        st.markdown("Storico Efficienza:")
        st.line_chart(data.loc[(data.my_team == scelta_team) & (data.season == scelta_season) & (data.Giocatore == scelta_player)], x="date", y="EFF")
        st.markdown("Storico Punti:")
        st.line_chart(data.loc[(data.my_team == scelta_team) & (data.season == scelta_season) & (data.Giocatore == scelta_player)], x="date", y="PTS")
        st.markdown("Efficienza rispetto ai minuti impiegati:")
        st.altair_chart(
            chart_data,
            x='MIN',
            y='EFF',
            color='Giocatore',
        )

    if scelta_media == "Dati al minuto":
        st.markdown(
            """
            ... Lavori in corso pt.2 ....  =)
            """
        )
    


if __name__ == "__main__":
    main()