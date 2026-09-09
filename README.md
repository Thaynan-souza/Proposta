# Análise Socioeconômica e de Saúde (TCC)

Este repositório contém o pipeline de dados desenvolvido para o Trabalho de Conclusão de Curso (TCC). O objetivo do projeto é extrair, processar e cruzar dados de internações hospitalares (DATASUS) com indicadores demográficos e de saneamento básico (IBGE/SIDRA) para o Estado de São Paulo.

---

## 📚 O que são as Bases de Dados Utilizadas?

Para garantir a fundamentação da análise, o projeto integra dados de três grandes sistemas de informações públicas do Brasil:

**1. Censo Demográfico (IBGE)**
A pesquisa mais ampla sobre a população brasileira. Utilizamos os dados agregados por **Setores Censitários** (a menor divisão territorial mapeada pelo IBGE) para identificar com alta precisão características domiciliares e de renda em nível de bairro. Isso permite classificar regiões (Sede vs. Periferia) e mapear a desigualdade intraurbana detalhadamente.

**2. SIDRA - Sistema IBGE de Recuperação Automática**
É o banco de dados oficial do IBGE que centraliza e disponibiliza tabelas consolidadas de diversas pesquisas. Neste projeto, extraímos indicadores em nível **Municipal** para todo o Estado de São Paulo, focando nas infraestruturas que impactam a saúde:
* **Tabela 4714**: População residente e estimativas demográficas.
* **Tabela 6803**: Proporção de domicílios com abastecimento de água adequado.
* **Tabela 6805**: Proporção de domicílios com esgotamento sanitário (rede geral).
* **Tabela 10295**: Indicadores de rendimento e características domiciliares.

**3. SIH/DATASUS - Sistema de Informações Hospitalares**
É o sistema do Ministério da Saúde responsável por registrar todas as internações financiadas pelo Sistema Único de Saúde (SUS) por meio da emissão da AIH (Autorização de Internação Hospitalar).
* **O que utilizamos:** Os arquivos massivos de microdados de internações do Estado de São Paulo (2025).
* **O que eles indicam:** Permitem analisar os motivos da internação (diagnósticos), custos, tempo de permanência e o desfecho do paciente — especialmente a coluna de **Óbito (MORTE)** —, permitindo cruzar a morbidade e mortalidade hospitalar com a precariedade sanitária apontada pelo IBGE.

---

## 📂 Estrutura do Projeto

O repositório foi modularizado em dois grandes blocos de análise:
- **`Socioeconomico/Sidra/`**: Dedicado à extração e tratamento dos dados demográficos e de infraestrutura do IBGE.
- **`tcc-datasus/SIH/`**: Focado no processamento das bases massivas de morbidade hospitalar do SUS.

*Nota: As pastas `data/raw/` e `data/processed/` são ignoradas no versionamento do Git devido ao limite de tamanho de arquivos (Large File Storage), garantindo que apenas os códigos-fonte sejam versionados.*

---

## ⚙️ Códigos de Extração e Transformação (ETL)

### Módulo Socioeconômico (IBGE/SIDRA)
* **`extract_sidra.py`**: Conecta-se à API ou fontes do IBGE para realizar o download automatizado das tabelas dos agregados (População, Água, Esgoto e Renda) e salva os arquivos brutos.
* **`transform_sidra.py`**: Realiza a limpeza dos dados brutos do estado de São Paulo. Ele padroniza os cabeçalhos para o formato `snake_case`, remove sufixos desnecessários (como " - SP" dos nomes dos municípios) e exporta planilhas unificadas e prontas para cruzamento.

### Módulo Saúde (DATASUS/SIH)
* **`extract.py`**: Conecta-se ao FTP do DATASUS e realiza o download dos arquivos brutos mensais (em formato `.dbc`) de São Paulo, convertendo-os estruturalmente para iniciar o processamento.
* **`transform.py`**: Desenvolvido para lidar com grandes volumes de dados (Big Data). Ele lê as bases estaduais do SIH em lotes (*chunks*), otimizando o uso de memória, aplica filtros de limpeza e consolida as internações em um arquivo CSV processado final.

---

## 🚀 Como Executar

1. Crie o ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Execute os scripts de extração nas pastas src/ para baixar os dados para a pasta data/raw/.

3. Execute os scripts de transformação para gerar os dados limpos na pasta data/processed/.