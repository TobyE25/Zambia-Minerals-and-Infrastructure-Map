#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install folium requests')



# In[ ]:


get_ipython().system('pip install geopandas')


# In[ ]:


get_ipython().system('pip install arcgis')


# In[ ]:


import folium
import requests
import geopandas as gpd
from io import BytesIO

# Step 1: Load GeoJSON from Dropbox (ensure raw content link)
dropbox_url = "https://www.dropbox.com/scl/fi/3j5hbzhixyinm3gf0c7pr/Zambia-Border-Crossings-and-Airports.geojson?rlkey=52izw4fsyqrj6jvv60av505as&dl=1"
response = requests.get(dropbox_url)
geojson_data = response.json()

# Step 2: Create a base map centered on Zambia
m = folium.Map(location=[-13.1339, 27.8493], zoom_start=6)

# Step 3: Add the GeoJSON layer
folium.GeoJson(
    geojson_data,
    name="Zambia Border Crossings and Airports",
    tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Name"])
).add_to(m)

# Step 4: Add layer control
folium.LayerControl().add_to(m)

# Step 5: Save the map
m.save(r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\Mining and Energy Webmap\zambia-ports-webmap-first-iteraton.html")


# In[ ]:





# In[ ]:





# In[42]:


#Converting shapefiles to geojson files


import geopandas as gpd
import os

shapefile_dir = r"C:\Users\EDISON\Downloads\miningsites"
output_geojson = os.path.join(shapefile_dir, "miningsites DRC.geojson")

gdf = gpd.read_file(shapefile_dir)
gdf.to_file(output_geojson, driver="GeoJSON")

print(f"✅ Shapefile converted to GeoJSON: {output_geojson}")


# In[51]:


import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# File paths
input_csv = r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\industrial_projects (1).csv"
output_geojson = r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\industrial_projects.geojson"

# Read the CSV file
df = pd.read_csv(input_csv)

# Ensure 'longitude' and 'latitude' columns are present
if 'longitude' not in df.columns or 'latitude' not in df.columns:
    raise ValueError("The CSV file must contain 'longitude' and 'latitude' columns.")

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df['longitude'], df['latitude'])],
    crs="EPSG:4326"  # WGS 84 (standard for GeoJSON)
)

# Save to GeoJSON
gdf.to_file(output_geojson, driver="GeoJSON")

print(f"✅ CSV successfully converted to GeoJSON: {output_geojson}")


# In[3]:


#Latest webmap version 
#This is the public dissementation version 


import folium
import geopandas as gpd
import os
from shapely.geometry import box
from folium.plugins import FeatureGroupSubGroup
import pandas as pd




print("📍 Starting grouped, slimmed Southern Africa map…")

# 1) Base map _without_ adding the default OSM into the control
m = folium.Map(
    location=[-13.5, 27.8],
    zoom_start=6,
    control=False     # disable the default base layer in the layer control
)
print("✅ Base map created.")

# 1b) Now add OSM back, but with our custom name
folium.TileLayer(
    tiles="OpenStreetMap",
    name="Layer Control",  # this will appear as the only radio in the "base layers" section
    control=False
).add_to(m)

print("Adding title")

# 2) Title and Dashboard Button
header_html = '''
<div style="
    position: fixed; top: 10px; left: 50%;
    transform: translateX(-50%);
    z-index:9999;
    background-color: white;
    padding: 6px 12px;
    border: 2px solid grey;
    border-radius: 4px;
    font-size: 20px;
    font-weight: bold;
    display: flex;
    align-items: center;
">
    ZEL Mining and Infrastructure Map
    <button id="dashboard-toggle" style="
        margin-left: 20px;
        background-color: #007bff;
        color: white;
        padding: 6px 12px;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        font-size: 14px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    ">Show Dashboard</button>
</div>
'''
m.get_root().html.add_child(folium.Element(header_html))
print("✏️ Map title and dashboard button added.")

# 3) Collapsible Dashboard Panel
panel_html = '''
<div id="dashboard-panel" class="dashboard-panel collapsed">
    <iframe id="dashboard-iframe" width="100%" height="100%" src="https://lookerstudio.google.com/embed/reporting/090745d0-4b31-4f50-b3df-b7e5751036d7/page/cpZJF" frameborder="0" allowfullscreen></iframe>
</div>

<style>
.dashboard-panel {
    position: fixed;
    top: 80px;
    right: 5%;
    width: 90%;
    height: 80vh;
    background-color: white;
    padding: 8px;
    border: 1px solid grey;
    border-radius: 4px;
    z-index: 9999;
    transition: top 0.3s ease;
    box-shadow: 4px 4px 12px rgba(0,0,0,0.3);
}

@media (min-width: 600px) {
    .dashboard-panel {
        right: 390px;
        width: 800px;
        height: 600px;
    }
}

.dashboard-panel.collapsed {
    top: -10050px;
}
</style>

<script>
document.getElementById('dashboard-toggle').addEventListener('click', function() {
    const panel = document.getElementById('dashboard-panel');
    this.textContent = panel.classList.toggle('collapsed') ? 'Show Dashboard' : 'Hide Dashboard';
});
</script>
'''
m.get_root().html.add_child(folium.Element(panel_html))
print("📊 Responsive collapsible dashboard added.")


# 4) Styles & file paths
layer_styles = {
    # Mining & Quarries
    "Processing Sites": "#a65628",
    "Quarries": "#e377c2",
    "Mines": "#ff9896",
    "Amethyst Restricted Areas": "#d62728",
    "Artisinal Mining Rights": "#ff7f0e",
    "Bidding Areas": "#bcbd22",
    "Emerald Restricted Areas": "#17becf",
    "Large Scale Exploration Licences": "#aec7e8",
    "Large Scale Gemstone Licences": "#c5b0d5",
    "Large Scale Mining Licences": "#9467bd",
    "Mineral Processing Licences": "#8c564b",
    "Petroleum Licences": "#1f77b4",
    "Prospecting Licences 2008": "#98df8a",
    "Prospecting Permits 2008": "#c49c94",
    "Restricted Areas 1": "#7f7f7f",
    "Restricted Areas 2": "#dbdb8d",
    "Small Scale Gemstone Licences": "#ffbb78",
    "Small Scale Mining Licences": "#2ca02c",
    # DRC Mining and Quarries 
    "DRC Mining Permits": "#91318B",
    "DRC Artisinal Mining Sites": "#c49c94",
    "DRC Processing Entities": "#40029C",
    "DRC Industial Projects": "#21129C",
    # Electricity Infrastructure
    "Power Plants": "#17becf",
    "Power Lines": "#9467bd",
    "Substations": "#bcbd22",
    # Transport Infrastructure
    "Railways Southern Africa": "#8B0000",
    "Major Roads Southern Africa": "#00008B",
    "Export Corridors": "#6B0000",
    "Ports Southern Africa": "#00009A",
    "Ports of Entry and Border Crossings": "#29d6ae",
    #Health
    "Health Facilities Zambia": "#69d4ae"
}

layer_groups = {
    "⬛ Mining & Quarries - Mines and Processing Sites (Source: OSM) ▼": {
        "Processing Sites": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Zambian Mines\Processing SItes.geojson",
        "Quarries":        r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Quarries In Zambia\Quarries.geojson",
        "Mines":           r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Zambian Mines\Location of Mines Zambia.geojson",
    },
        "⬛ Mining & Quarries - Licence Areas (Source: ZMB Mining Cadastre) ▼": {
        "Amethyst Restricted Areas": r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Amethyst_Resticted_Areas.geojson",
        "Artisinal Mining Rights":   r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Artisinal_Mining_Rights.geojson",
        "Bidding Areas":             r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Bidding_Areas.geojson",
        "Emerald Restricted Areas":  r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Emerald_Restricted_Areas.geojson",
        "Large Scale Exploration Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Large_Scale_Exploration_Licences.geojson",
        "Large Scale Gemstone Licences":    r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Large_Scale_Gemstone_Licences.geojson",
        "Large Scale Mining Licences":      r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Large_Scale_Mining_Licences.geojson",
        "Mineral Processing Licences":      r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Mineral_Processing_licences.geojson",
        "Petroleum Licences":               r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\petroleum_licences.geojson",
        "Prospecting Licences 2008":        r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Propecting_Licences_2008.geojson",
        "Prospecting Permits 2008":         r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Prospecting_Permits_2008.geojson",
        "Restricted Areas 1":               r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\restricted_areas_layer_1.geojson",
        "Restricted Areas 2":               r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\restricted_areas_layer_2.geojson",
        "Small Scale Gemstone Licences":    r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Small_Scale_Gemstone_licences.geojson",
        "Small Scale Mining Licences":      r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Small_Scale_Mining_Licences.geojson",
    },
      "⬛ DRC Mining Data (Source: CGS DRC) ▼": {
        "DRC Artisinal Mining Sites": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\artisanal_sites.geojson",
        "DRC Mining Permits": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\Democratic_Republic_of_the_Congo_mining_permits.geojson",
        "DRC Processing Entities": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\processing_entities.geojson",
        "DRC Industrial Projects": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\industrial_projects.geojson",
    },
    "⬛ Electricity Infrastructure (Source: OSM) ▼": {
        "Power Plants": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Electrical Infrastrcture Zambia\Power Plants Zambia.geojson",
        "Power Lines":  r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Electrical Infrastrcture Zambia\Power Lines Zambia.geojson",
        "Substations":  r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Electrical Infrastrcture Zambia\Substations Zambia.geojson",
    },
    "⬛ Transport Infrastructure (Source: OSM) ▼": {
#        "Railways Southern Africa":    r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Railways Zambia and Southern Africa\Rail_Compressed.geojson",
        "Ports of Entry and Border Crossings": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Ports of Entry Zambia\Zambia Border Crossings and Airports.geojson",
        "Ports Southern Africa": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\Export Ports.geojson",
        "Export Corridors": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\Corridors.geojson",
 #       "Major Roads Southern Africa": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Southern Africa Road Network\Road_Compressed.geojson",
    },
    "⬛ Heath Data (Source: OSM) ▼": {
        "Health Facilities Zambia": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Health Facility Catchment Areas\Health Facilties Zambia.geojson",
    },
#        "⬛ Zambian Districts and Health Zata (Source: National Energy Access Survey) ▼" : {"National Energy Access Survey by Distric
}

