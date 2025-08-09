#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

print("=== VERIFICAÇÃO COMPLETA DAS 19 DIRETORIAS ===")

# Carregar dados
with open("dados/json/dados_escolas_atualizados.json", "r", encoding="utf-8") as f:
    escolas = json.load(f)

with open(
    "dados/json/dados_veiculos_originais_corretos.json", "r", encoding="utf-8"
) as f:
    veiculos = json.load(f)

# Listar diretorias únicas das escolas
diretorias_escolas = sorted(list(set(escola["diretoria"] for escola in escolas)))

# Mapeamento de diretorias das escolas para diretorias de veículos
mapeamento = {
    "Andradina": "ADAMANTINA",
    "Apiai": "BOTUCATU",
    "Avare": "BOTUCATU",
    "Bauru": "BAURU",
    "Caraguatatuba": "CARAPICUÍBA",
    "Itapeva": "BOTUCATU",
    "Itarare": "ITARARÉ",
    "Lins": "ARARAQUARA",
    "Miracatu": "ITAPECERICA DA SERRA",
    "Mirante do Paranapanema": "PRESIDENTE PRUDENTE",
    "Norte 1": "GUARULHOS NORTE",
    "Penapolis": "ARAÇATUBA",
    "Registro": "ITAPECERICA DA SERRA",
    "Santo Anastacio": "PRESIDENTE PRUDENTE",
    "Santos": "SANTOS",
    "Sao Bernardo do Campo": "DIADEMA",
    "Sul 3": "GUARULHOS SUL",
    "SÃO VICENTE": "SANTOS",
    "Tupa": "TUPÃ",
}

print(f"📋 Total de diretorias que atendem escolas: {len(diretorias_escolas)}")
print()

com_veiculos = 0
sem_veiculos = 0
total_veiculos_relevantes = 0

diretorias_com_veiculos_list = []

for diretoria_escola in diretorias_escolas:
    # Mapear para nome da diretoria de veículos
    diretoria_veiculo = mapeamento.get(diretoria_escola, diretoria_escola.upper())

    # Buscar dados de veículos
    dados_veiculo = veiculos.get(
        diretoria_veiculo, {"total": 0, "s1": 0, "s2": 0, "s2_4x4": 0}
    )

    if dados_veiculo["total"] > 0:
        com_veiculos += 1
        total_veiculos_relevantes += dados_veiculo["total"]
        diretorias_com_veiculos_list.append(diretoria_veiculo)
        status = "✅ COM VEÍCULOS"
        detalhes = f"(S1={dados_veiculo['s1']}, S2={dados_veiculo['s2']}, S2_4x4={dados_veiculo['s2_4x4']}, Total={dados_veiculo['total']})"
    else:
        sem_veiculos += 1
        status = "❌ SEM VEÍCULOS"
        detalhes = "(0 veículos)"

    print(f"{status:15} {diretoria_escola:25} → {diretoria_veiculo:20} {detalhes}")

print()
print("📊 RESUMO FINAL:")
print(f"   🚗 Diretorias COM veículos: {com_veiculos}/{len(diretorias_escolas)}")
print(f"   ❌ Diretorias SEM veículos: {sem_veiculos}/{len(diretorias_escolas)}")
print(f"   🚐 Total de veículos relevantes: {total_veiculos_relevantes}")
print()
print("🎯 DIRETORIAS COM VEÍCULOS:")
for i, diretoria in enumerate(sorted(diretorias_com_veiculos_list), 1):
    dados = veiculos[diretoria]
    print(f"   {i:2d}. {diretoria:20} → {dados['total']} veículos")

print()
print(f"✅ RESPOSTA: Das 19 diretorias, {com_veiculos} têm veículos locados.")
