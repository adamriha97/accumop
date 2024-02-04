import streamlit as st
import constants as const
from functions import Functions as func


st.set_page_config(page_title="AccuMop - demo", page_icon="world_map", layout="wide") # wide centered

# ---- SIDEBAR ----
st.sidebar.header("Možnosti:")
red_factor = st.sidebar.slider('Míra červenosti:', 0.0, 0.99, 0.0, 0.01)

# ---- MAINPAGE ----
st.title("AccuMop :world_map:")
st.subheader('Demo page', divider='blue')
st.markdown("##")


mx = func.create_demo_matrix(2)
df = func.convert_mx_to_df(func, matrix = mx, red_factor = red_factor)

st.map(df, latitude='latitude', longitude='longitude', color='color_hex', size=350)

mx = func.blur_matrix(func, matrix = mx, power = 1)
df = func.convert_mx_to_df(func, matrix = mx, red_factor = red_factor)

st.map(df, latitude='latitude', longitude='longitude', color='color_hex', size=350)