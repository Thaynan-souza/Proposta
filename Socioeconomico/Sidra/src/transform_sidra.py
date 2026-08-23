import os
import pandas as pd

def transformar_dados_sidra():
    print("Iniciando a transformação dos dados do SIDRA (IBGE)...")
    
    # Caminhos baseados na sua estrutura de pastas
    caminho_entrada = "Socioeconomico/Sidra/data/raw/tabela4714.csv"
    pasta_processed = "Socioeconomico/Sidra/data/processed"
    os.makedirs(pasta_processed, exist_ok=True)
    caminho_saida = os.path.join(pasta_processed, "sidra_campinas_tratado.csv")
    
    if not os.path.exists(caminho_entrada):
        print(f"⚠️ Arquivo não encontrado em: {caminho_entrada}. Verifique se o arquivo está na pasta raw.")
        return
    
    try:
        # Pula as primeiras linhas de metadados/cabeçalho institucional do IBGE
        # O skiprows pula o cabeçalho textual e o sep=';' lê o delimitador correto
        df = pd.read_csv(caminho_entrada, sep=';', skiprows=4, encoding='utf-8', dtype=str)
        
        print(f"Colunas brutas encontradas: {df.columns.tolist()}")
        
        # Remove eventuais linhas vazias ou sujeiras remanescentes
        df = df.dropna(how='all')
        
        # Salva o arquivo limpo e tratado na pasta processed
        df.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8')
        
        print(f"✅ Sucesso! Dados limpos e salvos em: {caminho_saida}")
        print("\n📊 PRÉVIA DOS DADOS TRATADOS:")
        print(df.head())
        
    except Exception as e:
        print(f"⚠️ Erro ao transformar os dados: {e}")

if __name__ == "__main__":
    transformar_dados_sidra()