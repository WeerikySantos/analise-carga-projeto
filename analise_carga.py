import requests
import matplotlib.pyplot as plt

# Defina os parâmetros da requisição
data_inicio = '2024-01-01'
data_fim = '2024-12-31'
codigo_area_carga = 'SECO'

# Construa a URL da requisição
url = f'https://apicarga.ons.org.br/prd/cargaverificada?dat_inicio={data_inicio}&dat_fim={data_fim}&cod_areacarga={codigo_area_carga}'

# Faça a requisição GET
response = requests.get(url)

# Verifique se a requisição foi bem-sucedida (código 200)
if response.status_code == 200:
    # Converta a resposta para JSON
    data = response.json()

    # Dicionário para armazenar as médias por estação e ano
    medias_por_estacao_ano = {}

    # Função para determinar a estação
    def determinar_estacao(data_referencia):
        mes = int(data_referencia.split('-')[1])  # Extrai o mês da data de referência
        if mes in [12, 1, 2]:
            return "Verão"
        elif mes in [3, 4, 5]:
            return "Outono"
        elif mes in [6, 7, 8]:
            return "Inverno"
        else:
            return "Primavera"

    # Função para determinar o ano
    def determinar_ano(data_referencia):
        return int(data_referencia.split('-')[0])

    # Iterar sobre os itens do JSON
    for item in data:
        data_referencia = item['dat_referencia']
        carga_global = item['val_cargaglobal']
        
        estacao = determinar_estacao(data_referencia)
        ano = determinar_ano(data_referencia)
        
        if estacao not in medias_por_estacao_ano:
            medias_por_estacao_ano[estacao] = {}
        if ano not in medias_por_estacao_ano[estacao]:
            medias_por_estacao_ano[estacao][ano] = {'soma': 0, 'contagem': 0}
        
        medias_por_estacao_ano[estacao][ano]['soma'] += carga_global
        medias_por_estacao_ano[estacao][ano]['contagem'] += 1

    # Plotagem do gráfico
    for estacao, medias in medias_por_estacao_ano.items():
        anos = list(medias.keys())
        valores = [medias[ano]['soma'] / medias[ano]['contagem'] for ano in anos]
        plt.plot(anos, valores, label=estacao)
        
    # Personalização do gráfico
    plt.title('Médias de Carga Global por Estação ao Longo dos Anos')
    plt.xlabel('Ano')
    plt.ylabel('Média de Carga Global')
    plt.legend()
    plt.grid(True)

    # Exibição do gráfico
    plt.show()

else:
    print('Erro ao acessar a API:', response.status_code)
