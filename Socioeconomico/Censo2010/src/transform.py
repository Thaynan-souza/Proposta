import pandas as pd
import os

def process_basico_campinas():
    # Caminhos relativos considerando a execução na raiz do workspace (/workspaces/Proposta)
    input_path = 'Socioeconomico/Censo2010/data/raw/Basico_SP2.csv'
    output_path = 'Socioeconomico/Censo2010/data/processed/Basico_Campinas.csv'

    print("Carregando o arquivo original...")
    
    # O arquivo do IBGE utiliza separador de ponto e vírgula e decimais com vírgula.
    # O enconding 'latin1' ou 'iso-8859-1' previne problemas com caracteres especiais (como os "" vistos no arquivo).
    df = pd.read_csv(input_path, sep=';', decimal=',', encoding='latin1')

    # Filtrar os setores apenas para o município de Campinas
    print("Filtrando os dados para Campinas...")
    df_campinas = df[df['Nome_do_municipio'] == 'CAMPINAS'].copy()

    # Dicionário com os nomes significativos das variáveis Básicas do Censo 2010
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

    # Renomear os cabeçalhos
    print("Renomeando cabeçalhos V001-V012...")
    df_campinas.rename(columns=colunas_significativas, inplace=True)

    # Garantir que a pasta de destino exista
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Salvar o novo arquivo CSV (agora em utf-8 para facilitar o uso no Power BI ou bancos de dados)
    df_campinas.to_csv(output_path, sep=';', index=False, encoding='utf-8')
    
    print(f"Sucesso! Foram processados {len(df_campinas)} setores censitários de Campinas.")
    print(f"Arquivo salvo em: {output_path}")

if __name__ == "__main__":
    process_basico_campinas()