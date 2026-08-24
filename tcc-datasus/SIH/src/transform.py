import pandas as pd
import requests
import os
import time

def buscar_bairro_unico(cep_limpo):
    """Faz a requisição na API para um CEP já limpo e validado."""
    if len(cep_limpo) != 8:
        return "CEP Invalido"
        
    try:
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            if "erro" not in dados:
                return dados.get('bairro', 'Bairro vazio na base')
    except Exception:
        pass # Ignora o erro no terminal para não poluir a tela
        
    return "Nao encontrado/Erro"

def processar_sih():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, '../data/raw/sih_campinas_2025.csv')
    output_path = os.path.join(base_dir, '../data/processed/sih_campinas_2025_processado.csv')

    print("Carregando o arquivo original do SIH...")
    df = pd.read_csv(input_path, sep=',', dtype={'CEP': str}, low_memory=False)

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

    print("Renomeando cabeçalhos do DataSUS...")
    df.rename(columns=colunas_sih_significativas, inplace=True)

    # OTIMIZAÇÃO: Isola apenas os CEPs únicos para evitar milhares de consultas repetidas
    print("Identificando CEPs únicos...")
    ceps_unicos = df['CEP_Paciente'].dropna().unique()
    print(f"Total de {len(ceps_unicos)} CEPs únicos para consultar. Iniciando API...")
    
    cache_ceps = {}
    
    for i, cep in enumerate(ceps_unicos):
        if i > 0 and i % 50 == 0:
            print(f"Progresso: {i} de {len(ceps_unicos)} CEPs consultados...")
            
        # Limpeza do CEP
        cep_limpo = str(cep).replace(".0", "").replace("-", "").strip().zfill(8)
        
        # Consulta e salva no dicionário
        cache_ceps[cep] = buscar_bairro_unico(cep_limpo)
        
        # Pausa fundamental para não ser bloqueado pelo ViaCEP
        time.sleep(0.3)

    print("Mapeando os bairros de volta para a base completa...")
    df['Bairro_Paciente'] = df['CEP_Paciente'].map(cache_ceps)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep=';', index=False, encoding='utf-8')
    
    print(f"Sucesso! Arquivo gerado em: {output_path}")

if __name__ == "__main__":
    processar_sih()