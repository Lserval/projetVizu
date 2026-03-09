import pandas as pd
import plotly.express as px
import json
import urllib.request
import os

# 1. Chargement des données regroupées
os.chdir(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv('production_vins_2009_2018_v2.csv')

# 2. Récupération du GeoJSON
geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"
with urllib.request.urlopen(geojson_url) as url:
    geojson_data = json.loads(url.read().decode())

# 3. Création de la carte animée
fig = px.choropleth(
    df.sort_values('Year'), # Trier par année pour l'animation
    geojson=geojson_data,
    locations='Dept_Code',
    featureidkey="properties.code",
    color='total_prod',
    animation_frame='Year', # C'est ici que l'évolution se passe
    color_continuous_scale="Viridis",
    range_color=(0, 1000000), # Fixer l'échelle pour éviter qu'elle ne bouge
    scope="europe",
    hover_name='Departements',
    title='Évolution de la production viticole par département (2009-2018)',
    labels={'total_prod': 'Production (hl)', 'Year': 'Année'}
)

fig.update_geos(fitbounds="locations", visible=False)
fig.write_html("carte_animée_2009_2018.html")
fig.show()