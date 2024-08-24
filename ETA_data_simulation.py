#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install osmnx geopandas folium numpy pandas


# In[4]:


get_ipython().system('pip install numpy==1.22.4')
get_ipython().system('pip install --upgrade scipy')


# In[7]:


import osmnx as ox
import geopandas as gpd
import folium
import numpy as np
import pandas as pd
import random
import time


# In[17]:


import matplotlib.pyplot as plt

north, south, east, west = 12.935, 12.920, 77.634, 77.620

graph = ox.graph_from_bbox(north, south, east, west, network_type='drive')

fig, ax = ox.plot_graph(graph, bgcolor='k', node_color='w', node_size=15, edge_color='#999999', edge_linewidth=1, edge_alpha=0.7)
plt.show()


# In[18]:


edges = ox.graph_to_gdfs(graph, edges=True)


# In[22]:


north, south, east, west = 12.935, 12.920, 77.634, 77.62graph = ox.graph_from_bbox(north, south, east, west, network_type='drive')
nodes, edges = ox.graph_to_gdfs(graph, nodes=True, edges=True)
utm_crs = 'EPSG:32643'
edges = edges.to_crs(utm_crs)

edges['length'] = edges.geometry.length 

segments = edges[edges['length'] < 1000]

fig, ax = ox.plot_graph(graph, bgcolor='k', node_color='w', node_size=15, edge_color='#999999', edge_linewidth=1, edge_alpha=0.7)
plt.show()

print(segments[['length']].head())


# In[23]:


import geopandas as gpd

edges['length'] = edges.geometry.length
segments = edges[edges['length'] < 1000]


# In[24]:


import random

def simulate_gps_data(segments, num_samples=10):
    gps_data = []
    for _ in range(num_samples):
        segment = segments.sample(1)
        length = segment['length'].values[0]
        point = segment.geometry.values[0].interpolate(random.uniform(0, 1))
        gps_data.append((point.y, point.x, length))
    return gps_data

simulated_gps = simulate_gps_data(segments, num_samples=20)


# In[25]:


def calculate_eta(gps_data, average_speed=30):
    eta_data = []
    for lat, lon, length in gps_data:
        time_seconds = (length / 1000) / (average_speed / 3600)
        eta_data.append((lat, lon, time_seconds))
    return eta_data

eta_predictions = calculate_eta(simulated_gps)


# In[27]:


import folium
m = folium.Map(location=[12.9352, 77.6243], zoom_start=14)
for lat, lon, eta in eta_predictions:
    folium.Marker(location=[lat, lon], popup=f"ETA: {eta:.2f} seconds").add_to(m)
m


# In[30]:


north, south, east, west = 12.935, 12.920, 77.634, 77.620

graph = ox.graph_from_bbox(north, south, east, west, network_type='drive')

nodes, edges = ox.graph_to_gdfs(graph, nodes=True, edges=True)

utm_crs = 'EPSG:32643'  # UTM zone 43N for Bangalore
edges = edges.to_crs(utm_crs)

edges['length'] = edges.geometry.length

segments = edges[edges['length'] < 1000]
def simulate_vehicle_movement(segments, speed_kmh=30):
    speed_mps = speed_kmh / 3.6    
    current_segment = segments.sample(1).iloc[0]
    current_length = current_segment['length']    
    position = 0  
    
    while position < current_length:
        remaining_length = current_length - position
        eta = remaining_length / speed_mps 
        
        position += speed_mps  
        print(f"Current Position: {position:.2f} m, ETA: {eta:.2f} seconds")
        time.sleep(1) 

    print("Reached the end of the segment!")

simulate_vehicle_movement(segments)


# In[ ]:




