docker-compose up -d

docker exec -it postgis \
  psql -U gis -d geodb \
  -c "CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS postgis_topology;"


python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 data_collection/bike_api.py
python3 data_collection/download_shapes.py

python3 data_collection/ingest_postgis.py




