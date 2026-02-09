import pandas as pd
import plotly.express as px
import json
import urllib.request

# 1. Chargement et nettoyage (identique au précédent)
df = pd.read_csv('VinGouv_2009_clean.csv')
df = df[df['Departements'] != 'TOTAUX']

def clean_dept_code(name):
    code = name.split(' ')[0]
    code = code.replace('O', '0')
    return code.zfill(2)

df['code'] = df['Departements'].apply(clean_dept_code)

# 2. Récupération du fond de carte
geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"
with urllib.request.urlopen(geojson_url) as url:
    geojson_data = json.loads(url.read().decode())

# 3. Création de la carte avec formatage spécifique
fig = px.choropleth(
    df,
    geojson=geojson_data,
    locations='code',
    featureidkey="properties.code",
    color='total_prod',
    color_continuous_scale="Viridis",
    range_color=(0, df['total_prod'].quantile(0.95)),
    scope="europe",
    # On définit ici le format du survol (hover)
    hover_name='Departements',
    hover_data={'code': False, 'total_prod': ':,.0f'}, # ':,.0f' = nombre entier avec séparateur
    labels={'total_prod': 'Production (hl)'},
    title='Production de Vin par Département en 2009'
)

# 4. Forcer l'affichage des nombres entiers sur la barre de couleur
fig.update_layout(coloraxis_colorbar=dict(
    title="Hectolitres",
    tickformat=".0f" # Force l'affichage sans le 'k'
))

fig.update_geos(fitbounds="locations", visible=False)

# 5. Sauvegarde
fig.write_html("carte_production_2009.html")
print("Carte mise à jour générée sans les 'k'.")
fig.show()