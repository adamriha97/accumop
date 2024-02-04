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

#######################################################################

### st.dataframe(df_selection)
### st.dataframe(result_df)

#######################################################################

# test
# lat_list = np.linspace(min_tude['latitude'], max_tude['latitude'], lat_div).tolist() * long_div
# long_list = [num for num in np.linspace(min_tude['longitude'], max_tude['longitude'], long_div).tolist() for _ in range(lat_div)]
# tude_test = {'latitude': lat_list, 'longitude': long_list}
# st.map(tude_test, size=1000)