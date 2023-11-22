import pandas as pd
import base64
import os

def import_data():
    list_path = os.listdir('data')
    list_path = [ "data//" + path for path in list_path ]
    df_results = pd.DataFrame(columns=["Season", "my_team", "Squadra" ,"Data", "Luogo", "Chiav", "Avversari", "W/L"])
    L_append = []
    for path in list_path:
        data_temp = pd.read_csv(path).rename(columns={"Nº":"Nr"})
        data_temp.fillna(9999, inplace=True)

        avv_tot = data_temp.loc[data_temp.Nr == "Avversari"][["PTS"]].values[0][0]
        chiav_tot = data_temp.loc[data_temp.Nr == 9999 ][["PTS"]].values[0][0]
        casa = data_temp.loc[data_temp.Nr == "Avversari"][["MIN"]].values[0][0]

        if chiav_tot > avv_tot:
            res = "W"
        else:
            res = "L"

        data_temp = data_temp.loc[data_temp.Nr != "Avversari"]

        data_temp.Nr = data_temp.Nr.astype(int)
        data_temp.replace(9999, "", inplace=True)
        game = path.split("/")[-1][6:-4]

        split_ = game.split("-")
        season = split_[0][-5:]
        my_team = split_[0][:-6]
        other_team = split_[2]
        date = pd.to_datetime( split_[5] + "-" + split_[4] + "-" + split_[3] )

        data_temp["season"] = season
        data_temp["my_team"] = my_team
        data_temp["other_team"] = other_team
        data_temp["date"] = date
        data_temp.date = data_temp.date.apply( lambda x: pd.to_datetime( x ).strftime('%d-%m-%Y') )

        data_temp["min_"] = data_temp.MIN.apply(lambda x: x.split(":")[0] if len(x.split(":")[0])> 0 else 0).astype(int)
        data_temp["sec_"] = data_temp.MIN.apply(lambda x: x.split(":")[1] if len(x.split(":")) > 1 else 0 ).astype(int)
        data_temp["sec"] = data_temp.sec_ + 60*(data_temp.min_)

        L_append = L_append + [data_temp]
        df_results.loc[len(df_results)] = [season, my_team, other_team, pd.to_datetime(date), casa, chiav_tot, avv_tot, res ]
        df_results = df_results.sort_values(by='Data')
    df_results.Data = pd.to_datetime(df_results.Data)
    df_results = df_results.sort_values(by=['Data']).reset_index(drop=True)
    df_results.Data = df_results.Data.apply( lambda x: pd.to_datetime( x ).strftime('%d-%m-%Y') )

    data = pd.concat(L_append)
    return data, df_results

def sec_to_time(sec):
    min = int( sec // 60 )
    sec_new = int( sec - (min*60) )
    if min<10:
        min = "0" + str(min)
    if sec_new<10:
        sec_new = "0" + str(sec_new)    
    return f"{min}:{sec_new}"

def avg_perc(m, a):
    if a>0:
        r = round( (m/a)*100 , 1 )
    else:
        r = 0.0
    return str(r) + "%"