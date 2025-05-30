# Projeto CIC901 – Geolocalização e Mapas Digitais (Parte 1)

**Alunos:** Rodrigo Diana Siqueira e Rafael Bidetti Baldi Simões Ferreira
**RA:** 22.00680-0 e 22.01019-0

## Tema
Análise das estações de bike‑sharing (Bike Sampa) em São Paulo.

## Ferramentas e Tecnologias

- **Python 3.9+** com bibliotecas:
  - `requests`
  - `pandas`
  - `geopandas`
  - `sqlalchemy`
  - `psycopg2-binary`
  - `matplotlib`
  - `folium`
- **Docker & Docker Compose**
  - Container `postgis/postgis:15-3.3`
  - Container `jupyter/scipy-notebook`
- **PostgreSQL + PostGIS**
- **Jupyter Notebook**

## Estrutura de Arquivos

```bash
projeto-geolocalizacao/ 
└── data/ 
    ├── bike/ 
    │      ├── station_information.json  
    │      ├── station_status.json 
    ├── shapes/ 
    │      ├── BR_Municipios_2020.shp 
    │      ├── BR_Municipios_2020.shx 
    │      ├── BR_Municipios_2020.dbf 
    │      └── BR_Municipios_2020.prj 
└── data_collection/ 
    │      ├── download_shapes.py 
    │      ├── bike_api.py 
    │      └── ingest_postgis.py 
└── notebooks/ 
    │      ├── 1_coleta_e_ingestao.ipynb 
    │      └── 2_analise_inicial.ipynb 
└── docker-compose.yml 
└── README.md
└── bash.example.sh
└── .gitignore
└── requirements.txt
```


## Como Executar

### 1. Preparar o ambiente Python
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Iniciar o container e rodar scripts
```bash
# Deixe o script executável
chmod +x bash.example.sh

# Pelo Bash no Windows
chmod +x bash.windows.sh

# Rode o script
./bash.example.sh

# Pelo Bash no Windows
./bash.windows.sh

# Rode o bloco de codigo do jupyter notebook notebooks/coleta_e_ingestao.ipynb
```

### 3. Acessar o Jupyter Notebook
```bash
docker exec -it jupyter jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

### 4. Acessar o PostgreSQL
```bash
docker exec -it postgis psql -U gis -d geodb
```

## Possíveis Estudos a partir dos Dados

- **Análise de Hotspots (DBSCAN)**  
  Identificar clusters espaciais de estações com alta escassez (baixo número de bikes) para orientar realocação de frotas.

- **Correlação Socioeconômica**  
  Fazer join com camada de renda média por bairro (IBGE) e usar regressão espacial para ver se renda influencia disponibilidade.

- **Série Temporal de Uso**  
  Armazenar snapshots diários de `station_status` e analisar padrões sazonais (hora do dia, dias da semana, meses).

- **Otimização de Rebalanceamento**  
  Modelar rotas de rebalanceamento de bikes minimizando distância e custo, usando grafos (NetworkX).

- **Análise de Acessibilidade**  
  Calcular isócronas (tempo de caminhada de 5/10 minutos) em torno das estações para avaliar cobertura da malha.


## Proposta de Análise Final

**Objetivo:**  
Aplicar **DBSCAN** para identificar hotspots de escassez de bicicletas nas estações e, em seguida, realizar uma **regressão espacial (GWR)** entre a densidade populacional / renda média por bairro e a disponibilidade média de bicicletas.

**Passos:**
1. Gerar dataset de features por estação: latitude, longitude, média diária de `num_bikes_available`.  
2. Rodar DBSCAN para agrupar estações críticas (mínimo de 5 estações por cluster, distância eps=500 m).  
3. Agregar renda média e população de cada cluster (usando shapefile de distritos).  
4. Executar GWR para avaliar influência de variáveis socioeconômicas na disponibilidade.  
5. Visualizar resultados em mapas temáticos e avaliar recomendações de rebalanceamento.

Esse fluxo permitirá validar se fatores socioeconômicos estão associados à oferta de bikes e indicar políticas de realocação mais eficientes.


