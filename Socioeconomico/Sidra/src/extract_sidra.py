import pandas as pd
import requests
import os
import json

def extrair_dados_renda_sidra():
    print("Extraindo dados de rendimento por Distritos do SIDRA (IBGE)...")
    
    # Tabela 1378 (Censo Universo): Rendimento nominal médio dos responsáveis
    # N10[in]3509502: Traz os dados dos 5 Distritos de Campinas
    url = "https://servicodados.ibge.gov.br/api/v3/agregados/1378/periodos/2010?localidades=N10[in]3509502"
    
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        print("✅ Dados obtidos com sucesso da API do SIDRA!")
        
        pasta_raw = "../data/raw"
        os.makedirs(pasta_raw, exist_ok=True)
        
        caminho_arquivo = os.path.join(pasta_raw, "sidra_renda_distritos_campinas.json")
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
            
        print(f"Arquivo bruto salvo em: {caminho_arquivo}")
    else:
        print(f"❌ Erro ao acessar a API do SIDRA: {resposta.status_code}")

if __name__ == "__main__":
    extrair_dados_renda_sidra()