# 4) Custom Legend
legend_html = '''
<div id="legend-container" style="position: fixed; top: 90px; left: 10px; z-index: 9999;">
    <button id="legend-toggle" style="
        background-color: #007bff;
        color: white;
        padding: 6px 12px;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        margin-bottom: 8px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    ">Toggle Legend</button>
    <div id="legend" style="
        max-height: 75vh;
        overflow-y: auto;
        background: white;
        padding: 8px;
        border: 1px solid grey;
        border-radius: 4px;
        font-size: 12px;
        box-shadow: 4px 4px 12px rgba(0,0,0,0.3);
    ">
        <b>Legend</b><br>
'''
for grp, layers in layer_groups.items():
    legend_html += f"<b>{grp}</b><br>"
    for lname in layers.keys():
        color = layer_styles.get(lname, "#000000")
        legend_html += f"<span style='color:{color};'>■</span> {lname}<br>"
legend_html += "</div></div>"

legend_html += '''
<script>
document.getElementById('legend-toggle').addEventListener('click', function() {
    const legend = document.getElementById('legend');
    legend.style.display = (legend.style.display === 'none') ? 'block' : 'none';
});
</script>
'''
m.get_root().html.add_child(folium.Element(legend_html))
print("📌 Collapsible custom legend added.")

# Southern‐Africa bbox for clipping
south_bounds = (11.5, -35.0, 41.0, 5.0)
south_poly   = box(*south_bounds)

# =================================================================================
#  Marker symbol configuration:
#  type="awesome" uses FontAwesome (fa) icons, type="circle" uses CircleMarker.
point_symbol_map = {
    "Processing Sites": {
        "type": "awesome",
        "icon": "cog",
        "prefix": "fa",
        "marker_color": "brown"
    },
    "Quarries": {
        "type": "awesome",
        "icon": "industry",
        "prefix": "fa",
        "marker_color": "purple"
    },
    # add more or change to "circle" type if desired
}
# =================================================================================

# 5) Build groups & subgroups
# 5) Build groups & sub
# 5) Build groups & subgroups (scrollable popups and empty field removal)
# 5) Build groups & subgroups (scrollable popups and empty field removal with timestamp fix)
# 5) Build groups & subgroups (fixed indentation and NaT handling)
for group_label, layers in layer_groups.items():
    default_on = group_label.startswith("X")
    print(f"\n📂 Creating group: {group_label} (default {'on' if default_on else 'off'})")
    
    # Create the main group
    parent = folium.FeatureGroup(name=group_label, show=default_on)
    parent.add_to(m)

    for layer_name, path in layers.items():
        print(f"  🔍 Layer: {layer_name}")
        
        # Check if the file exists
        if not os.path.exists(path):
            print(f"    ⚠️ File not found: {path}")
            continue
        
        # Read and clean GeoJSON
        size_mb = os.path.getsize(path) / 1e6
        print(f"    • Reading from: {path} ({size_mb:.1f} MB)")
        gdf = gpd.read_file(path)
        gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty]
        print(f"    ✅ Read {len(gdf)} valid geometries")
        
        # Clip if transport data, but preserve all columns
        if group_label.startswith("⬛"):
            gdf = gpd.clip(gdf, south_poly)
            gdf["geometry"] = gdf.geometry.simplify(0.05, preserve_topology=True)
            print(f"    ✂️ Clipped to region, {len(gdf)} features remaining")

        # Create subgroup
        display_name = f"■ {layer_name}"
        subgroup = FeatureGroupSubGroup(parent, display_name, show=default_on)
        subgroup.add_to(m)

        # Process each feature
        for _, row in gdf.iterrows():
            # Extract properties, handling NaT, Timestamp, and empty fields
            props = {
                k: (str(v) if isinstance(v, (pd.Timestamp, pd._libs.tslibs.nattype.NaTType)) else v)
                for k, v in row.drop("geometry").items()
                if pd.notna(v) and v not in (None, "", "null", "None")
            }

            # Create popup content with scrolling
            if props:
                html = """
                <div style="font-family: Arial, sans-serif; font-size: 12px; max-height: 300px; overflow-y: auto;">
                    <table style="width: 100%; border-collapse: collapse;">
                """ + "".join(
                    f"<tr><th style='text-align: left; padding: 4px; background-color: #f2f2f2;'>{k}</th><td style='padding: 4px;'>{v}</td></tr>"
                    for k, v in props.items()
                ) + "</table></div>"
                popup = folium.Popup(html, max_width=300)
            else:
                popup = folium.Popup("<b>No data available</b>", max_width=300)

            # Handle different geometry types
            if row.geometry.geom_type in ["Point", "MultiPoint"]:
                lat, lon = row.geometry.y, row.geometry.x
                sym = point_symbol_map.get(layer_name, {})

                if sym.get("type") == "awesome":
                    icon = folium.Icon(
                        icon=sym.get("icon", "info-sign"),
                        prefix=sym.get("prefix", "fa"),
                        color=sym.get("marker_color", "blue")
                    )
                    marker = folium.Marker((lat, lon), icon=icon)
                elif sym.get("type") == "circle":
                    marker = folium.CircleMarker(
                        (lat, lon),
                        radius=sym.get("radius", 6),
                        color=layer_styles.get(layer_name, "#000000"),
                        fill=True,
                        fill_opacity=sym.get("fill_opacity", 0.7)
                    )
                else:
                    # Fallback circle marker
                    marker = folium.CircleMarker(
                        (lat, lon),
                        radius=6,
                        color=layer_styles.get(layer_name, "#000000"),
                        fill=True,
                        fill_opacity=0.7
                    )
                
                # Attach the popup to the marker
                marker.add_child(popup)
                marker.add_to(subgroup)

            # Handle all other geometries (Polygon, LineString, etc.)
            else:
                # Ensure all properties are JSON-serializable
                feat = {
                    "type": "Feature",
                    "geometry": row.geometry.__geo_interface__,
                    "properties": props
                }
                gj = folium.GeoJson(
                    feat,
                    style_function=lambda f, color=layer_styles.get(layer_name, "#000000"): {
                        "color": color,
                        "weight": 1.5,
                        "fillOpacity": 0.6
                    }
                )
                # Attach the popup
                gj.add_child(popup)
                gj.add_to(subgroup)
        
        print(f"    ✅ Added {len(gdf)} features for {layer_name}")

