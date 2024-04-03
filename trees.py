import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

st.title('SF Trees')
st.write("""This app analyzes trees in San Francisco using
a dataset kindly provided by SF DPW""")

trees_df = pd.read_csv('trees.csv')

st.write(trees_df)

#grouping acc to dbh
trees_df_dbh = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id']).reset_index()

st.write(trees_df_dbh)
trees_df_dbh.columns = ['dbh', 'tree_count']
st.line_chart(trees_df_dbh, x = 'dbh', y = 'tree_count')

trees_df_dbh['new_column'] = np.random.randn(len(trees_df_dbh)) * 500
st.line_chart(trees_df_dbh)

trees_df = trees_df.dropna(subset=['longitude', 'latitude'])
trees_df = trees_df.sample(n = 1000)
st.map(trees_df)

st.subheader('Plotly Chart')
fig = px.histogram(trees_df['dbh'])
st.plotly_chart(fig)

trees_df.dropna(how='any', inplace=True)
sf_initial_view = pdk.ViewState(
latitude=37.77,
longitude=-122.4,
zoom=11,
pitch=30
)
hx_layer = pdk.Layer(
'HexagonLayer',
data = trees_df,
get_position = ['longitude', 'latitude'],
radius=100,
extruded=True)
st.pydeck_chart(pdk.Deck(
map_style='mapbox://styles/mapbox/light-v9',
initial_view_state=sf_initial_view,
layers = [hx_layer]
))

pd.set_option('display.max_columns', None)
print(trees_df.head())

