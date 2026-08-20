import os
import glob
import pandas as pd
from datasus_dbc import decompress
from dbfread import DBF

def transformar_dados_esus():
    print("🔄 === INICIANDO PROCESSAMENTO DOS DADOS DO e-SUS (SIA) ===")
    
    caminho_raw = os.path.join("..", "data", "raw")
    caminho_processed = os.path.join("..", "data", "processed")
    os.makedirs(caminho_processed, exist_ok=True)
    
    arquivos_dbc = glob.glob(os.path.join(caminho_raw, "ABOSP*.dbc"))
    
    if not arquivos_dbc:
        print("❌ Nenhum arquivo .dbc encontrado com o prefixo ABOSP na pasta raw.")
        return

    print(f"📁 Arquivos .dbc encontrados para processamento: {len(arquivos_dbc)}")
    lista_dfs = []
    
    for arq in arquivos_dbc:
        nome_arq = os.path.basename(arq)
        caminho_dbf = arq.replace(".dbc", ".dbf")
        print(f"  -> Processando {nome_arq}...")
        
        try:
            # 1. Descompacta o arquivo .dbc original para .dbf
            decompress(arq, caminho_dbf)
            
            # 2. Lê os dados do .dbf gerado
            tabela_dbf = DBF(caminho_dbf, encoding='iso-8859-1')
            df = pd.DataFrame(iter(tabela_dbf))
            
            # 3. Filtra apenas Campinas
            if 'PA_MUNIC' in df.columns:
                df_campinas = df[df['PA_MUNIC'] == '350950']
            elif 'MUNIC_RES' in df.columns:
                df_campinas = df[df['MUNIC_RES'] == '350950']
            else:
                df_campinas = df
                
            lista_dfs.append(df_campinas)
            
            # 4. Remove o .dbf temporário para limpar o diretório
            if os.path.exists(caminho_dbf):
                os.remove(caminho_dbf)
                
        except Exception as e:
            print(f"  -> Erro ao processar {nome_arq}: {e}")
            
    if lista_dfs:
        df_consolidado = pd.concat(lista_dfs, ignore_index=True)
        caminho_saida = os.path.join(caminho_processed, "esus_campinas_2023.csv")
        df_consolidado.to_csv(caminho_saida, index=False)
        
        print(f"\n🎉 === PROCESSAMENTO CONCLUÍDO COM SUCESSO! ===")
        print(f"Arquivo salvo em: {caminho_saida}")
        print(f"Total de registros de Campinas consolidados: {len(df_consolidado)}")
    else:
        print("❌ Nenhum dado foi processado com sucesso.")

if __name__ == "__main__":
    transformar_dados_esus()