# 6) Layer control (expanded, left) - only add once
if not any(isinstance(c, folium.LayerControl) for c in m._children.values()):
    folium.LayerControl(collapsed=False, position="topright").add_to(m)
print("🧭 Layer control added.")


# 8) Fit bounds & save
m.fit_bounds([[south_bounds[1],south_bounds[0]],[south_bounds[3],south_bounds[2]]])
out_path = r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\Mining and Energy Webmap\zambia_infra_map_grouped_v11_with_dashboard_public.html"
m.save(out_path)
print(f"✅ Map saved: {out_path}")


# In[9]:


#Latest webmap version 
#This is the public dissementation version 

#second more experimentlal web map

import folium
import geopandas as gpd
import os
from shapely.geometry import box
from folium.plugins import FeatureGroupSubGroup
import pandas as pd




print("📍 Starting grouped, slimmed Southern Africa map…")

# 1) Base map _without_ adding the default OSM into the control
m = folium.Map(
    location=[-13.5, 27.8],
    zoom_start=6,
    control=False     # disable the default base layer in the layer control
)
print("✅ Base map created.")

# 1b) Now add OSM back, but with our custom name
folium.TileLayer(
    tiles="OpenStreetMap",
    name="Layer Control",  # this will appear as the only radio in the "base layers" section
    control=False
).add_to(m)

print("Adding title")

# 2) Title and Dashboard Button
header_html = '''
<div style="
    position: fixed; top: 10px; left: 50%;
    transform: translateX(-50%);
    z-index:9999;
    background-color: white;
    padding: 6px 12px;
    border: 2px solid grey;
    border-radius: 4px;
    font-size: 20px;
    font-weight: bold;
    display: flex;
    align-items: center;
">
    ZEL Mining and Infrastructure Map
    <button id="dashboard-toggle" style="
        margin-left: 20px;
        background-color: #007bff;
        color: white;
        padding: 6px 12px;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        font-size: 14px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    ">Show Dashboard</button>
</div>
'''
m.get_root().html.add_child(folium.Element(header_html))
print("✏️ Map title and dashboard button added.")

# 3) Collapsible Dashboard Panel
panel_html = '''
<div id="dashboard-panel" class="dashboard-panel collapsed">
    <iframe id="dashboard-iframe" width="100%" height="100%" src="https://lookerstudio.google.com/embed/reporting/090745d0-4b31-4f50-b3df-b7e5751036d7/page/cpZJF" frameborder="0" allowfullscreen></iframe>
</div>

<style>
.dashboard-panel {
    position: fixed;
    top: 80px;
    right: 5%;
    width: 90%;
    height: 80vh;
    background-color: white;
    padding: 8px;
    border: 1px solid grey;
    border-radius: 4px;
    z-index: 9999;
    transition: top 0.3s ease;
    box-shadow: 4px 4px 12px rgba(0,0,0,0.3);
}

@media (min-width: 600px) {
    .dashboard-panel {
        right: 390px;
        width: 800px;
        height: 600px;
    }
}

.dashboard-panel.collapsed {
    top: -10050px;
}
</style>

<script>
document.getElementById('dashboard-toggle').addEventListener('click', function() {
    const panel = document.getElementById('dashboard-panel');
    this.textContent = panel.classList.toggle('collapsed') ? 'Show Dashboard' : 'Hide Dashboard';
});
</script>
'''
m.get_root().html.add_child(folium.Element(panel_html))
print("📊 Responsive collapsible dashboard added.")


