import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("\n" + "="*80)
print("Início do processamento — versões e importações")
print("pandas version:", pd.__version__)
print("="*80 + "\n")

#carregamento e limpeza dos dados

df_2010 = pd.read_csv('INMET_S_RS_A801_PORTO ALEGRE_01-01-2010_A_31-12-2010.CSV', encoding='latin1', sep=';', skiprows=8)

df_2011 = pd.read_csv('INMET_S_RS_A801_PORTO ALEGRE_01-01-2011_A_31-12-2011.CSV', encoding='latin1', sep=';', skiprows=8)

df_2012 = pd.read_csv('INMET_S_RS_A801_PORTO ALEGRE_01-01-2012_A_31-12-2012.CSV', encoding='latin1', sep=';', skiprows=8)

df = pd.concat([df_2010, df_2011, df_2012], axis=0)

print("\n" + "-"*40)
print("Após concatenação dos arquivos")
print("- info do dataframe -")
df.info()
print("- colunas (preview) -")
print(df.columns.tolist())
print("-" * 40 + "\n")

# identificação de colunas que deveriam ser inteiros mas estão como string
object_cols = df.select_dtypes(include='object').columns
print("Colunas do tipo object (amostra):", list(object_cols)[:10])

numeric_cols_to_convert = [
    'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
    'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)',
    'PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)',
    'PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)',
    'RADIACAO GLOBAL (KJ/m²)',
    'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
    'TEMPERATURA DO PONTO DE ORVALHO (°C)',
    'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)',
    'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)',
    'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)',
    'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)',
    'VENTO, RAJADA MAXIMA (m/s)',
    'VENTO, VELOCIDADE HORARIA (m/s)'
]

# transformando as strings em inteiro e lidando com dados faltantes NaM (que no dataset são '-9999')
for col in numeric_cols_to_convert:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].replace(-9999, np.nan)

# lidando com valores -9999 em colunas que já estão em inteiro
humidity_wind_cols = [
    'UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)',
    'UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)',
    'UMIDADE RELATIVA DO AR, HORARIA (%)',
    'VENTO, DIREÇÃO HORARIA (gr) (° (gr))'
]

for col in humidity_wind_cols:
    if col in df.columns:
        df[col] = df[col].replace(-9999, np.nan)

# Substitui eventualmente strings '-9999' restantes (caso existam)
df.replace('-9999', np.nan, inplace=True)

# retirando a coluna 19 ela não apresenta nome e parece ser um erro do dataset
if 'Unnamed: 19' in df.columns:
    df = df.drop(columns=['Unnamed: 19'])
    print("Removida coluna 'Unnamed: 19'")

# acrescentando indice DATETIME no lugar das colunas 'DATA (YYYY-MM-DD)' e 'HORA (UTC)'
df['DATETIME'] = pd.to_datetime(df['DATA (YYYY-MM-DD)'] + ' ' + df['HORA (UTC)'].str.replace(':', ''), format='%Y-%m-%d %H%M', errors='coerce')
df = df.set_index('DATETIME')
if 'DATA (YYYY-MM-DD)' in df.columns:
    df = df.drop(columns=['DATA (YYYY-MM-DD)'])
if 'HORA (UTC)' in df.columns:
    df = df.drop(columns=['HORA (UTC)'])

print("Index dtype:", df.index.dtype)
print("Index sample:", df.index[:3])
print("\nDataset após conversão dos valores")
df.info()

print("\n" + "-"*40)
print("Nulos por coluna antes do ffill:")
print(df.isnull().sum().sort_values(ascending=False))
print("-" * 40 + "\n")

# 'RADIACAO GLOBAL (KJ/m²)' apresentou um número muito grande de valores faltantes, por isso foi removido
if 'RADIACAO GLOBAL (KJ/m²)' in df.columns:
    df.drop('RADIACAO GLOBAL (KJ/m²)', axis=1, inplace=True)
    print(">> Coluna 'Radiacao' removida.")

# aplicando forward fill com tratamento de erro
print("\nAplicando ffill (ffill)...") 
base = df.ffill()
print("ffill aplicado com sucesso.")

print("\nNulos por coluna após ffill:")
print(base.isnull().sum().sort_values(ascending=False))

# verificando outliers nas colunas numéricas com boxplots para ter noção de quais variaveis podem ser exogenas

numeric_cols_df = base.select_dtypes(include=np.number)
numeric_columns = numeric_cols_df.columns.tolist()

num_cols_per_row = 4
num_rows = (len(numeric_columns) + num_cols_per_row - 1) // num_cols_per_row

plt.figure(figsize=(num_cols_per_row * 5, num_rows * 4))

for i, col in enumerate(numeric_columns):
    plt.subplot(num_rows, num_cols_per_row, i + 1)
    sns.boxplot(y=base[col])
    plt.title(col, fontsize=10)
    plt.ylabel('')
    plt.xticks([])

plt.tight_layout()
plt.suptitle('Boxplots para as coluna numéricas da base', y=1.02, fontsize=16)
plt.show()