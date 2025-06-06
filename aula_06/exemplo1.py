import pandas as pd
import numpy as np
from utils import limpar_nome_municipio

try:
    print('Obtendo dados...')

    # latin1, utf-8
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencia = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencia.head()) - Utilizado para testar se o .CSV foi importado.

    for i in range(2):
        df_ocorrencia['munic'] = df_ocorrencia['munic'].apply(limpar_nome_municipio)


except Exception as e:
    print(f'Erro de conexão: {e}')
    exit()

df_ocorrencia = df_ocorrencia[['munic', 'roubo_veiculo']]
# print(df_ocorrencia.head())

df_roubo_veiculo = df_ocorrencia.groupby('munic').sum(['roubo_veiculo']).reset_index()

print(df_roubo_veiculo.to_string())

# Iniciando Análise

try:
    print('Obtendo informações sobre padrão de roubo:')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])
    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo)

    print("\nMEDIDAS DE TENDÊNCIA CENTRAL")
    print(30*"=")
    print(f'Média de Roubos {media_roubo_veiculo}')
    print(f'Mediana dos Roubos {mediana_roubo_veiculo}')
    print(f'Distância entre a média e mediana: {distancia}')

    # MEDIDAS DE POSIÇÃO
    # Quartis

    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull')
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull')
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull')

    print(q1)
    print(q2)
    print(q3)

    # MUNICIPIOS COM MENOS E MAIS INDICES DE ROUBO

    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]

    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    print("\nMunicípios com menores índices de roubos")
    print(30*"=")
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

    print("\nMunicípios com maiores índices de roubos")
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

    # IDENTIFICANDO OUTLIERS (Discrepantes)

    # IQR

    iqr = q3 - q1
    print(iqr)

    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    print(("\nLimites - Medidas de Posição"))
    print(30*"=")
    print(f'Limite inferior: {limite_inferior}')
    print(f'Limite superior: {limite_superior}')

    df_roubo_veiculo_outliermaior = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    df_roubo_veiculo_outliermenor = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    if len(df_roubo_veiculo_outliermenor) == 0:  # Trata o erro caso não haja outliers 
        print('Não foram encontrados outliers inferiores')
    else:
        print(df_roubo_veiculo_outliermenor.sort_values(by='roubo_veiculo', ascending=True))

    if len(df_roubo_veiculo_outliermaior) == 0:
        print('Não foram encontrados outliers superiores')
    else:
        print(df_roubo_veiculo_outliermaior.sort_values(by='roubo_veiculo', ascending=False))
    

except Exception as e:
     print(f'Erro no processamento das medidas {e}')