# 4) Styles & file paths
layer_styles = {
    # Mining & Quarries
    "Processing Sites": "#a65628",
    "Quarries": "#e377c2",
    "Mines": "#ff9896",
    "Amethyst Restricted Areas": "#d62728",
    "Artisinal Mining Rights": "#ff7f0e",
    "Bidding Areas": "#bcbd22",
    "Emerald Restricted Areas": "#17becf",
    "Large Scale Exploration Licences": "#aec7e8",
    "Large Scale Gemstone Licences": "#c5b0d5",
    "Large Scale Mining Licences": "#9467bd",
    "Mineral Processing Licences": "#8c564b",
    "Petroleum Licences": "#1f77b4",
    "Prospecting Licences 2008": "#98df8a",
    "Prospecting Permits 2008": "#c49c94",
    "Restricted Areas 1": "#7f7f7f",
    "Restricted Areas 2": "#dbdb8d",
    "Small Scale Gemstone Licences": "#ffbb78",
    "Small Scale Mining Licences": "#2ca02c",
    # DRC Mining and Quarries 
    "DRC Mining Permits": "#91318B",
    "DRC Artisinal Mining Sites": "#c49c94",
    "DRC Processing Entities": "#40029C",
    "DRC Industial Projects": "#21129C",
    # Botswana Mining Data
    "Mining Licence - Active": "#91318B",
    "Minerals Permit - Active": "#32318B",
    "Minerals Permit - Active": "#41618B",
    "Development Licence - Active": "#8B0000",  # Dark Red
    "Retention Licence - Active": "#006400",  # Dark Green
    "Energy Prospecting Licence - Active": "#4682B4",  # Steel Blue
    "Metals Prospecting Licence - Active": "#FF8C00",  # Dark Orange
    "Industrial Minerals Prospecting Licence - Active": "#9400D3",  # Dark Violet
    "Precious Stones Prospecting Licence - Active": "#DA70D6",  # Orchid
    "Semi Precious Stones Prospecting Licence - Active": "#20B2AA",  # Light Sea Green
    "Exploration Licences - Active": "#4169E1",  # Royal Blue
    
    #"🟨 Namibia Mining Data (Source: Namibia Mining Cadastre) ▼": {
    "Environmentally Sensitive Areas (Admin Layer)": "#A9A9A9",  # Dark Gray
    "Active Mining Claims": "#FF8C00",  # Dark Orange
    "Active Mineral Deposit Retention Licences": "#8B0000",  # Dark Red
    "Active Exclusive Prospecting Licences": "#4169E1",  # Royal Blue
    "Active Reconnaissance Licences": "#4682B4",  # Steel Blue
    "Active Exclusive Reconnaissance Licences": "#6A5ACD",  # Slate Blue

    "Application - Mining Claims": "#FFA07A",  # Light Salmon
    "Application - Mineral Deposit Retention": "#CD5C5C",  # Indian Red
    "Application - Exclusive Prospecting Licences": "#87CEFA",  # Light Sky Blue

    # "Application - Reconnaissance Licences": "#5F9EA0",  # Cadet Blue
    # "Application - Exclusive Reconnaissance Licences": "#9370DB",  # Medium Purple

    "Application - Production Licences (Petroleum)": "#DAA520",  # Goldenrod
    "Application - Petroleum Exploration Licences": "#B8860B",  # Dark Goldenrod

    # "Application - Reconnaissance Licences (Petroleum)": "#BC8F8F",  # Rosy Brown

    "Active - Production Licences (Petroleum)": "#556B2F",  # Dark Olive Green
    "Active - Petroleum Exploration Licences": "#228B22",  # Forest Green

    # "Active - Reconnaissance Licences (Petroleum)": "#2E8B57",  # Sea Green
    
    # Electricity Infrastructure
    "Power Plants": "#17becf",
    "Power Lines": "#9467bd",
    "Substations": "#bcbd22",
    # Transport Infrastructure
    "Railways Southern Africa": "#8B0000",
    "Major Roads Southern Africa": "#00008B",
    "Export Corridors": "#6B0000",
    "Ports Southern Africa": "#00009A",
    "Ports of Entry and Border Crossings": "#29d6ae",
    #Health
    "Health Facilities Zambia": "#69d4ae"
}

