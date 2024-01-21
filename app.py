import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="AccuMop", page_icon="world_map", layout="centered") # wide

file_path = 'akumulace_data.csv'
df = pd.read_csv(file_path, encoding='Windows-1252', sep=';')

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
KRAJ_NAZEV = st.sidebar.multiselect(
    "Select the KRAJ_NAZEV:",
    options=df["KRAJ_NAZEV"].unique(),
    default=df["KRAJ_NAZEV"].unique()
)

columns_to_check = ['LATITUDE', 'LONGITUDE']
df = df.dropna(subset=columns_to_check)

df_selection = df.query(
    "KRAJ_NAZEV == @KRAJ_NAZEV"
)

# krajní body ČR -> 50.251944, 12.091389 49.550278, 18.858889 51.055702, 14.315577 48.5525, 14.333056
min_tude = {'latitude': 48.5525, 'longitude': 12.091389}
max_tude = {'latitude': 51.055702, 'longitude': 18.858889}

# rozdělení mapy na grid
long_div = 500
lat_div = int((max_tude['latitude'] - min_tude['latitude'])/(max_tude['longitude'] - min_tude['longitude']) * long_div)

lat_list = np.linspace(min_tude['latitude'], max_tude['latitude'], lat_div).tolist() * long_div
long_list = [num for num in np.linspace(min_tude['longitude'], max_tude['longitude'], long_div).tolist() for _ in range(lat_div)]
tude_test = {'latitude': lat_list, 'longitude': long_list}

st.map(tude_test, size=1)

st.map(df_selection, size=1)

st.dataframe(df_selection)