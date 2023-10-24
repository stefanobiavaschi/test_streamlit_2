# This demo lets you to explore the Udacity self-driving car image dataset.

import streamlit as st
import pandas as pd
import os, urllib

# from lib.io_utils import download_file
# from lib.ui_components import render_frame_selector_ui, render_object_detector_ui
# from lib.image_utils import draw_image_with_boxes, load_image
# from lib.yolo_model import yolo_v3_predict


# from configs import DATA_URL_ROOT, EXTERNAL_DEPENDENCIES


# Download a single file and make its content available as a string.
@st.cache_resource(show_spinner=False)
def get_file_content_as_string(path):
    return open(path, "r").read()


def main():
    st.set_page_config(layout="wide")

    st.markdown("# Prova streamlit - stats")
    st.markdown(
        """
        Cartella per provare funzionamento di streamlit
        """
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Download external dependencies.
    # for filename in EXTERNAL_DEPENDENCIES.keys():
        # download_file(filename)

    # app_mode = st.radio("Choose the app mode", [ "Show the main.py source code", "Run the app"])
    # st.markdown("""---""")
    # if app_mode == "Show the main.py source code":
    #     st.code(get_file_content_as_string("main.py"))
    # elif app_mode == "Run the app":
    #     run()

    data = pd.read_csv(r"C:\Users\BiavaschiStefano\OneDrive - PORINI Srl\Progetti\streamlit_test\data\stats-chiav_u15_23_24-vs-annone-22-10-2023.csv")
    st.write(data)



# This is the main app app itself, which appears when the user selects "Run the app".
# def run():
#     @st.cache_data
#     def create_summary(metadata):
#         one_hot_encoded = pd.get_dummies(metadata[["frame", "label"]], columns=["label"])
#         summary = (
#             one_hot_encoded.groupby(["frame"])
#             .sum()
#             .rename(
#                 columns={
#                     "label_biker": "biker",
#                     "label_car": "car",
#                     "label_pedestrian": "pedestrian",
#                     "label_trafficLight": "traffic light",
#                     "label_truck": "truck",
#                 }
#             )
#         )
#         return summary


if __name__ == "__main__":
    main()