layer_groups = {
    "⬛ Mining & Quarries - Mines and Processing Sites (Source: OSM) ▼": {
        "Processing Sites": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Zambian Mines\Processing SItes.geojson",
        "Quarries":        r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Quarries In Zambia\Quarries.geojson",
        "Mines":           r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Zambian Mines\Location of Mines Zambia.geojson",
    },
        "⬛ Mining & Quarries - Licence Areas (Source: ZMB Mining Cadastre) ▼": {
        "Amethyst Restricted Areas": r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Amethyst_Resticted_Areas.geojson",
        "Artisinal Mining Rights":   r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Artisinal_Mining_Rights.geojson",
        "Bidding Areas":             r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Bidding_Areas.geojson",
        "Emerald Restricted Areas":  r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Emerald_Restricted_Areas.geojson",
        "Large Scale Exploration Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Large_Scale_Exploration_Licences.geojson",
        "Large Scale Gemstone Licences":    r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Large_Scale_Gemstone_Licences.geojson",
        "Large Scale Mining Licences":      r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Large_Scale_Mining_Licences.geojson",
        "Mineral Processing Licences":      r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Mineral_Processing_licences.geojson",
        "Petroleum Licences":               r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\petroleum_licences.geojson",
        "Prospecting Licences 2008":        r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Propecting_Licences_2008.geojson",
        "Prospecting Permits 2008":         r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Prospecting_Permits_2008.geojson",
        "Restricted Areas 1":               r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\restricted_areas_layer_1.geojson",
        "Restricted Areas 2":               r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\restricted_areas_layer_2.geojson",
        "Small Scale Gemstone Licences":    r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Small_Scale_Gemstone_licences.geojson",
        "Small Scale Mining Licences":      r"C:\Users\EDISON\IGC Teams Dropbox\Toby Edison\GIS Data\Other GIS Data Sources\Zambia Mining Cadastre\Small_Scale_Mining_Licences.geojson",
    },
      "⬛ DRC Mining Data (Source: CGS DRC) ▼": {
        "DRC Artisinal Mining Sites": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\artisanal_sites.geojson",
        "DRC Mining Permits": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\Democratic_Republic_of_the_Congo_mining_permits.geojson",
        "DRC Processing Entities": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\processing_entities.geojson",
        "DRC Industrial Projects": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\industrial_projects.geojson",
    },

    #More can be added here like non active licences
    "⬛ Botswana Mining Data (Source: Botswana Mining Cadastre) ▼": {
        "Mining Licence - Active": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Botswana Mining Cadastre\botswana_mining_named\02_Active_ML.geojson",
        "Minerals Permit - Active": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Botswana Mining Cadastre\botswana_mining_named\06_Active_MP.geojson",
        "Development Licence - Active": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Botswana Mining Cadastre\botswana_mining_named\10_Active_DL.geojson",
        "Retention Licence - Active": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Botswana Mining Cadastre\botswana_mining_named\14_Active_RL.geojson",
        "Energy Prospecting Licence - Active": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Botswana Mining Cadastre\botswana_mining_named\19_Active_PL__Energy.geojson",
        "Metals Prospecting Licence - Active": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Botswana Mining Cadastre\botswana_mining_named\23_Active_PL__Metals.geojson",
        "Industrial Minerals Prospecting Licence - Active": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Botswana Mining Cadastre\botswana_mining_named\27_Active_PL__Industrial.geojson",
        "Precious Stones Prospecting Licence - Active": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Botswana Mining Cadastre\botswana_mining_named\31_Active_PL__Precious.geojson",
        "Semi Precious Stones Prospecting Licence - Active": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Botswana Mining Cadastre\botswana_mining_named\35_Active_PL__SemiPrecious.geojson",
        "Exploration Licences - Active": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Botswana Mining Cadastre\botswana_mining_named\64_Active_EL.geojson",
    },
    "⬛ Namibia Mining Data (Source: Namibia Mining Cadastre) ▼": {
      # "Withdrawn Areas (Admin Layer)": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Namibia Mining Cadastre\AdminLayer_0_Withdrawn_Areas.geojson",
        "Environmentally Sensitive Areas (Admin Layer)": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\AdminLayer_1_Environmentally_Sensitive_Areas.geojson",
        "Active Mining Claims": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Mining_Licences_-_Active_1_Mining_Claims.geojson",
        "Active Mineral Deposit Retention Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Mining_Licences_-_Active_2_Mineral_Deposit_Retention_Licences.geojson",
        "Active Exclusive Prospecting Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Mining_Licences_-_Active_3_Exclusive_Prospecting_Licences.geojson",
        "Active Reconnaissance Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Mining_Licences_-_Active_4_Reconnaissance_Licences.geojson",
        "Active Exclusive Reconnaissance Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Mining_Licences_-_Active_5_Exclusive_Reconnaissance_Licences.geojson",
        "Application - Mining Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Mining_Licences_-_Applications_0_Mining_Licences.geojson",
        "Application - Mining Claims": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Mining_Licences_-_Applications_1_Mining_Claims.geojson",
        "Application - Mineral Deposit Retention": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Mining_Licences_-_Applications_2_Mineral_Deposit_Retention_Licences.geojson",
        "Application - Exclusive Prospecting Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Mining_Licences_-_Applications_3_Exclusive_Prospecting_Licences.geojson",
 #       "Application - Reconnaissance Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Namibia Mining Cadastre\Mining_Licences_-_Applications_4_Reconnaissance_Licences.geojson",
 #       "Application - Exclusive Reconnaissance Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Namibia Mining Cadastre\Mining_Licences_-_Applications_5_Exclusive_Reconnaissance_Licences.geojson",
        "Application - Production Licences (Petroleum)": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Petroleum_Layers_-_Applications_0_Production_Licences.geojson",
        "Application - Petroleum Exploration Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Petroleum_Layers_-_Applications_1_Petroleum_Exploration_Licences.geojson",
  #      "Application - Reconnaissance Licences (Petroleum)": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Namibia Mining Cadastre\Petroleum_Layers_-_Applications_2_Reconnaissance_Licences.geojson",
        "Active - Production Licences (Petroleum)": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Petroleum_Licences_-_Active_0_Production_Licences.geojson",
        "Active - Petroleum Exploration Licences": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Nambia Mining Cadastre\Petroleum_Licences_-_Active_1_Petroleum_Exploration_Licences.geojson",
#       "Active - Reconnaissance Licences (Petroleum)": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Namibia Mining Cadastre\Petroleum_Licences_-_Active_2_Reconnaissance_Licences.geojson",
    },
        
    "⬛ Electricity Infrastructure (Source: OSM) ▼": {
        "Power Plants": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Electrical Infrastrcture Zambia\Power Plants Zambia.geojson",
        "Power Lines":  r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Electrical Infrastrcture Zambia\Power Lines Zambia.geojson",
        "Substations":  r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Electrical Infrastrcture Zambia\Substations Zambia.geojson",
    },
    "⬛ Transport Infrastructure (Source: OSM) ▼": {
#        "Railways Southern Africa":    r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Railways Zambia and Southern Africa\Rail_Compressed.geojson",
        "Ports of Entry and Border Crossings": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Ports of Entry Zambia\Zambia Border Crossings and Airports.geojson",
        "Ports Southern Africa": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\Export Ports.geojson",
        "Export Corridors": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\CGS Data DRC\Corridors.geojson",
 #       "Major Roads Southern Africa": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Southern Africa Road Network\Road_Compressed.geojson",
    },
    "⬛ Heath Data (Source: OSM) ▼": {
        "Health Facilities Zambia": r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\GIS Data\Other GIS Data Sources\Health Facility Catchment Areas\Health Facilties Zambia.geojson",
    },
#        "⬛ Zambian Districts and Health Zata (Source: National Energy Access Survey) ▼" : {"National Energy Access Survey by Distric
      
}

