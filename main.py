import requests
import pandas as pd

# Parâmetros da API
url = "https://dados.educacao.sp.gov.br/api/3/action/datastore_search"
params = {
    "resource_id": "3bf9ac87-f5cd-42bc-b5b8-a07184ea589b",  # ID da tabela de escolas ativas
    "limit": 1000
}

# Requisição
response = requests.get(url, params=params)

# Verificação de sucesso
if response.status_code == 200:
    try:
        data = response.json()
        registros = data['result']['records']
        df = pd.DataFrame(registros)
        print(df.head())
        print(f"Total de escolas carregadas: {len(df)}")
    except Exception as e:
        print("Erro ao processar JSON:", e)
        print("Resposta bruta:", response.text)
else:
    print(f"Erro HTTP {response.status_code}")
    print("Resposta:", response.text)
