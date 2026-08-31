import os
import pandas as pd
import urllib.request
import pyreaddbc
from dbfread import DBF

def baixar_dados_sih_sp(ano: int, estado: str = "SP"):
    print(f"📥 [SIH] Iniciando extração otimizada por lotes de {ano} ({estado})...")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_raw = os.path.join(base_dir, "..", "data", "raw")
    os.makedirs(pasta_raw, exist_ok=True)
    arquivo_csv = os.path.join(pasta_raw, f"sih_sp_{ano}.csv")
    
    if os.path.exists(arquivo_csv):
        os.remove(arquivo_csv)

    ano_curto = str(ano)[-2:]
    meses = [str(m).zfill(2) for m in range(1, 13)] 
    total_registros = 0
    
    for mes in meses:
        arquivo_dbc = f"RD{estado}{ano_curto}{mes}.dbc"
        caminho_local_dbc = os.path.join(pasta_raw, arquivo_dbc)
        caminho_local_dbf = caminho_local_dbc.replace('.dbc', '.dbf')
        url = f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/{arquivo_dbc}"
        
        try:
            print(f"   -> Baixando e processando {mes}/{ano}... ", end="", flush=True)
            urllib.request.urlretrieve(url, caminho_local_dbc)
            
            pyreaddbc.dbc2dbf(caminho_local_dbc, caminho_local_dbf)
            table = DBF(caminho_local_dbf, encoding='iso-8859-1')
            
            # Lendo em lotes (chunks) de 50 mil registros para poupar a RAM do Codespaces
            lote = []
            registros_mes = 0
            escrever_cabecalho = (total_registros == 0)
            
            for registro in table:
                lote.append(registro)
                if len(lote) >= 50000:
                    df_lote = pd.DataFrame(lote)
                    df_lote.to_csv(arquivo_csv, mode='a', index=False, encoding='utf-8', header=escrever_cabecalho)
                    escrever_cabecalho = False
                    registros_mes += len(df_lote)
                    total_registros += len(df_lote)
                    lote = [] # Limpa a lista do lote da memória

            # Salva o restante que sobrou (menos de 50 mil)
            if lote:
                df_lote = pd.DataFrame(lote)
                df_lote.to_csv(arquivo_csv, mode='a', index=False, encoding='utf-8', header=escrever_cabecalho)
                registros_mes += len(df_lote)
                total_registros += len(df_lote)

            print(f"✅ {registros_mes} registros.")
                
        except Exception as e:
            print(f"⚠️ Falha no mês {mes}/{ano}: {e}")
            
        finally:
            if os.path.exists(caminho_local_dbc): 
                os.remove(caminho_local_dbc)
            if os.path.exists(caminho_local_dbf): 
                os.remove(caminho_local_dbf)

    print(f"💾 Arquivo anual salvo: {arquivo_csv} com {total_registros} internações!\n")

if __name__ == "__main__":
    anos_coleta = [2025] 
    print("🚀 === INICIANDO PIPELINE DE EXTRAÇÃO (SIH - SP) === ")
    for ano in anos_coleta:
        baixar_dados_sih_sp(ano=ano)
    print("🎉 === PROCESSO CONCLUÍDO ===")