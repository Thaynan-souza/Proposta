# 📊 TCC - Inteligência de Dados na Gestão Pública de Saúde (Campinas/SP)

Projeto acadêmico focado no desenvolvimento de um pipeline de dados (ETL) para extração, tratamento e análise espacial de microdados públicos. O objetivo é integrar indicadores de saúde (DATASUS) e de vulnerabilidade social (CadÚnico/IBGE) para mapear padrões territoriais no município de Campinas, auxiliando a tomada de decisão na gestão pública.

---

## 🏗️ Arquitetura do Projeto

O repositório está organizado de forma modular para separar os processos de extração, transformação e carga/análise espacial:

```text
tcc-datasus/
├── data/                  # 📁 Diretório local ignorado pelo Git (armazena os CSVs pesados)
├── notebooks/             # 📓 Jupyter Notebooks para análises exploratórias (EDA)
├── src/                   # 💻 Códigos-fonte do pipeline de ETL
│   ├── extract.py         # 📥 Script de coleta do DATASUS via FTP (Resiliente e Baixo Consumo de Memória)
│   ├── transform.py       # 🔄 Script de limpeza e unificação de dados (Em desenvolvimento)
│   ├── spatial.py         # 🗺️ Script de junção espacial via GeoPandas (Em breve)
│   └── database.py        # 🗄️ Script de conexão com o banco MySQL (Em breve)
├── .gitignore             # 🚫 Regras para não subir arquivos pesados para o GitHub
├── requirements.txt       # 📦 Dependências do projeto (Bibliotecas Python)
└── README.md              # 📖 Documentação do projeto

🚀 Status Atual do Desenvolvimento
Atualmente, concluímos a Fase 1: Extração de Dados (Extract).

O script src/extract.py foi construído para lidar de forma autônoma e resiliente com o Sistema de Informações sobre Mortalidade (SIM) do DATASUS. Suas principais características incluem:

Download Direto (FTP): Conecta diretamente aos servidores governamentais para baixar os microdados brutos (.dbc).

Descompactação Nativa: Utiliza pyreaddbc para transformar os dados em um formato legível localmente.

Leitura em Streaming (Linha por Linha): Lê o banco de dados estadual linha por linha utilizando dbfread, filtrando apenas os registros de Campinas (código IBGE 350950) antes de gerar o DataFrame do Pandas. Isso impede o esgotamento da memória (RAM) em ambientes de nuvem.

Série Histórica: Coleta automatizada dos últimos 5 anos de dados consolidados (2020 a 2024).

💻 Como Executar a Extração
Certifique-se de estar com o ambiente virtual ativado:

Bash
source .venv/bin/activate
Instale as dependências (caso seja a primeira execução):

Bash
pip install -r requirements.txt
Rode o script de extração:

Bash
python src/extract.py
Os arquivos CSV resultantes serão salvos automaticamente na pasta data/.

---

## 🔄 Fase 2: Transformação de Dados (Transform)

O script `src/transform.py` é responsável por limpar, padronizar e unificar os dados brutos extraídos, preparando-os para a análise espacial e cruzamentos futuros. Suas principais funções são:
- **Consolidação:** Unifica os arquivos anuais em uma única base de dados consolidada.
- **Tradução de Variáveis (Dicionários de Dados):** Decodifica as numerações originais do DATASUS para formatos textuais analíticos legíveis (ex: Idade, Sexo, Raça/Cor e Escolaridade).
- **Tratamento de CEPs:** Limpeza e padronização da formatação dos CEPs de residência para viabilizar o futuro georreferenciamento e cruzamento com indicadores do IBGE/CadÚnico.
- **Otimização:** Filtra apenas as colunas de interesse para reduzir o peso do arquivo final.

[ ] Análise Espacial: Obter os shapefiles de Campinas e cruzar os CEPs/Endereços com os polígonos dos bairros e setores censitários.
