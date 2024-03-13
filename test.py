import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import math

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from functions import Functions as func


def get_data_from_csv(file_path):
    df = pd.read_csv(file_path, encoding='Windows-1252', sep=';')
    columns_to_check = ['lat_grid_mid', 'long_grid_mid']
    df = df.dropna(subset=columns_to_check)
    return df

df = get_data_from_csv(file_path = './data/streamlit_data_20240220_skody_cut.csv')
print(df.head())
mx = func.convert_data_to_mx(func, df, 'skody_POVODEN_cut1')
mx_poji_povo = func.convert_data_to_mx(func, df, 'pojistne_POVODEN', normalize=False, fix_none=True)


#df_map = func.map_mx_to_df(func, mx)
#print(df_map)

df_map_poji = func.map_mx_to_df_poji(func, mx, mx_poji_povo)
print(df_map_poji)