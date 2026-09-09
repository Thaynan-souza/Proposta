import os
import pandas as pd

def processar_sih_por_partes():
    print("🚀 Iniciando transformação em lotes da base SIH SP (2025)...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_path = os.path.join(base_dir, '../data/raw/sih_sp_2025.csv')
    output_path = os.path.join(base_dir, '../data/processed/sih_sp_2025_processado.csv')

    colunas_sih_significativas = {
        'UF_ZI': 'Unidade_Federativa', 'ANO_CMPT': 'Ano_Competencia',
        'MES_CMPT': 'Mes_Competencia', 'CGC_HOSP': 'CNPJ_Hospital',
        'N_AIH': 'Numero_AIH', 'CEP': 'CEP_Paciente',
        'MUNIC_RES': 'Codigo_Municipio_Residencia', 'NASC': 'Data_Nascimento',
        'SEXO': 'Sexo_Paciente', 'QT_DIARIAS': 'Quantidade_Diarias',
        'VAL_TOT': 'Valor_Total_Internacao', 'VAL_UTI': 'Valor_UTI',
        'DT_INTER': 'Data_Internacao', 'DT_SAIDA': 'Data_Saida',
        'DIAG_PRINC': 'Diagnostico_Principal_CID', 'DIAG_SECUN': 'Diagnostico_Secundario_CID',
        'MORTE': 'Indicador_Obito', 'IDADE': 'Idade',
        'RACA_COR': 'Raca_Cor', 'CNES': 'Codigo_CNES_Hospital'
    }

    colunas_necessarias = list(colunas_sih_significativas.keys())
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Se já existir um arquivo antigo processado, remove para recomeçar limpo
    if os.path.exists(output_path):
        os.remove(output_path)

    print("Lendo e processando o arquivo em blocos de 100 mil linhas...")
    tamanho_lote = 100000
    primeiro_lote = True
    total_linhas = 0

    # O chunksize lê o arquivo gigante em pedaços pequenos, poupando a RAM
    for chunk in pd.read_csv(input_path, sep=',', dtype={'CEP': str, 'MUNIC_RES': str}, usecols=colunas_necessarias, low_memory=False, chunksize=tamanho_lote):
        
        chunk.rename(columns=colunas_sih_significativas, inplace=True)
        chunk['Codigo_Municipio_Residencia'] = chunk['Codigo_Municipio_Residencia'].astype(str).str[:6]

        cids_saneamento = ('A0', 'A27', 'B65', 'A90', 'A91')
        chunk['Grupo_Saneamento'] = chunk['Diagnostico_Principal_CID'].astype(str).str.startswith(cids_saneamento, na=False)
        chunk['Grupo_Saneamento'] = chunk['Grupo_Saneamento'].map({True: 'Relacionada ao Saneamento', False: 'Outras Causas'})

        # Salva incrementalmente no arquivo final
        chunk.to_csv(output_path, sep=';', index=False, encoding='utf-8', mode='w' if primeiro_lote else 'a', header=primeiro_lote)
        
        total_linhas += len(chunk)
        primeiro_lote = False
        print(f"   -> Processados e salvos: {total_linhas} registros...")

    print(f"✅ Sucesso! Base estadual processada com {total_linhas} registros.")
    print(f"📁 Arquivo salvo em: {output_path}")

if __name__ == "__main__":
    processar_sih_por_partes()