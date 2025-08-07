import pandas as pd

# Criar arquivo de veículos de exemplo
dados_veiculos = [
    {
        "DIRETORIA": "CENTRO",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 1,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "CENTRO OESTE",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 1,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "NORTE 1",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 1,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "NORTE 2",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 1,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "LESTE 1",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 1,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "LESTE 2",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 1,
        "QUANTIDADE S-2 4X4": 0,
    },
    # Adicionar todas as diretorias do sistema (algumas com 0 veículos)
    {
        "DIRETORIA": "ANDRADINA",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 0,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "AVARE",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 0,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "BAURU",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 0,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "CARAGUATATUBA",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 0,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "ITAPEVA",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 0,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "ITARARE",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 0,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "LINS",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 0,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "MIRACATU",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 0,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "MIRANTE DO PARANAPANEMA",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 0,
        "QUANTIDADE S-2 4X4": 0,
    },
    {
        "DIRETORIA": "SANTO ANASTACIO",
        "QUANTIDADE S-1": 0,
        "QUANTIDADE S-2": 0,
        "QUANTIDADE S-2 4X4": 0,
    },
]

df_veiculos = pd.DataFrame(dados_veiculos)

# Criar arquivo de supervisão de exemplo
dados_gep = [
    {
        "REGIÃO": "CAPITAL",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "CENTRO",
        "QUANTIDADE DE DEs": 5,
        "SUPERVISOR GEP": "João Silva",
    },
    {
        "REGIÃO": "CAPITAL",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "CENTRO OESTE",
        "QUANTIDADE DE DEs": 4,
        "SUPERVISOR GEP": "João Silva",
    },
    {
        "REGIÃO": "CAPITAL",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "NORTE 1",
        "QUANTIDADE DE DEs": 3,
        "SUPERVISOR GEP": "Maria Santos",
    },
    {
        "REGIÃO": "CAPITAL",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "NORTE 2",
        "QUANTIDADE DE DEs": 3,
        "SUPERVISOR GEP": "Maria Santos",
    },
    {
        "REGIÃO": "CAPITAL",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "LESTE 1",
        "QUANTIDADE DE DEs": 4,
        "SUPERVISOR GEP": "Carlos Oliveira",
    },
    {
        "REGIÃO": "CAPITAL",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "LESTE 2",
        "QUANTIDADE DE DEs": 4,
        "SUPERVISOR GEP": "Carlos Oliveira",
    },
    {
        "REGIÃO": "INTERIOR",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "ANDRADINA",
        "QUANTIDADE DE DEs": 2,
        "SUPERVISOR GEP": "Ana Costa",
    },
    {
        "REGIÃO": "INTERIOR",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "AVARE",
        "QUANTIDADE DE DEs": 3,
        "SUPERVISOR GEP": "Ana Costa",
    },
    {
        "REGIÃO": "INTERIOR",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "BAURU",
        "QUANTIDADE DE DEs": 4,
        "SUPERVISOR GEP": "Pedro Lima",
    },
    {
        "REGIÃO": "LITORAL",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "CARAGUATATUBA",
        "QUANTIDADE DE DEs": 2,
        "SUPERVISOR GEP": "Lucia Fernandes",
    },
    {
        "REGIÃO": "INTERIOR",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "ITAPEVA",
        "QUANTIDADE DE DEs": 1,
        "SUPERVISOR GEP": "Roberto Souza",
    },
    {
        "REGIÃO": "INTERIOR",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "ITARARE",
        "QUANTIDADE DE DEs": 1,
        "SUPERVISOR GEP": "Roberto Souza",
    },
    {
        "REGIÃO": "INTERIOR",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "LINS",
        "QUANTIDADE DE DEs": 2,
        "SUPERVISOR GEP": "Ana Costa",
    },
    {
        "REGIÃO": "LITORAL",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "MIRACATU",
        "QUANTIDADE DE DEs": 1,
        "SUPERVISOR GEP": "Lucia Fernandes",
    },
    {
        "REGIÃO": "INTERIOR",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "MIRANTE DO PARANAPANEMA",
        "QUANTIDADE DE DEs": 2,
        "SUPERVISOR GEP": "Roberto Souza",
    },
    {
        "REGIÃO": "INTERIOR",
        "DIRETORIA DE ENSINO SOB SUPERVISÃO": "SANTO ANASTACIO",
        "QUANTIDADE DE DEs": 1,
        "SUPERVISOR GEP": "Roberto Souza",
    },
]

df_gep = pd.DataFrame(dados_gep)

# Salvar os arquivos
df_veiculos.to_excel("QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx", index=False)
df_gep.to_excel("GEP.xlsx", index=False)

print("✅ Arquivos de exemplo criados:")
print("📁 QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx")
print("📁 GEP.xlsx")
print("\n📊 Exemplo de dados de veículos:")
print(df_veiculos.head().to_string())
print("\n👥 Exemplo de dados de supervisão:")
print(df_gep.head().to_string())
