import os
from ftplib import FTP

def baixar_todos_meses_sia(ano=2023):
    pasta_destino = "../data/raw"
    os.makedirs(pasta_destino, exist_ok=True)
    
    print(f"\n[SIA/e-SUS] Conectando ao FTP do DATASUS para o ano de {ano}...")
    try:
        ftp = FTP('ftp.datasus.gov.br')
        ftp.login()
        ftp.cwd('/dissemin/publicos/SIASUS/200801_/Dados')
        
        ano_abrev = str(ano)[-2:]
        
        for mes in range(1, 13):
            mes_str = str(mes).zfill(2)
            # Padrão correto validado: ABOSP + Ano (2 dígitos) + Mês (2 dígitos)
            nome_arquivo = f"ABOSP{ano_abrev}{mes_str}.dbc"
            caminho_local = os.path.join(pasta_destino, nome_arquivo)
            
            # Verifica se já existe e está íntegro (> 1 KB)
            if os.path.exists(caminho_local):
                if os.path.getsize(caminho_local) > 1024:
                    print(f"  -> {nome_arquivo} já existe. Pulando...")
                    continue
                else:
                    os.remove(caminho_local)
            
            try:
                print(f"  -> Baixando {nome_arquivo}...")
                with open(caminho_local, 'wb') as f:
                    ftp.retrbinary(f'RETR {nome_arquivo}', f.write)
                print(f"     Sucesso!")
            except Exception as e:
                print(f"  -> Arquivo {nome_arquivo} não encontrado ou erro: {e}")
                if os.path.exists(caminho_local):
                    os.remove(caminho_local)
                    
        ftp.quit()
        print("\n🎉 === DOWNLOAD DE TODOS OS MESES CONCLUÍDO! ===")
        
    except Exception as e:
        print(f"❌ Erro de conexão com o FTP: {e}")

if __name__ == "__main__":
    baixar_todos_meses_sia(ano=2023)