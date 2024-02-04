import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

st.set_page_config(page_title="AccuMop", page_icon="world_map", layout="wide") # wide centered
# ---- MAINPAGE ----
st.title("AccuMop :world_map:")
st.subheader('Clean the Accumulation', divider='blue')
st.markdown("##")

# ---- READ CSV ----
@st.cache_data
def get_data_from_csv():
    file_path = 'akumulace_data.csv'
    df = pd.read_csv(file_path, encoding='Windows-1252', sep=';')
    columns_to_check = ['LATITUDE', 'LONGITUDE']
    df = df.dropna(subset=columns_to_check)
    return df
df = get_data_from_csv()

# ---- SIDEBAR ----
st.sidebar.header("Možnosti:")
blok_km = st.sidebar.slider('Kilometrů čtverečních v jedné oblasti:', 0.5, 10.0, 1.0, 0.25)
red_factor = st.sidebar.slider('Míra červenosti:', 0.0, 0.99, 0.7, 0.01)
show_on_map = st.sidebar.selectbox(
    'Co zobrazit?',
    ('CONTRACT_ID_01_100', 'limit_plneni_01_100'))
st.sidebar.divider()
kraj_filtr = st.sidebar.checkbox('Chci filtrovat konkrétní kraj')
if kraj_filtr:
    KRAJ_NAZEV = st.sidebar.multiselect(
        "Vyberte kraj:",
        options=df["KRAJ_NAZEV"].unique(),
        default=df["KRAJ_NAZEV"].unique(),
        disabled=False
    )
    df_selection = df.query(
        "KRAJ_NAZEV == @KRAJ_NAZEV" # "KRAJ_NAZEV == @KRAJ_NAZEV & OKRES_NAZEV == @OKRES_NAZEV & ORP_NAZEV == @ORP_NAZEV"
    )
else:
    df_selection = df

# krajní body ČR -> 50.251944, 12.091389 49.550278, 18.858889 51.055702, 14.315577 48.5525, 14.333056
min_tude = {'latitude': 48.5525, 'longitude': 12.091389}
max_tude = {'latitude': 51.055702, 'longitude': 18.858889}

# rozdělení mapy na grid -> 485.5, 278.34
long_div = int(485.5 / blok_km)
#lat_div = int((max_tude['latitude'] - min_tude['latitude'])/(max_tude['longitude'] - min_tude['longitude']) * long_div)
lat_div = int((278.34 / 485.5) * long_div)
long_diff = (max_tude['longitude'] - min_tude['longitude']) / long_div
lat_diff = (max_tude['latitude'] - min_tude['latitude']) / lat_div
df_selection['long_grid_mid'] = df_selection['LONGITUDE'] - ((df_selection['LONGITUDE'] - min_tude['longitude'])%long_diff) + (long_diff/2)
df_selection['lat_grid_mid'] = df_selection['LATITUDE'] - ((df_selection['LATITUDE'] - min_tude['latitude'])%lat_diff) + (lat_diff/2)



# normalizace limitu plnění
max_limit_plneni = df_selection['limit_plneni'].max()
df_selection['limit_plneni_01'] = df_selection['limit_plneni'] / max_limit_plneni * 100

result_df = df_selection.groupby(['lat_grid_mid', 'long_grid_mid']).agg({'CONTRACT_ID': 'count', 'limit_plneni': 'sum'}).reset_index()
max_contract_id_count = result_df['CONTRACT_ID'].max()
result_df['CONTRACT_ID_01_100'] = result_df['CONTRACT_ID'] / max_contract_id_count * 1000
max_limit_plneni_sum = result_df['limit_plneni'].max()
result_df['limit_plneni_01_100'] = result_df['limit_plneni'] / max_limit_plneni_sum * 1000
cmap = plt.get_cmap('coolwarm') # 'Blues'
norm = mcolors.Normalize(vmin=0, vmax=1000*(1-red_factor))
result_df['color_hex'] = result_df[show_on_map].apply(lambda x: mcolors.to_hex(cmap(norm(x)))) + 'bf'

### st.map(df_selection, size=1)

st.map(result_df, latitude='lat_grid_mid', longitude='long_grid_mid', color='color_hex', size=show_on_map)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)