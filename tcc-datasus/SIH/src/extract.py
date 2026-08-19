import os
import pandas as pd
import urllib.request
from urllib.error import URLError
import pyreaddbc
from dbfread import DBF

def baixar_dados_sih_campinas(ano: int, estado: str = "SP"):
    print(f"📥 [SIH] Iniciando extração das internações de {ano} ({estado})...")

    pasta_raw = os.path.join("..", "data", "raw")
    os.makedirs(pasta_raw, exist_ok=True)
    arquivo_csv = os.path.join(pasta_raw, f"sih_campinas_{ano}.csv")
    
    if os.path.exists(arquivo_csv):
        print(f"📦 Arquivo já existente em cache local: {arquivo_csv}. Pulando.\n")
        return

    # O SIH usa os 2 últimos dígitos do ano (ex: 2023 vira '23')
    ano_curto = str(ano)[-2:]
    meses = [str(m).zfill(2) for m in range(1, 13)] # ['01', '02', ..., '12']
    
    lista_dfs_meses = []
    
    for mes in meses:
        # Padrão de arquivo: RD (Resumo de Internação) + UF + Ano + Mês
        arquivo_dbc = f"RD{estado}{ano_curto}{mes}.dbc"
        caminho_local_dbc = os.path.join(pasta_raw, arquivo_dbc)
        caminho_local_dbf = caminho_local_dbc.replace('.dbc', '.dbf')
        
        # Caminho oficial do FTP do DATASUS para o SIH
        url = f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/{arquivo_dbc}"
        
        try:
            print(f"   -> Baixando {mes}/{ano}... ", end="")
            urllib.request.urlretrieve(url, caminho_local_dbc)
            
            # Descompacta e lê linha por linha para economizar memória
            pyreaddbc.dbc2dbf(caminho_local_dbc, caminho_local_dbf)
            table = DBF(caminho_local_dbf, encoding='iso-8859-1')
            
            registros_campinas = []
            for linha in table:
                # MUNIC_RES = Município de Residência. 350950 = Campinas
                mun_res = str(linha.get('MUNIC_RES', '')).strip()
                if mun_res.startswith('350950'):
                    registros_campinas.append(linha)
            
            if registros_campinas:
                lista_dfs_meses.append(pd.DataFrame(registros_campinas))
                print(f"✅ {len(registros_campinas)} registros.")
            else:
                print("✅ 0 registros.")
                
        except Exception as e:
            print(f"⚠️ Erro ao processar: {e}")
            
        # Limpeza obrigatória para não estourar o disco do Codespaces
        if os.path.exists(caminho_local_dbc): os.remove(caminho_local_dbc)
        if os.path.exists(caminho_local_dbf): os.remove(caminho_local_dbf)

    # Consolida os 12 meses do ano e salva no raw
    if lista_dfs_meses:
        df_ano = pd.concat(lista_dfs_meses, ignore_index=True)
        df_ano.to_csv(arquivo_csv, index=False, encoding='utf-8')
        print(f"💾 Arquivo anual salvo: {arquivo_csv} com {len(df_ano)} internações!\n")
    else:
        print(f"❌ Nenhum dado encontrado para {ano}.\n")

if __name__ == "__main__":
    anos_coleta = [2020, 2021, 2022, 2024, 2025] 
    print("🚀 === INICIANDO PIPELINE DE EXTRAÇÃO (SIH) === ")
    for ano in anos_coleta:
        baixar_dados_sih_campinas(ano=ano)
    print("🎉 === PROCESSO CONCLUÍDO ===")