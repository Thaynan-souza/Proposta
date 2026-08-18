import os
import pandas as pd
import urllib.request
from urllib.error import URLError
import pyreaddbc
from dbfread import DBF

def baixar_dados_sim_campinas(ano: int, estado: str = "SP"):
    print(f"📥 [SIM] Iniciando extração do ano {ano} para o estado {estado}...")

    # Força a criação e o uso da pasta data/raw/
    pasta_raw = os.path.join("..", "data", "raw")
    os.makedirs(pasta_raw, exist_ok=True)
    
    arquivo_csv = os.path.join(pasta_raw, f"sim_campinas_{ano}.csv")
    
    if os.path.exists(arquivo_csv):
        print(f"📦 Arquivo já existente em cache local: {arquivo_csv}. Pulando download.\n")
        return

    arquivo_dbc = f"DO{estado}{ano}.dbc"
    caminho_local_dbc = os.path.join(pasta_raw, arquivo_dbc)
    caminho_local_dbf = caminho_local_dbc.replace('.dbc', '.dbf')

    url_dores = f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DORES/{arquivo_dbc}"
    url_do = f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DO/{arquivo_dbc}"

    sucesso_download = False
    for url in [url_dores, url_do]:
        try:
            print(f"   -> Tentando baixar de: {url}")
            urllib.request.urlretrieve(url, caminho_local_dbc)
            sucesso_download = True
            print("   ✅ Download concluído com sucesso!")
            break
        except URLError:
            print("   ⚠️ Arquivo não encontrado neste diretório. Tentando o próximo...")

    if not sucesso_download:
        print(f"❌ Erro: Não foi possível encontrar a base de {ano}.\n")
        return

    print("   -> Lendo e filtrando o arquivo...")
    try:
        pyreaddbc.dbc2dbf(caminho_local_dbc, caminho_local_dbf)
        table = DBF(caminho_local_dbf, encoding='iso-8859-1')
        
        registros_campinas = []
        for linha in table:
            mun_res = str(linha.get('CODMUNRES', '')).strip()
            mun_ocor = str(linha.get('CODMUNOCOR', '')).strip()
            if mun_res.startswith('350950') or mun_ocor.startswith('350950'):
                registros_campinas.append(linha)
                
        df_campinas = pd.DataFrame(registros_campinas)
        print(f"   -> Registros filtrados exclusivamente para Campinas: {len(df_campinas)}")
        
    except Exception as e:
        print(f"❌ Erro ao ler/converter: {e}\n")
        if os.path.exists(caminho_local_dbc): os.remove(caminho_local_dbc)
        if os.path.exists(caminho_local_dbf): os.remove(caminho_local_dbf)
        return

    if not df_campinas.empty:
        df_campinas.to_csv(arquivo_csv, index=False, encoding='utf-8')
        
    if os.path.exists(caminho_local_dbc): os.remove(caminho_local_dbc)
    if os.path.exists(caminho_local_dbf): os.remove(caminho_local_dbf) 
        
    print(f"💾 Arquivo gerado com sucesso: {arquivo_csv}\n")

if __name__ == "__main__":
    anos_coleta = list(range(2020, 2025))
    print("🚀 === INICIANDO PIPELINE DE EXTRAÇÃO === ")
    for ano in anos_coleta:
        baixar_dados_sim_campinas(ano=ano)
    print("🎉 === PROCESSO CONCLUÍDO ===")