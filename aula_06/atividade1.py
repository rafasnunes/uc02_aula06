import pandas as pd
import numpy as np
from utils import limpar_nome_municipio

# OBTENDO OS DADOS

try:
    print('Obtendo dados...')

    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencia = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    for i in range(2):

        df_ocorrencia['munic'] = df_ocorrencia['munic'].apply(limpar_nome_municipio)

except Exception as e:
    print(f'Erro de conexão: {e}')
    exit()

df_ocorrencia = df_ocorrencia[['munic', 'estelionato']]

df_estelionato = df_ocorrencia.groupby('munic').sum(['estelionato']).reset_index()

print(df_estelionato.to_string())

# Iniciando Análise

try:
    print('Obtendo informações sobre padrão de estelionato:')
    array_estelionato = np.array(df_estelionato['estelionato'])
    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)
    distancia = abs((media_estelionato - mediana_estelionato) / mediana_estelionato)

    print("\nMEDIDAS DE TENDENCIA CENTRAL")
    print(30*"=")
    print(f'Média de Estelionatos: {media_estelionato}')
    print(f'Mediana de Estelionatos: {mediana_estelionato}')
    print(f'Distância entre a média e a mediana: {distancia}')

    # Medidas de Posição
    # Quartis

    q1 = np.quantile(array_estelionato, 0.25, method='weibull')
    q1 = np.quantile(array_estelionato, 0.50, method='weibull')
    q1 = np.quantile(array_estelionato, 0.75, method='weibull')



except Exception as e:
    print(f'Erro no processamento das medidas {e}')