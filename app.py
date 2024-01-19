import pandas as pd
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

st.map(df_selection, size=1, use_container_width=False)

st.dataframe(df_selection)