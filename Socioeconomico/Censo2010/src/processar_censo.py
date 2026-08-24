import sqlite3
import pandas as pd
import os

print("--- Processando e Renomeando Colunas para o Banco SQLite ---")

# Caminhos padrão do projeto
caminho_csv = '../data/raw/Basico_SP2.csv'
pasta_processed = '../data/processed'
os.makedirs(pasta_processed, exist_ok=True)
db_path = os.path.join(pasta_processed, 'banco_tcc.db')

# Conectando ao banco SQLite
conexao = sqlite3.connect(db_path)

print(f"Lendo o arquivo CSV: {caminho_csv}...")
df_campinas = pd.read_csv(caminho_csv, sep=';', encoding='latin1')

# 1. Filtrando estritamente para Campinas (código 3509502)
df_campinas = df_campinas[df_campinas['Cod_municipio'].astype(str).str.startswith('3509502')].copy()

# 2. Dicionário completo de renomeação (Adicione mais colunas do Censo aqui se precisar)
colunas_renomeadas = {
    'Cod_setor': 'codigo_setor',
    'Cod_ibge': 'codigo_ibge',
    'Nome_do_distrito': 'nome_distrito',
    'Nome_do_subdistrito': 'nome_subdistrito',
    'Nome_do_bairro': 'nome_bairro',
    'V001': 'total_domicilios',
    'V002': 'total_moradores',
    'V003': 'media_moradores_por_domicilio',
    'V005': 'renda_media_domiciliar'
}

# 3. Aplicando o renomeio no DataFrame ANTES de jogar para o SQL
colunas_existentes = [c for c in colunas_renomeadas.keys() if c in df_campinas.columns]
df_tratado = df_campinas[colunas_existentes].rename(columns=colunas_renomeadas).copy()

# 4. Gravando no banco com os novos cabeçalhos
nome_tabela = 'tb_censo_campinas_limpo'
df_tratado.to_sql(nome_tabela, conexao, if_exists='replace', index=False)

# Validação: consultando o esquema da tabela no SQLite para provar que mudou
cursor = conexao.cursor()
cursor.execute(f"PRAGMA table_info({nome_tabela});")
colunas_no_banco = cursor.fetchall()

print("\n--- Cabeçalhos gravados com sucesso no SQLite ---")
for col in colunas_no_banco:
    print(f"Coluna: {col[1]} (Tipo: {col[2]})")

conexao.close()