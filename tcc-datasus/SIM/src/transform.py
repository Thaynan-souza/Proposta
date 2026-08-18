import pandas as pd
import glob
import os

def transformar_dados_sim():
    print("Iniciando a transformação e consolidação dos dados do SIM...")
    
    # Busca os arquivos voltando um nível (..) e entrando em data/raw/
    caminho_busca = os.path.join("..", "data", "raw", "sim_campinas_*.csv")
    arquivos = glob.glob(caminho_busca)
    
    if not arquivos:
        print("Aviso: Nenhum arquivo bruto do SIM foi encontrado na pasta '../data/raw/'.")
        return

    print(f"Arquivos encontrados para consolidação: {len(arquivos)}")

    lista_dfs = []
    for arq in arquivos:
        print(f"Lendo arquivo: {arq}")
        df_temp = pd.read_csv(arq, low_memory=False, dtype=str)
        lista_dfs.append(df_temp)

    df_consolidado = pd.concat(lista_dfs, ignore_index=True)

    # Cria/Salva na pasta processed
    diretorio_saida = os.path.join("..", "data", "processed")
    os.makedirs(diretorio_saida, exist_ok=True)
    
    caminho_saida = os.path.join(diretorio_saida, "sim_campinas.csv")
    df_consolidado.to_csv(caminho_saida, index=False)

    print(f"\nTransformação concluída com sucesso!")
    print(f"Arquivo salvo em: {caminho_saida}")
    print(f"Total de registros consolidados: {len(df_consolidado)}")
    print(f"Total de colunas preservadas: {len(df_consolidado.columns)}")

if __name__ == "__main__":
    transformar_dados_sim()