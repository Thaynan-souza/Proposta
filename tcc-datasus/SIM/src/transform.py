import os
import glob
import pandas as pd

def traduzir_idade(valor):
    valor = str(valor).strip()
    if valor in ['nan', 'None', '', '0']:
        return None
    if len(valor) == 3:
        valor = "0" + valor
    tipo = valor[0]
    try:
        if tipo == '4':
            return int(valor[1:])
        elif tipo == '5':
            return 100 + int(valor[1:])
        elif tipo in ['0', '1', '2', '3']:
            return 0
        else:
            return None
    except ValueError:
        return None

def traduzir_sexo(valor):
    val_str = str(valor).strip().replace('.0', '').upper()
    if val_str in ['1', 'M', 'MASCULINO']:
        return 'Masculino'
    elif val_str in ['2', 'F', 'FEMININO']:
        return 'Feminino'
    else:
        return 'Ignorado/Não informado'

def traduzir_raca_cor(valor):
    dicionario = {
        '1': 'Branca', '2': 'Preta', '3': 'Amarela', 
        '4': 'Parda', '5': 'Indígena'
    }
    return dicionario.get(str(valor).strip().replace('.0', ''), 'Ignorado/Sem informação')

def traduzir_escolaridade(valor):
    dicionario = {
        '0': 'Sem escolaridade',
        '1': 'Fundamental I (1ª a 4ª série)',
        '2': 'Fundamental II (5ª a 8ª série)',
        '3': 'Ensino Médio',
        '4': 'Ensino Superior Incompleto',
        '5': 'Ensino Superior Completo',
        '9': 'Ignorado'
    }
    valor_str = str(valor).strip().replace('.0', '')
    return dicionario.get(valor_str, 'Ignorado/Sem informação')

def consolidar_dados_sim():
    print("🔄 === INICIANDO PIPELINE DE TRANSFORMAÇÃO (ETL CORRIGIDO) ===")
    
    # Pega apenas os anos específicos e ignora o arquivo consolidado anterior
    arquivos_csv = [f for f in glob.glob("data/sim_campinas_*.csv") if "consolidado" not in f]
    
    if not arquivos_csv:
        print("❌ Nenhum arquivo bruto encontrado na pasta 'data/'.")
        return

    print(f"📂 Encontrados {len(arquivos_csv)} arquivos brutos anuais. Processando...")
    
    lista_dfs = []
    for arquivo in arquivos_csv:
        try:
            df_temp = pd.read_csv(arquivo, dtype=str, low_memory=False)
            df_temp.columns = [c.upper().strip() for c in df_temp.columns]
            
            df_clean_temp = pd.DataFrame()
            
            # 1. IDADE
            if 'IDADE' in df_temp.columns:
                df_clean_temp['IDADE_ANOS'] = df_temp['IDADE'].apply(traduzir_idade)
            else:
                df_clean_temp['IDADE_ANOS'] = None
                
            # 2. SEXO
            coluna_sexo = None
            for c in ['SEXO', 'TIPOSEXO']:
                if c in df_temp.columns:
                    coluna_sexo = c
                    break
                    
            if coluna_sexo:
                df_clean_temp['SEXO_NOME'] = df_temp[coluna_sexo].apply(traduzir_sexo)
            else:
                df_clean_temp['SEXO_NOME'] = 'Ignorado/Não informado'
                
            # 3. RAÇA/COR
            if 'RACACOR' in df_temp.columns:
                df_clean_temp['RACA_COR_NOME'] = df_temp['RACACOR'].apply(traduzir_raca_cor)
            else:
                df_clean_temp['RACA_COR_NOME'] = 'Ignorado/Sem informação'
                
            # 4. ESCOLARIDADE
            coluna_esc = None
            for col in ['ESC2010', 'ESC', 'ESCOLARIDADE']:
                if col in df_temp.columns:
                    coluna_esc = col
                    break
            if coluna_esc:
                df_clean_temp['ESCOLARIDADE'] = df_temp[coluna_esc].apply(traduzir_escolaridade)
            else:
                df_clean_temp['ESCOLARIDADE'] = 'Não disponível'

            # 5. DATA E ANO DO ÓBITO
            if 'DTOBITO' in df_temp.columns:
                dt_serie = pd.to_datetime(
                    df_temp['DTOBITO'].astype(str).str.zfill(8), 
                    format='%d%m%Y', 
                    errors='coerce'
                )
                df_clean_temp['DTOBITO'] = dt_serie
                df_clean_temp['ANO_OBITO'] = dt_serie.dt.year
            else:
                df_clean_temp['DTOBITO'] = pd.NaT
                df_clean_temp['ANO_OBITO'] = None

            # 6. MUNICÍPIO DE RESIDÊNCIA
            if 'CODMUNRES' in df_temp.columns:
                df_clean_temp['CODMUNRES'] = df_temp['CODMUNRES'].astype(str).str.replace(r'\.0$', '', regex=True)
            else:
                df_clean_temp['CODMUNRES'] = '350950'

            # 7. CAUSA BÁSICA
            if 'CAUSABAS' in df_temp.columns:
                df_clean_temp['CAUSABAS'] = df_temp['CAUSABAS']
            else:
                df_clean_temp['CAUSABAS'] = None

            # Remove linhas onde o ano do óbito for nulo
            df_clean_temp = df_clean_temp.dropna(subset=['ANO_OBITO'])

            lista_dfs.append(df_clean_temp)
            print(f"   -> Processado: {os.path.basename(arquivo)} ({len(df_clean_temp)} registros válidos)")

        except Exception as e:
            print(f"⚠️ Erro ao processar {arquivo}: {e}")

    if lista_dfs:
        df_consolidado = pd.concat(lista_dfs, ignore_index=True)
        caminho_saida = "data/sim_campinas_consolidado.csv"
        df_consolidado.to_csv(caminho_saida, index=False, encoding='utf-8')
        print(f"\n💾 Base unificada salva com sucesso em: {caminho_saida}")
        print(f"📊 Total de registros válidos consolidados: {len(df_consolidado)}")
    
    print("🎉 === PIPELINE FINALIZADO ===")

if __name__ == "__main__":
    consolidar_dados_sim()