import streamlit as st
import pandas as pd
import os, urllib

from lib.func_data import import_data

list_path =[r"data/stats-chiav_u15_23_24-vs-annone-22-10-2023.csv",
             r"data/stats-chiav_dr3_23_34-vs-brembate-22-10-2023.csv"
            ]


def main():
    st.set_page_config(layout="wide")

    st.markdown("# Prova streamlit - stats")
    st.markdown(
        """
        Cartella per provare funzionamento di streamlit
        """
    )
    st.markdown("<br>", unsafe_allow_html=True)


    data = import_data(list_path)

    list_team = list(set(list(data.my_team.values)))
    list_other = list(set(list(data.other_team.values)))

    scelta = st.radio("Scegli un'opzione:", list_team)
    data = data.loc[data.my_team == scelta]
    
    st.write(data)


if __name__ == "__main__":
    main()










import streamlit as st

# Crea un'app Streamlit
st.title("Seleziona una delle tre opzioni")

# Crea un widget di selezione radio per le tre opzioni
opzioni = ["Opzione 1", "Opzione 2", "Opzione 3"]
scelta = st.radio("Scegli un'opzione:", opzioni)

# Variabile per memorizzare la scelta
variabile_scelta = None

# Gestisci la scelta dell'utente
if scelta == "Opzione 1":
    variabile_scelta = "Valore 1"
elif scelta == "Opzione 2":
    variabile_scelta = "Valore 2"
else:
    variabile_scelta = "Valore 3"

# Mostra il valore scelto
st.write(f"Valore scelto: {variabile_scelta}")

