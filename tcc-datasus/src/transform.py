import os
import glob
import pandas as pd

def traduzir_idade(valor):
    """
    Decodifica o formato de idade do DATASUS.
    O primeiro dígito indica a unidade de medida:
    1 a 3 = Minutos, Horas, Meses (vamos agrupar como 0 anos / menor de 1 ano)
    4 = Anos (ex: 4050 -> 50 anos)
    5 = Mais de 100 anos (ex: 5010 -> 110 anos)
    """
    valor = str(valor).strip()
    if valor in ['nan', 'None', '', '0']:
        return None
        
    # Preenche com zero à esquerda se vier quebrado (ex: 450 -> 0450)
    if len(valor) == 3:
        valor = "0" + valor
        
    tipo = valor[0]
    try:
        if tipo == '4':
            return int(valor[1:])
        elif tipo == '5':
            return 100 + int(valor[1:])
        elif tipo in ['0', '1', '2', '3']:
            return 0  # Menores de 1 ano
        else:
            return None
    except ValueError:
        return None

def traduzir_sexo(valor):
    dicionario = {'1': 'Masculino', '2': 'Feminino'}
    return dicionario.get(str(valor).strip(), 'Ignorado')

def traduzir_raca_cor(valor):
    dicionario = {
        '1': 'Branca', '2': 'Preta', '3': 'Amarela', 
        '4': 'Parda', '5': 'Indígena'
    }
    return dicionario.get(str(valor).strip(), 'Ignorado/Sem informação')

def traduzir_escolaridade(valor):
    # Baseado no campo ESC2010 do SIM
    dicionario = {
        '0': 'Sem escolaridade',
        '1': 'Fundamental I (1ª a 4ª série)',
        '2': 'Fundamental II (5ª a 8ª série)',
        '3': 'Ensino Médio',
        '4': 'Ensino Superior Incompleto',
        '5': 'Ensino Superior Completo'
    }
    return dicionario.get(str(valor).strip(), 'Ignorado/Sem informação')

def consolidar_dados_sim():
    print("🔄 === INICIANDO PIPELINE DE TRANSFORMAÇÃO (ETL) ===")
    
    # 1. Carregar todos os CSVs gerados na fase de extração
    arquivos_csv = glob.glob("data/sim_campinas_*.csv")
    
    if not arquivos_csv:
        print("❌ Nenhum arquivo encontrado na pasta 'data/'. Rode o extract.py primeiro.")
        return

    print(f"📂 Encontrados {len(arquivos_csv)} arquivos. Iniciando consolidação...")
    
    lista_dfs = []
    for arquivo in arquivos_csv:
        try:
            # Força a leitura do CEP como string para não perder o zero à esquerda
            df_temp = pd.read_csv(arquivo, dtype={'CEP': str})
            lista_dfs.append(df_temp)
        except Exception as e:
            print(f"⚠️ Erro ao ler o arquivo {arquivo}: {e}")

    df_consolidado = pd.concat(lista_dfs, ignore_index=True)
    total_linhas_original = len(df_consolidado)
    print(f"📊 Total de registros brutos consolidados: {total_linhas_original}")

    # 2. Filtrar colunas de interesse para o projeto
    colunas_interesse = [
        'DTOBITO', 'CAUSABAS', 'IDADE', 'SEXO', 'RACACOR', 'ESC2010', 'CEP'
    ]
    
    # Mantém apenas as colunas que realmente existem no DataFrame
    colunas_presentes = [col for col in colunas_interesse if col in df_consolidado.columns]
    df_clean = df_consolidado[colunas_presentes].copy()

    # 3. Aplicar as traduções (Limpeza de Dados)
    print("🧹 Traduzindo códigos do DATASUS para formato legível...")
    
    if 'IDADE' in df_clean.columns:
        df_clean['IDADE_ANOS'] = df_clean['IDADE'].apply(traduzir_idade)
        
    if 'SEXO' in df_clean.columns:
        df_clean['SEXO_NOME'] = df_clean['SEXO'].apply(traduzir_sexo)
        
    if 'RACACOR' in df_clean.columns:
        df_clean['RACA_COR_NOME'] = df_clean['RACACOR'].apply(traduzir_raca_cor)
        
    if 'ESC2010' in df_clean.columns:
        df_clean['ESCOLARIDADE'] = df_clean['ESC2010'].apply(traduzir_escolaridade)

    # 4. Formatar a Data do Óbito
    if 'DTOBITO' in df_clean.columns:
        # DATASUS salva como DDMMAAAA
        df_clean['DTOBITO'] = pd.to_datetime(
            df_clean['DTOBITO'].astype(str).str.zfill(8), 
            format='%d%m%Y', 
            errors='coerce'
        )
        df_clean['ANO_OBITO'] = df_clean['DTOBITO'].dt.year

    # 5. Tratamento básico do CEP (fundamental para a análise espacial depois)
    if 'CEP' in df_clean.columns:
        df_clean['CEP'] = df_clean['CEP'].astype(str).str.replace(r'\.0$', '', regex=True)
        # Remove valores que não parecem CEPs válidos (menor que 8 dígitos)
        df_clean.loc[df_clean['CEP'].str.len() < 8, 'CEP'] = 'Sem CEP'

    # Removemos as colunas originais que já foram traduzidas para manter o arquivo leve
    colunas_para_remover = ['IDADE', 'SEXO', 'RACACOR', 'ESC2010']
    df_clean.drop(columns=[col for col in colunas_para_remover if col in df_clean.columns], inplace=True)

    # 6. Salvar o arquivo final consolidado
    caminho_saida = "data/sim_campinas_consolidado.csv"
    df_clean.to_csv(caminho_saida, index=False, encoding='utf-8')
    
    print(f"💾 Transformação concluída! Base unificada salva em: {caminho_saida}")
    print("🎉 === PIPELINE DE TRANSFORMAÇÃO FINALIZADO ===")

if __name__ == "__main__":
    consolidar_dados_sim()