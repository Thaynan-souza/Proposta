import pandas as pd
import os

def limpar_dados_censo():
    print("Carregando a base bruta de Setores Censitários de Campinas...")
    
    # Caminho corrigido com a pasta raiz correta (Projeto_Base_de_dados)
    caminho_raw = "../data/raw/bq-results-20260823-192758-1787513308171.csv"
    
    df_bruto = pd.read_csv(caminho_raw)
    df_bruto.columns = df_bruto.columns.str.lower()
    
    dicionario_colunas = {
        'id_setor_censitario': 'id_setor',
        'geometria': 'geometria',
        'pessoas': 'total_pessoas',
        'domicilios': 'total_domicilios',
        'v00090': 'resp_branca',
        'v00091': 'resp_preta',
        'v00092': 'resp_amarela',
        'v00093': 'resp_parda',
        'v00094': 'resp_indigena',
        'v00105': 'resp_masculino',
        'v00106': 'resp_feminino',
        'v00238': 'domicilios_sem_banheiro'
    }
    
    print("Filtrando e traduzindo as variáveis do IBGE...")
    
    df_limpo = df_bruto[list(dicionario_colunas.keys())].rename(columns=dicionario_colunas)
    cols_numericas = df_limpo.columns.drop(['id_setor', 'geometria'])
    df_limpo[cols_numericas] = df_limpo[cols_numericas].fillna(0).astype(int)
    df_limpo['resp_negra_total'] = df_limpo['resp_preta'] + df_limpo['resp_parda']
    
    pasta_processed = "../data/processed"
    os.makedirs(pasta_processed, exist_ok=True)
    caminho_salvo = os.path.join(pasta_processed, "setores_campinas_limpo.csv")
    
    df_limpo.to_csv(caminho_salvo, index=False, sep=';')
    
    print(f"\n✅ SUCESSO! Base limpa salva em: {caminho_salvo}")

if __name__ == "__main__":
    limpar_dados_censo()