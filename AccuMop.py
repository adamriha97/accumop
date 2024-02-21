import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from functions import Functions as func


coordinates_matrix = func.create_coordinates_matrix()
st.set_page_config(page_title="AccuMop", page_icon="world_map", layout="wide") # wide centered

# ---- READ CSV ----
@st.cache_data
def get_data_from_csv(file_path):
    df = pd.read_csv(file_path, encoding='Windows-1252', sep=';')
    columns_to_check = ['lat_grid_mid', 'long_grid_mid']
    df = df.dropna(subset=columns_to_check)
    return df
# main data
df = get_data_from_csv(file_path = './data/streamlit_data_20240220_skody_cut.csv') # streamlit_data_skody
# zone data
df_zone = get_data_from_csv(file_path = './data/DATA_MATRIX_FLOOD_ZONE_A.csv')

# ---- SIDEBAR ----
st.sidebar.header("Možnosti:")
map_option = st.sidebar.radio('Jakou statistiku zobrazit?', ('skody', 'plneni', 'propojistenost'))
if map_option == 'skody':
    risks = ('POVODEN_cut', 'ZAPLAVA_cut', 'VICHRICE_cut', 'KRUPOBITI_cut', 'POVODEN', 'ZAPLAVA', 'VICHRICE', 'KRUPOBITI')
else:
    risks = ('Všechna rizika', 'VICHRICE', 'KRUPOBITI', 'POVODEN', 'ZAPLAVA', 'POV_ZAP')
risk_on_map = st.sidebar.selectbox(
    'Jaké riziko zobrazit?',
    risks)
red_factor = st.sidebar.slider('Míra červenosti:', 0.0, 0.99, 0.0, 0.01)
blur_distance = st.sidebar.slider('Rozmělnění - vzdálenost:', 1, 10, 3, 1)
blur_power = st.sidebar.slider('Rozmělnění - snížení efektu:', 0.0, 3.0, 1.0, 0.1)

if risk_on_map == 'Všechna rizika':
    show_on_map = '1'
else:
    show_on_map = '_' + risk_on_map + '1'
show_on_map = map_option + show_on_map

# ---- MAINPAGE ----
st.title("AccuMop :world_map:")
st.subheader('Clean the Accumulation', divider='blue')
st.markdown("##")

cmap = plt.get_cmap('coolwarm') # 'Blues'
norm = mcolors.Normalize(vmin=0, vmax=1*(1-red_factor))
df['color_hex'] = df[show_on_map].apply(lambda x: mcolors.to_hex(cmap(norm(x)))) + 'bf'
df = df.reset_index()

#st.dataframe(df)

st.map(df, latitude='lat_grid_mid', longitude='long_grid_mid', color='color_hex', size=350)

mx = func.convert_data_to_mx(func, df, show_on_map)
blur_mx = func.blur_matrix(func, matrix = mx, distance = blur_distance, power = blur_power)
df2 = func.convert_mx_to_df(func, matrix = blur_mx, red_factor = red_factor)
st.map(df2, latitude='latitude', longitude='longitude', color='color_hex', size=350)

#mx = func.convert_data_to_mx_test(func, df, show_on_map)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)