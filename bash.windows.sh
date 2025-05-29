docker-compose up -d

docker exec -it postgis \
  psql -U gis -d geodb \
  -c "CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS postgis_topology;"


python -m venv venv
if [ -f "./venv/Scripts/activate" ]; then
  source ./venv/Scripts/activate
elif [ -f "./venv/bin/activate" ]; then
  source ./venv/bin/activate
else
  echo "❌ Não foi possível encontrar o script de ativação do ambiente virtual"
  echo "📝 Continuando sem ativar o ambiente virtual..."
fi
pip install -r requirements.txt

python data_collection/bike_api.py
python data_collection/download_shapes.py

python data_collection/ingest_postgis.py