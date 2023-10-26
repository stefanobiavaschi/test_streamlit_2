import pandas as pd


def import_data(list_path):
    L_append = []
    for path in list_path:
        data_temp = pd.read_csv(path).rename(columns={"Nº":"Nr"})
        data_temp.fillna(9999, inplace=True)
        data_temp.Nr = data_temp.Nr.astype(int)
        data_temp.replace(9999, "", inplace=True)
        game = path.split("/")[-1][6:-4]

        split_ = game.split("-")
        season = split_[0][-5:]
        my_team = split_[0][:-6]
        other_team = split_[2]
        date = pd.to_datetime( split_[3] + "-" + split_[4] + "-" + split_[5] )

        data_temp["season"] = season
        data_temp["my_team"] = my_team
        data_temp["other_team"] = other_team
        data_temp["date"] = date

        data_temp["min_"] = data_temp.MIN.apply(lambda x: x.split(":")[0] if len(x.split(":")[0])> 0 else 0).astype(int)
        data_temp["sec_"] = data_temp.MIN.apply(lambda x: x.split(":")[1] if len(x.split(":")) > 1 else 0 ).astype(int)
        data_temp["sec"] = data_temp.sec_ + 60*(data_temp.min_)
        data_temp = data_temp.drop(columns=["min_", "sec_"])

        L_append = L_append + [data_temp]

    data = pd.concat(L_append)
    return data