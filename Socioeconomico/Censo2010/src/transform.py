import pandas as pd
import os

def process_basico_completo():
    # Obtém o diretório atual do script (src) e mapeia os caminhos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, '../data/raw/Basico_SP2.csv')
    output_path = os.path.join(base_dir, '../data/processed/Basico_SP2_Processado.csv')

    print("Carregando o arquivo original com todas as cidades...")
    df = pd.read_csv(input_path, sep=';', decimal=',', encoding='latin1')

    # Dicionário com os nomes significativos das variáveis
    colunas_significativas = {
        'V001': 'Domicilios_Particulares_Permanentes',
        'V002': 'Moradores_Domicilios_Particulares',
        'V003': 'Media_Moradores_por_Domicilio',
        'V004': 'Variancia_Moradores',
        'V005': 'Renda_Media_Mensal_Pessoas_10_Anos_ou_Mais',
        'V006': 'Variancia_Renda_Pessoas',
        'V007': 'Renda_Media_Mensal_Domicilios',
        'V008': 'Variancia_Renda_Domicilios',
        'V009': 'Renda_Media_Mensal_Pessoas_Com_Rendimento',
        'V010': 'Variancia_Renda_Pessoas_Com_Rendimento',
        'V011': 'Renda_Media_Mensal_Domicilios_Com_Rendimento',
        'V012': 'Variancia_Renda_Domicilios_Com_Rendimento'
    }

    print("Renomeando cabeçalhos V001-V012...")
    df.rename(columns=colunas_significativas, inplace=True)

    # Criar pasta e salvar
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep=';', index=False, encoding='utf-8')
    
    print(f"Sucesso! Foram processados {len(df)} setores censitários (todas as cidades).")
    print(f"Arquivo salvo em: {output_path}")

if __name__ == "__main__":
    process_basico_completo()