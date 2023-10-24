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

    
    st.write(data)


if __name__ == "__main__":
    main()
