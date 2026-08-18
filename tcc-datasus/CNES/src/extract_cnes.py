import os
import pandas as pd

def criar_bruto_vazio():
    print("=== EXTRATOR BRUTO CNES: APENAS ESTRUTURA (SEM LINHAS FICTÍCIAS) ===")
    
    ano = 2024
    raw_dir = f"CNES/data/raw/{ano}"
    os.makedirs(raw_dir, exist_ok=True)
    
    arquivo_bruto_path = os.path.join(raw_dir, f"cnes_sp_{ano}_bruto.csv")
    
    # Definindo apenas as colunas oficiais brutas do DATASUS (sem dados inventados)
    colunas_oficiais_cnes = [
        "CODUFMUN", "MUNICIPIO", "CNES", "ESTABELECIMENTO", 
        "BAIRRO", "TIPO_UNIDADE", "LEITOS", "ESFERA", "SUS"
    ]
    
    # Cria um DataFrame vazio apenas com o cabeçalho
    df_vazio = pd.DataFrame(columns=colunas_oficiais_cnes)
    df_vazio.to_csv(arquivo_bruto_path, index=False, encoding="utf-8")
    
    print(f"-> Arquivo bruto estruturado e limpo gerado em: {arquivo_bruto_path}")
    print(f"-> Pronto para receber a base oficial integral.")

if __name__ == "__main__":
    criar_bruto_vazio()