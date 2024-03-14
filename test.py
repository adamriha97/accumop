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
mx_poji_povo = func.convert_data_to_mx(func, df, 'pojistne_POVODEN', normalize=False, round_values=True)

#df_map = func.map_mx_to_df(func, mx)
#print(df_map)

df_map_poji = func.map_mx_to_df_poji(func, mx, mx_poji_povo)
#print(df_map_poji)

df_aggregated = func.aggregate_df(func, df_map_poji, bounds=[0.1, 0.2, 0.3, 1])
print(df_aggregated)

df_aggregated = func.aggregate_df(func, df_map_poji, bounds=[0.1, 0.2, 0.3, 1], aggregated_column='poji')
print(df_aggregated)

print(df_aggregated['poji'].sum())

original_prc = 0.016
prirazka = df_aggregated['poji'].sum() * original_prc
print(prirazka)
pojis = df_aggregated['poji'].to_list()
print(pojis)

max_plus = 0.06
step_plus = max_plus / (len(pojis) - 1)
plus_prirazka = 0
for i in range(1, len(pojis)):
    plus_prirazka = plus_prirazka + (pojis[i] * (original_prc + i * step_plus))
step_minus = original_prc - ((prirazka - plus_prirazka) / pojis[0])

print(step_minus)

print([x / sum(pojis) for x in pojis])