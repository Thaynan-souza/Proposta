import os
import urllib.request
from ftplib import FTP

def baixar_dados_esus_campinas(ano, meses=range(1, 13)):
    """
    Baixa os dados de Produção Ambulatorial (PA) de São Paulo do FTP do DATASUS,
    que contém os registros do e-SUS APS.
    """
    pasta_destino = "../data/raw"
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Conectando ao FTP público do DATASUS
    ftp = FTP('ftp.datasus.gov.br')
    ftp.login()
    ftp.cwd('/dissemin/publicos/SIASUS/200801_/Dados')
    
    print(f"\n[e-SUS/SIA] Iniciando extração dos atendimentos ambulatoriais de {ano} (SP)...")
    
    ano_abrev = str(ano)[-2:]
    
    for mes in meses:
        mes_str = str(mes).zfill(2)
        # O arquivo de Produção Ambulatorial de SP tem o formato PASP + Ano (2 dígitos) + Mês (2 dígitos)
        nome_arquivo = f"PASP{ano_abrev}{mes_str}.dbc"
        caminho_local = os.path.join(pasta_destino, nome_arquivo)
        
        if os.path.exists(caminho_local):
            print(f"  -> Arquivo {nome_arquivo} já existe. Pulando...")
            continue
            
        try:
            print(f"  -> Baixando {nome_arquivo}...")
            with open(caminho_local, 'wb') as f:
                ftp.retrbinary(f'RETR {nome_arquivo}', f.write)
        except Exception as e:
            print(f"  -> Erro ao baixar {nome_arquivo}: {e}")
            
    ftp.quit()
    print(f"[e-SUS/SIA] Extração de {ano} finalizada!")

if __name__ == "__main__":
    # Vamos começar testando com o ano de 2023
    anos_coleta = [2023]
    
    print("🚀 === INICIANDO PIPELINE DE EXTRAÇÃO (e-SUS APS / SIA) === ")
    for ano in anos_coleta:
        baixar_dados_esus_campinas(ano=ano)
    print("🎉 === PROCESSO CONCLUÍDO ===")