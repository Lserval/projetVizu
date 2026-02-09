import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import urllib.request
import os

# 1. Chargement et préparation des données
os.chdir(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv('VinGouv_2009_clean.csv')
df = df[df['Departements'] != 'TOTAUX']

# Remplissage des valeurs manquantes par 0 pour éviter les trous sur la carte
df['tot_blanc'] = df['tot_blanc'].fillna(0)
df['tot_rougerose'] = df['tot_rougerose'].fillna(0)

def clean_dept_code(name):
    code = name.split(' ')[0].replace('O', '0')
    return code.zfill(2)

df['code'] = df['Departements'].apply(clean_dept_code)

# 2. Récupération du GeoJSON
geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"
with urllib.request.urlopen(geojson_url) as url:
    geojson_data = json.loads(url.read().decode())

# 3. Création de la figure avec Plotly Graph Objects pour plus de contrôle
fig = go.Figure()

# Trace pour le Vin Blanc
fig.add_trace(go.Choropleth(
    geojson=geojson_data,
    locations=df['code'],
    z=df['tot_blanc'],
    featureidkey="properties.code",
    colorscale="Purp", # Teintes violettes/claires pour le blanc
    name="Vin Blanc",
    text=df['Departements'],
    hovertemplate="<b>%{text}</b><br>Production Blanc: %{z:,.0f} hl<extra></extra>",
    colorbar_title="Hectolitres",
    visible=True # Visible par défaut
))

# Trace pour le Vin Rouge/Rosé
fig.add_trace(go.Choropleth(
    geojson=geojson_data,
    locations=df['code'],
    z=df['tot_rougerose'],
    featureidkey="properties.code",
    colorscale="Reds", # Teintes rouges pour le rouge/rosé
    name="Vin Rouge & Rosé",
    text=df['Departements'],
    hovertemplate="<b>%{text}</b><br>Production Rouge/Rosé: %{z:,.0f} hl<extra></extra>",
    colorbar_title="Hectolitres",
    visible=False # Caché par défaut
))

# 4. Ajout des boutons de sélection
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.5,
            y=1.1,
            buttons=list([
                dict(label="Production Blanc",
                     method="update",
                     args=[{"visible": [True, False]},
                           {"title": "Production de Vin Blanc par Département (2009)"}]),
                dict(label="Production Rouge & Rosé",
                     method="update",
                     args=[{"visible": [False, True]},
                           {"title": "Production de Vin Rouge & Rosé par Département (2009)"}]),
            ]),
        )
    ]
)

# Ajustements cosmétiques
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title_text='Production de Vin par Département (2009)',
    margin={"r":0,"t":50,"l":0,"b":0}
)

# 5. Sauvegarde
fig.write_html("carte_comparative_vins.html")
print("Fichier 'carte_comparative_vins.html' généré.")
fig.show()