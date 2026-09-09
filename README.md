# 📊 TCC - Inteligência de Dados na Gestão Pública de Saúde (Campinas/SP)

Projeto acadêmico focado no desenvolvimento de um pipeline de dados (ETL) para extração, tratamento e análise espacial de microdados públicos. O objetivo é integrar indicadores de saúde (DATASUS) e de vulnerabilidade social (CadÚnico/IBGE) para mapear padrões territoriais no município de Campinas, auxiliando a tomada de decisão na gestão pública.

---

## 🏗️ Arquitetura do Projeto

O repositório está organizado de forma modular para separar os processos de extração, tratamento e análise espacial:

```text
tcc-datasus/
├── SIM/                   # 📁 Módulo de Mortalidade (Óbitos)
│   ├── data/              # 📁 Dados brutos e processados do SIM
│   ├── notebooks/         # 📓 Análises exploratórias de mortalidade (Ano, Sexo, Idade, Raça)
│   └── src/               # 💻 Scripts de ETL do SIM
├── SIH/                   # 📁 Módulo de Internações Hospitalares
│   ├── data/              # 📁 Dados brutos e processados do SIH
│   ├── notebooks/         # 📓 Análises de internações, CEPs e causas (CID-10)
│   └── src/               # 💻 Scripts de extração do SIH
├── .gitignore             # 🚫 Regras para ignorar arquivos pesados (CSV/DBC)
├── requirements.txt       # 📦 Dependências do projeto (Bibliotecas Python)
└── README.md              # 📖 Documentação do projeto

🚀 Status Atual do Desenvolvimento
1️⃣ Fase de Extração (Extract) — Concluída
SIM (Mortalidade): Coleta automatizada via FTP dos últimos 5 anos de óbitos em Campinas (2020–2024), com preservação de todas as 87 colunas originais do DATASUS.

SIH (Internações): Pipeline mensal implementado para extração de microdados de internação (RD), filtrando de forma otimizada (linha por linha) apenas os registros de moradores de Campinas (código IBGE 350950).

2️⃣ Fase de Análise Exploratória (EDA) — Em Andamento
Mortalidade: Cruzamentos populacionais por Ano, Faixa Etária, Sexo e Raça/Cor das principais causas de óbito (com destaque para o impacto da COVID-19, infartos e Alzheimer).

Internações: Validação do preenchimento de CEPs (100% de cobertura na base de 2023) e mapeamento preliminar por regiões e causas principais de internação hospitalar via CID-10.

💻 Como Executar o Projeto
Certifique-se de estar com o ambiente virtual ativado e as dependências instaladas:

Bash
# Ativa o ambiente virtual
source .venv/bin/activate

# Instala as bibliotecas necessárias
pip install -r requirements.txt
Para rodar a extração dos dados brutos do DATASUS:

Bash
# Extração do SIM (Óbitos)
cd SIM/src && python extract.py

# Extração do SIH (Internações)
cd SIH/src && python extract.py

---

Após colar e salvar o arquivo, basta fazer o último commit e push rápido para atualizar a página principal do GitHub:
```bash
git add README.md
git commit -m "docs: atualiza o README com a estrutura do SIH e status atual"
git push