# 4) Custom Legend
legend_html = '''
<div id="legend-container" style="
    position: fixed;
    top: 90px;
    left: 10px;
    z-index: 9999;
    max-width: 90vw;
    width: 300px;
    font-size: 12px;
">
    <button id="legend-toggle" style="
        background-color: #007bff;
        color: white;
        padding: 6px 12px;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        margin-bottom: 8px;
        width: 100%;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    ">Toggle Legend</button>
    <div id="legend" style="
        max-height: 70vh;
        overflow-y: auto;
        background: white;
        padding: 8px;
        border: 1px solid grey;
        border-radius: 4px;
        box-shadow: 4px 4px 12px rgba(0,0,0,0.3);
    ">
        <b>Legend</b><br>
'''
for grp, layers in layer_groups.items():
    legend_html += f"<b>{grp}</b><br>"
    for lname in layers.keys():
        color = layer_styles.get(lname, "#000000")
        legend_html += f"<span style='color:{color};'>■</span> {lname}<br>"
legend_html += "</div></div>"

legend_html += '''
<script>
document.getElementById('legend-toggle').addEventListener('click', function() {
    const legend = document.getElementById('legend');
    legend.style.display = (legend.style.display === 'none') ? 'block' : 'none';
});
</script>
'''
m.get_root().html.add_child(folium.Element(legend_html))
print("📌 Collapsible custom legend added.")

# Southern‐Africa bbox for clipping
south_bounds = (11.5, -35.0, 41.0, 5.0)
south_poly   = box(*south_bounds)

# =================================================================================
#  Marker symbol configuration:
#  type="awesome" uses FontAwesome (fa) icons, type="circle" uses CircleMarker.
point_symbol_map = {
    "Processing Sites": {
        "type": "awesome",
        "icon": "cog",
        "prefix": "fa",
        "marker_color": "brown"
    },
    "Quarries": {
        "type": "awesome",
        "icon": "industry",
        "prefix": "fa",
        "marker_color": "purple"
    },
    # add more or change to "circle" type if desired
}
# =================================================================================

