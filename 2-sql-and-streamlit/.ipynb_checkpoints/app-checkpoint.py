import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3
import plotly.graph_objects as go
import collections
conn = sqlite3.connect('listings.db')
cursor = conn.cursor()

st.title('Airbnb Explorer')

max_price = st.sidebar.slider(min_value = 20, max_value = 1000, step = 25, label = 'select max price')
min_price = st.sidebar.slider(min_value = 20, max_value = 1000, step = 25, label = 'select min price')

records = pd.read_sql("SELECT name FROM neighborhoods ORDER BY name", conn).to_dict('records')
neighborhoods = [record['name'] for record in records]
selected_neighborhoods = st.sidebar.multiselect("Select Neighborhoods", neighborhoods)
# def exclude_not_selected():
# if selected_neighborhoods > 1:
# 

def selected_locations(neighborhoods, max_price = "1000000", min_price = "0"):
    neighborhoods = format_neighborhoods(neighborhoods)
    max_price = str(max_price)
    min_price = str(min_price)
    return pd.read_sql(f'''SELECT locations.*, listings.room_type, AVG(listings.price) as avg_price
    FROM listings
    JOIN locations ON listings.location_id = locations.id
    JOIN neighborhoods ON locations.neighborhood_id = neighborhoods.id
    GROUP BY listings.location_id
    HAVING avg_price < {max_price} AND avg_price > {min_price}
    AND neighborhoods.name in {neighborhoods}
    ;''', conn)
    
def format_neighborhoods(neighborhoods):
    if len(neighborhoods) > 1:
        return tuple(neighborhoods)
    else:
        return f"('{neighborhoods[0]}')"

def room_hist(locations_df):
    locations = locations_df.to_dict('records')
    room_types = [location['room_type'] for location in locations]
    room_hist = dict(collections.Counter(room_types))
    return room_hist

def bar_chart(histogram):
    x_vals = list(histogram.keys())
    y_vals = list(histogram.values())
    bar = go.Bar(x = x_vals, y = y_vals)
    return go.Figure(bar)
        
if len(selected_neighborhoods) > 0:
    neighborhoods = selected_neighborhoods

locations_df = selected_locations(neighborhoods, max_price, min_price)
st.map(locations_df)

hist = room_hist(locations_df)
fig = bar_chart(hist)
st.plotly_chart(fig)