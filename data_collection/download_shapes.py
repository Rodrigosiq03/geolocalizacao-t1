import requests, zipfile, io, os

URL = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2020/Brasil/BR/BR_Municipios_2020.zip"

print("🔽 Baixando shapefile IBGE...")
r = requests.get(URL)
r.raise_for_status()

print("📦 Extraindo apenas arquivos .shp/.shx/.dbf/.prj para data/shapes...")
z = zipfile.ZipFile(io.BytesIO(r.content))
os.makedirs("data/shapes", exist_ok=True)
for member in z.namelist():
    if member.endswith((".shp", ".shx", ".dbf", ".prj")):
        z.extract(member, "data/shapes")
        src = os.path.join("data/shapes", member)
        dst = os.path.join("data/shapes", os.path.basename(member))
        if src != dst:
            os.replace(src, dst)

print("✔️ Shapefiles extraídos em data/shapes/")
