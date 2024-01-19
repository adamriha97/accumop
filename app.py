import pandas as pd
import streamlit as st

st.set_page_config(page_title="AccuMop", page_icon="world_map", layout="wide")

file_path = 'akumulace_data.csv'
df = pd.read_csv(file_path, encoding='Windows-1252', sep=';')

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
KRAJ_NAZEV = st.sidebar.multiselect(
    "Select the KRAJ_NAZEV:",
    options=df["KRAJ_NAZEV"].unique(),
    default=df["KRAJ_NAZEV"].unique()
)

df_selection = df.query(
    "KRAJ_NAZEV == @KRAJ_NAZEV"
)

st.dataframe(df_selection)