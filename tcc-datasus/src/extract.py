import os
import pandas as pd
import urllib.request
from urllib.error import URLError
import pyreaddbc
from dbfread import DBF

def baixar_dados_sim_campinas(ano: int, estado: str = "SP"):
    """
    Baixa o arquivo bruto (.dbc) direto do FTP do DATASUS, descompacta,
    lê linha por linha (para não estourar a memória do Codespaces) e converte 
    para Pandas filtrando apenas o município de Campinas.
    """
    print(f"📥 [SIM] Iniciando extração do ano {ano} para o estado {estado}...")

    os.makedirs("data", exist_ok=True)
    arquivo_csv = f"data/sim_campinas_{ano}.csv"
    
    if os.path.exists(arquivo_csv):
        print(f"📦 Arquivo já existente em cache local: {arquivo_csv}. Pulando download.\n")
        return

    arquivo_dbc = f"DO{estado}{ano}.dbc"
    caminho_local_dbc = f"data/{arquivo_dbc}"
    caminho_local_dbf = caminho_local_dbc.replace('.dbc', '.dbf')

    # URLs do FTP do DATASUS (DORES = Consolidados, DO = Preliminares)
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
        print(f"❌ Erro: Não foi possível encontrar a base de {ano} no FTP do DATASUS.\n")
        return

    print("   -> Lendo e filtrando o arquivo (Modo Baixo Consumo de Memória)...")
    try:
        # 1. Descompacta o .dbc para .dbf
        pyreaddbc.dbc2dbf(caminho_local_dbc, caminho_local_dbf)
        
        # 2. Abre o arquivo .dbf sem carregar tudo na memória
        table = DBF(caminho_local_dbf, encoding='iso-8859-1')
        
        registros_campinas = []
        
        # 3. Lê linha por linha e só guarda na memória se for de Campinas
        for linha in table:
            mun_res = str(linha.get('CODMUNRES', '')).strip()
            mun_ocor = str(linha.get('CODMUNOCOR', '')).strip()
            
            # Código IBGE de Campinas: 350950
            if mun_res.startswith('350950') or mun_ocor.startswith('350950'):
                registros_campinas.append(linha)
                
        # 4. Transforma apenas a amostra pequena de Campinas em DataFrame
        df_campinas = pd.DataFrame(registros_campinas)
        print(f"   -> Registros filtrados exclusivamente para Campinas: {len(df_campinas)}")
        
    except Exception as e:
        print(f"❌ Erro ao ler ou converter o arquivo .dbc: {e}\n")
        if os.path.exists(caminho_local_dbc): 
            os.remove(caminho_local_dbc)
        if os.path.exists(caminho_local_dbf): 
            os.remove(caminho_local_dbf)
        return

    if not df_campinas.empty:
        # Salvar em CSV e limpar os arquivos intermediários pesados
        df_campinas.to_csv(arquivo_csv, index=False, encoding='utf-8')
        
    if os.path.exists(caminho_local_dbc):
        os.remove(caminho_local_dbc)
    if os.path.exists(caminho_local_dbf):
        os.remove(caminho_local_dbf) # Erro de digitação corrigido aqui
        
    print(f"💾 Arquivo gerado com sucesso: {arquivo_csv}\n")


if __name__ == "__main__":
    anos_coleta = list(range(2020, 2025))
    
    print("🚀 === INICIANDO PIPELINE DE EXTRAÇÃO DIRETA (DATASUS - SIM) ===")
    for ano in anos_coleta:
        baixar_dados_sim_campinas(ano=ano)
    print("🎉 === PROCESSO DE EXTRAÇÃO CONCLUÍDO ===")