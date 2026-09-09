import pandas as pd
import os

print("--- Iniciando ETL das tabelas do SIDRA (Estado de São Paulo) ---")

# 1. Correção dos caminhos: usa o local do script para achar a pasta data dinamicamente
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pasta_raw = os.path.join(BASE_DIR, 'data', 'raw')
pasta_processed = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(pasta_processed, exist_ok=True)

arquivos_sidra = {
    'populacao': 'tabela_4714_populacao.csv',
    'agua': 'tabela_6803_agua.csv',
    'esgoto': 'tabela_6805_esgoto.csv',
    'renda': 'tabela_10295_renda.csv'
}

for nome, arquivo in arquivos_sidra.items():
    caminho_arquivo = os.path.join(pasta_raw, arquivo)
    
    if os.path.exists(caminho_arquivo):
        print(f"Processando {arquivo}...")
        df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8')
        
        # 2. Padronizar nomes das colunas para snake_case limpo
        df.columns = [c.strip().lower().replace(' ', '_').replace('__', '_') for c in df.columns]
        
        # 3. Limpar o sufixo ' - SP' e manter TODOS os municípios do estado
        if 'municipio' in df.columns:
            df['municipio'] = df['municipio'].astype(str).str.replace(r'\s*-\s*SP$', '', regex=True).str.strip()
            
        # 4. Salvar o arquivo limpo e processado para o estado inteiro
        caminho_saida = os.path.join(pasta_processed, f'sidra_{nome}_sp_tratado.csv')
        df.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')
        print(f"-> Salvo com sucesso: {caminho_saida}")
    else:
        print(f"Erro: Arquivo {arquivo} não encontrado no caminho {caminho_arquivo}.")

print("--- ETL do SIDRA concluído para o Estado de SP! ---")