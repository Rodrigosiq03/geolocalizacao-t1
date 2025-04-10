import requests, json, os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'bike')
os.makedirs(DATA_DIR, exist_ok=True)

GBFS_URL = "https://saopaulo.publicbikesystem.net/customer/gbfs/v2/gbfs.json"
r = requests.get(GBFS_URL)
r.raise_for_status()
feeds = r.json()['data']['en']['feeds']
feed_map = {f['name']: f['url'] for f in feeds}

info_url = feed_map.get('station_information')
if not info_url:
    raise RuntimeError("station_information não encontrado no GBFS")
r_info = requests.get(info_url); r_info.raise_for_status()
with open(os.path.join(DATA_DIR, 'station_information.json'), 'w', encoding='utf-8') as f:
    json.dump(r_info.json(), f, ensure_ascii=False, indent=2)

status_url = feed_map.get('station_status')
if not status_url:
    raise RuntimeError("station_status não encontrado no GBFS")
r_stat = requests.get(status_url); r_stat.raise_for_status()
with open(os.path.join(DATA_DIR, 'station_status.json'), 'w', encoding='utf-8') as f:
    json.dump(r_stat.json(), f, ensure_ascii=False, indent=2)

print("✔️ Dados GBFS salvos em", DATA_DIR)
