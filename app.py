import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

st.set_page_config(page_title="AccuMop", page_icon="world_map", layout="centered") # wide

file_path = 'akumulace_data.csv'
df = pd.read_csv(file_path, encoding='Windows-1252', sep=';')

# ---- SIDEBAR ----
st.sidebar.header("Možnosti:")
long_div = st.sidebar.slider('Longtitude grid count:', 0, 500, 250, 10)
KRAJ_NAZEV = st.sidebar.multiselect(
    "Vyberte kraj:",
    options=df["KRAJ_NAZEV"].unique(),
    default=df["KRAJ_NAZEV"].unique(),
    disabled=False
)
OKRES_NAZEV = st.sidebar.multiselect(
    "Vyberte okres:",
    options=df["OKRES_NAZEV"].unique(),
    default=df["OKRES_NAZEV"].unique()
)
ORP_NAZEV = st.sidebar.multiselect(
    "Vyberte obec:",
    options=df["ORP_NAZEV"].unique(),
    default=df["ORP_NAZEV"].unique()
)

columns_to_check = ['LATITUDE', 'LONGITUDE']
df = df.dropna(subset=columns_to_check)

df_selection = df.query(
    "KRAJ_NAZEV == @KRAJ_NAZEV & OKRES_NAZEV == @OKRES_NAZEV & ORP_NAZEV == @ORP_NAZEV"
)

# krajní body ČR -> 50.251944, 12.091389 49.550278, 18.858889 51.055702, 14.315577 48.5525, 14.333056
min_tude = {'latitude': 48.5525, 'longitude': 12.091389}
max_tude = {'latitude': 51.055702, 'longitude': 18.858889}

# rozdělení mapy na grid -> 485.5, 278.34
#long_div = 500
#lat_div = int((max_tude['latitude'] - min_tude['latitude'])/(max_tude['longitude'] - min_tude['longitude']) * long_div)
lat_div = int((278.34 / 485.5) * long_div)
long_diff = (max_tude['longitude'] - min_tude['longitude']) / long_div
lat_diff = (max_tude['latitude'] - min_tude['latitude']) / lat_div
df_selection['long_grid_mid'] = df_selection['LONGITUDE'] - ((df_selection['LONGITUDE'] - min_tude['longitude'])%long_diff) + (long_diff/2)
df_selection['lat_grid_mid'] = df_selection['LATITUDE'] - ((df_selection['LATITUDE'] - min_tude['latitude'])%lat_diff) + (lat_diff/2)

# test
# lat_list = np.linspace(min_tude['latitude'], max_tude['latitude'], lat_div).tolist() * long_div
# long_list = [num for num in np.linspace(min_tude['longitude'], max_tude['longitude'], long_div).tolist() for _ in range(lat_div)]
# tude_test = {'latitude': lat_list, 'longitude': long_list}
# st.map(tude_test, size=1000)

# normalizace limitu plnění
max_limit_plneni = df_selection['limit_plneni'].max()
df_selection['limit_plneni_01'] = df_selection['limit_plneni'] / max_limit_plneni * 100

result_df = df_selection.groupby(['lat_grid_mid', 'long_grid_mid']).agg({'CONTRACT_ID': 'count', 'limit_plneni': 'sum'}).reset_index()
#groupby_df = result_df.copy()
max_contract_id_count = result_df['CONTRACT_ID'].max()
result_df['CONTRACT_ID_01'] = result_df['CONTRACT_ID'] / max_contract_id_count
max_limit_plneni_sum = result_df['limit_plneni'].max()
result_df['limit_plneni_01'] = result_df['limit_plneni'] / max_limit_plneni_sum
#result_df['color_RGBA'] = result_df.apply(lambda df: (df['CONTRACT_ID_01'], 0, (1-df['CONTRACT_ID_01']), 0.5), axis=1)
cmap = plt.get_cmap('coolwarm')
norm = mcolors.Normalize(vmin=0, vmax=1)
result_df['color_hex'] = result_df['CONTRACT_ID_01'].apply(lambda x: mcolors.to_hex(cmap(norm(x)))) + 'bf'
#result_df['color_hex'] = mcolors.to_hex(result_df['color_RGBA'])

df_reset = result_df.reset_index(drop=True)

st.map(df_selection, size=1)

#st.map(df_selection, latitude='lat_grid_mid', longitude='long_grid_mid', size='limit_plneni_01')

st.map(result_df, latitude='lat_grid_mid', longitude='long_grid_mid', color='color_hex', size='CONTRACT_ID')

st.dataframe(df_selection)

#st.dataframe(result_df)
#print(result_df)

#st.dataframe(result_df)

#######################################################################

st.pydeck_chart(pdk.Deck(
    map_style=None, # None 'road' 'satellite'
    initial_view_state=pdk.ViewState(
        latitude=49.75,
        longitude=15.5,
        zoom=7,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=result_df,
           get_position='[long_grid_mid, lat_grid_mid]',
           get_elevation_weight = 'limit_plneni_01',
           radius=300,
           elevation_scale=30000,
           elevation_range=[0, int(result_df['limit_plneni_01'].max())],
           pickable=True,
           extruded=True,
        ),
    ],
))