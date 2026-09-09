import os
import pandas as pd
import requests

# Novos códigos dos Agregados para o Censo de 2022
tabelas_sidra = {
    "tabela_4714_populacao": "4714",
    "tabela_6805_esgoto": "6805",
    "tabela_6803_agua": "6803",
    "tabela_10295_renda": "10295"
}

def extrair_e_salvar_tabelas():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, '../data/raw')
    os.makedirs(output_dir, exist_ok=True)

    for nome_arquivo, tabela_id in tabelas_sidra.items():
        # Nova rota oficial gerada pelo Query Builder do IBGE
        # Ao não especificar um ID após /variaveis, a API traz todas as variáveis padrão.
        url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{tabela_id}/periodos/2022/variaveis?localidades=N6[N3[35]]"
        
        print(f"Baixando dados do Agregado {tabela_id} ({nome_arquivo})...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            dados = response.json()
            registros = []
            
            for serie in dados:
                nome_variavel = serie.get('variavel', 'Valor') 
                
                resultados = serie.get('resultados', [])
                for resultado in resultados:
                    classificacoes = resultado.get('classificacoes', [])
                    series_dados = resultado.get('series', [])
                    
                    for s in series_dados:
                        localidade = s.get('localidade', {})
                        id_municipio = localidade.get('id')
                        nome_municipio = localidade.get('nome')
                        
                        for periodo, valor in s.get('serie', {}).items():
                            registro = {
                                'id_municipio': id_municipio,
                                'municipio': nome_municipio,
                                'variavel': nome_variavel, 
                                'ano': periodo,
                                'valor': valor
                            }
                            
                            for c in classificacoes:
                                categoria_dict = c.get('categoria', {})
                                cat_nome = list(categoria_dict.values())[0] if categoria_dict else 'Total'
                                sub_nome = c.get('nome', '')
                                registro[sub_nome] = cat_nome
                                
                            registros.append(registro)
            
            if registros:
                df = pd.DataFrame(registros)
                caminho_csv = os.path.join(output_dir, f"{nome_arquivo}.csv")
                df.to_csv(caminho_csv, index=False, sep=';', encoding='utf-8-sig')
                print(f"✅ Salvo com sucesso: {caminho_csv}\n")
            else:
                print(f"⚠️ Nenhum registro processado para {tabela_id}.\n")
        else:
            print(f"❌ Erro no Agregado {tabela_id}. Status: {response.status_code}\n")

if __name__ == "__main__":
    extrair_e_salvar_tabelas()