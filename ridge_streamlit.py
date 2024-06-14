# (1) Libraries
import streamlit as st
import folium
from streamlit_folium import st_folium
from ridge_map import RidgeMap
import matplotlib.pyplot as plt
from geopandas.tools import geocode


# (2) Main Functions
# Function to plot ridge map
def plot_ridge_map(bbox, num_lines, lake_flatness, water_ntile, vertical_ratio, linewidth, colormap, map_name):
    rm = RidgeMap(bbox)
    values = rm.get_elevation_data(num_lines=num_lines)
    values = rm.preprocess(values=values, lake_flatness=lake_flatness, water_ntile=water_ntile, vertical_ratio=vertical_ratio)
    fig, ax = plt.subplots(figsize=(12, 8))
    rm.plot_map(values=values, ax=ax, label=map_name, label_y=0.1, label_x=0.55, label_size=40, linewidth=linewidth, line_color=plt.get_cmap(colormap), kind='elevation')
    st.pyplot(fig)

# (3) App Start
# Set Streamlit layout to wide
st.set_page_config(layout="wide")

## (3a) Sidebar Content

st.sidebar.title("About")
st.sidebar.markdown("Create beautiful topographic maps with this interactive webapp, built in Python with [Streamlit](https://docs.streamlit.io/) + [Ridge Map](https://github.com/ColCarroll/ridge_map)")
st.sidebar.markdown("Learn how to **code** a custom map:")
st.sidebar.video('https://youtu.be/rsUQIDe-hjE')
st.sidebar.markdown("Subscribe to the [DeepCharts Youtube Channel](https://www.youtube.com/@DeepCharts)")

st.sidebar.title("Advanced Options")

# Sidebar plot parameters
map_name = st.sidebar.text_input("Add a Title", value="Mt. Shasta")
num_lines = st.sidebar.slider("Number of Lines", min_value=25, max_value=500, value=150)
linewidth = st.sidebar.slider("Line Width", min_value=0.1, max_value=5.0, value=1.0)
vertical_ratio = st.sidebar.slider("Vertical Ratio", min_value=0, max_value=1000, value=200)
lake_flatness = st.sidebar.slider("Lake Flatness", min_value=0.0, max_value=10.0, value=0.0)
water_ntile = st.sidebar.slider("Water Level", min_value=0, max_value=100, value=0)
colormap = st.sidebar.selectbox("Color Scheme", options=plt.colormaps(), index=plt.colormaps().index('viridis'))

## (3b) Main Content

### Title
st.title("Create a Topographic Map in Seconds")

st.write("Make beautiful topographic ridge maps for free.")

### Part 1
st.header("Part 1: Choose Area of Focus")
st.write("Toggle the map to choose a location. The viewable area of the map below will be turned into a ridge map.")


lat, lon = 41.375, -122.25  # Default center location

# Display map for bbox selection
m = folium.Map(location=[lat, lon], zoom_start=10)
output = st_folium(m, width=500, height=350)  # Adjusted size of the map

# Extract bbox coordinates from the current map view
bbox = (-122.5, 41.25, -122.0, 41.5)  # Default bbox
if output and 'bounds' in output:
    bounds = output['bounds']
    bbox = (
        bounds['_southWest']['lng'], bounds['_southWest']['lat'],
        bounds['_northEast']['lng'], bounds['_northEast']['lat']
    )

### Part 2
st.header("Part 2: Create Map")
st.write("Click below to generate the map.")
st.write("For more customization, edit the 'Advanced Options' on the left sidebar before clicking 'Create Ridge Map' button.")

if st.button("Create Ridge Map"):
    plot_ridge_map(bbox, num_lines, lake_flatness, water_ntile, vertical_ratio, linewidth, colormap, map_name)


    