# 5) Build groups & subgroups
# 5) Build groups & sub
# 5) Build groups & subgroups (scrollable popups and empty field removal)
# 5) Build groups & subgroups (scrollable popups and empty field removal with timestamp fix)
# 5) Build groups & subgroups (fixed indentation and NaT handling)
for group_label, layers in layer_groups.items():
    default_on = group_label.startswith("X")
    print(f"\n📂 Creating group: {group_label} (default {'on' if default_on else 'off'})")
    
    # Create the main group
    parent = folium.FeatureGroup(name=group_label, show=default_on)
    parent.add_to(m)

    for layer_name, path in layers.items():
        print(f"  🔍 Layer: {layer_name}")
        
        # Check if the file exists
        if not os.path.exists(path):
            print(f"    ⚠️ File not found: {path}")
            continue
        
        # Read and clean GeoJSON
        size_mb = os.path.getsize(path) / 1e6
        print(f"    • Reading from: {path} ({size_mb:.1f} MB)")
        gdf = gpd.read_file(path)
        gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty]
        print(f"    ✅ Read {len(gdf)} valid geometries")
        
        # Clip if transport data, but preserve all columns
        if group_label.startswith("⬛"):
            gdf = gpd.clip(gdf, south_poly)
            gdf["geometry"] = gdf.geometry.simplify(0.05, preserve_topology=True)
            print(f"    ✂️ Clipped to region, {len(gdf)} features remaining")

        # Create subgroup
        display_name = f"■ {layer_name}"
        subgroup = FeatureGroupSubGroup(parent, display_name, show=default_on)
        subgroup.add_to(m)

        # Process each feature
        for _, row in gdf.iterrows():
            # Extract properties, handling NaT, Timestamp, and empty fields
            props = {
                k: (str(v) if isinstance(v, (pd.Timestamp, pd._libs.tslibs.nattype.NaTType)) else v)
                for k, v in row.drop("geometry").items()
                if pd.notna(v) and v not in (None, "", "null", "None")
            }

            # Create popup content with scrolling
            if props:
                html = """
                <div style="font-family: Arial, sans-serif; font-size: 12px; max-height: 300px; overflow-y: auto;">
                    <table style="width: 100%; border-collapse: collapse;">
                """ + "".join(
                    f"<tr><th style='text-align: left; padding: 4px; background-color: #f2f2f2;'>{k}</th><td style='padding: 4px;'>{v}</td></tr>"
                    for k, v in props.items()
                ) + "</table></div>"
                popup = folium.Popup(html, max_width=300)
            else:
                popup = folium.Popup("<b>No data available</b>", max_width=300)

            # Handle different geometry types
            if row.geometry.geom_type in ["Point", "MultiPoint"]:
                lat, lon = row.geometry.y, row.geometry.x
                sym = point_symbol_map.get(layer_name, {})

                if sym.get("type") == "awesome":
                    icon = folium.Icon(
                        icon=sym.get("icon", "info-sign"),
                        prefix=sym.get("prefix", "fa"),
                        color=sym.get("marker_color", "blue")
                    )
                    marker = folium.Marker((lat, lon), icon=icon)
                elif sym.get("type") == "circle":
                    marker = folium.CircleMarker(
                        (lat, lon),
                        radius=sym.get("radius", 6),
                        color=layer_styles.get(layer_name, "#000000"),
                        fill=True,
                        fill_opacity=sym.get("fill_opacity", 0.7)
                    )
                else:
                    # Fallback circle marker
                    marker = folium.CircleMarker(
                        (lat, lon),
                        radius=6,
                        color=layer_styles.get(layer_name, "#000000"),
                        fill=True,
                        fill_opacity=0.7
                    )
                
                # Attach the popup to the marker
                marker.add_child(popup)
                marker.add_to(subgroup)

            # Handle all other geometries (Polygon, LineString, etc.)
            else:
                # Ensure all properties are JSON-serializable
                feat = {
                    "type": "Feature",
                    "geometry": row.geometry.__geo_interface__,
                    "properties": props
                }
                gj = folium.GeoJson(
                    feat,
                    style_function=lambda f, color=layer_styles.get(layer_name, "#000000"): {
                        "color": color,
                        "weight": 1.5,
                        "fillOpacity": 0.6
                    }
                )
                # Attach the popup
                gj.add_child(popup)
                gj.add_to(subgroup)
        
        print(f"    ✅ Added {len(gdf)} features for {layer_name}")


# 6) Layer control (expanded, left) - only add once
if not any(isinstance(c, folium.LayerControl) for c in m._children.values()):
    folium.LayerControl(collapsed=False, position="topright").add_to(m)
print("🧭 Layer control added.")

# 7) Add responsive script for layer control resizing
layer_control_script = '''
<script>
document.addEventListener("DOMContentLoaded", function() {
    const layerControl = document.querySelectorAll(".leaflet-control-layers")[0];
    if (layerControl) {
        layerControl.style.maxHeight = "75vh";
        layerControl.style.maxWidth = "300px";
        layerControl.style.overflowY = "auto";
        layerControl.style.overflowX = "auto";
    }
});
</script>
'''
m.get_root().html.add_child(folium.Element(layer_control_script))
print("🎯 Responsive layer control styling injected.")


# 8) Fit bounds & save
m.fit_bounds([[south_bounds[1],south_bounds[0]],[south_bounds[3],south_bounds[2]]])
out_path = r"C:\Users\EDISON\IGC Teams Dropbox\Zambia Team\Zambia Evidence Lab (ZEL)\Mining and Energy Webmap\zambia_infra_map_grouped_v14_with_dashboard_public.html"
m.save(out_path)
print(f"✅ Map saved: {out_path}")


# In[ ]:




