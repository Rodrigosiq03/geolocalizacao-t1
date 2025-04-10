import os, json
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def get_engine():
    for host in ("db", "localhost"):
        url = f"postgresql://gis:gis@{host}:5432/geodb"
        try:
            eng = create_engine(url)
            with eng.connect():
                print(f"✅ Conectado ao PostGIS em host '{host}'")
            return eng
        except OperationalError:
            print(f"⚠️ Falha ao conectar em '{host}', tentando próximo...")
    raise RuntimeError("❌ Não foi possível conectar ao PostGIS.")

engine = get_engine()

shp_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'shapes')
shps = [f for f in os.listdir(shp_dir) if f.lower().endswith('.shp')]
if not shps:
    raise FileNotFoundError(f"Não achei .shp em {shp_dir}. Rode download_shapes.py primeiro.")
shp_path = os.path.join(shp_dir, shps[0])
print("ℹ️ Usando shapefile:", shp_path)

gdf_all = gpd.read_file(shp_path)
if 'CD_MUN' in gdf_all.columns:
    gdf_lim = gdf_all[gdf_all['CD_MUN'] == '3550308']
else:
    gdf_lim = gdf_all[gdf_all['CD_GEOCMU'] == '3550308']
gdf_lim = gdf_lim.to_crs("EPSG:4326")
gdf_lim.to_postgis('limites_municipais', engine, if_exists='replace', index=False)
print("✔️ limites_municipais (SP) importado")

info_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'bike', 'station_information.json')
with open(info_path, 'r', encoding='utf-8') as f:
    info = json.load(f).get('data', {}).get('stations', [])
gdf_info = gpd.GeoDataFrame(
    info,
    geometry=gpd.points_from_xy(
        [s['lon'] for s in info],
        [s['lat'] for s in info]
    ),
    crs='EPSG:4326'
)
gdf_info.to_postgis('bike_station_info', engine, if_exists='replace', index=False)
print("✔️ bike_station_info importado")

status_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'bike', 'station_status.json')
with open(status_path, 'r', encoding='utf-8') as f:
    status = json.load(f).get('data', {}).get('stations', [])

df_status = pd.DataFrame(status)
drop_cols = ['vehicle_types_available', 'vehicle_docks_available']
for c in drop_cols:
    if c in df_status.columns:
        df_status = df_status.drop(columns=c)

df_status.to_sql('bike_station_status', engine, if_exists='replace', index=False)
print("✔️ bike_station_status importado")
