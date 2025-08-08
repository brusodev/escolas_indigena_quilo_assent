#!/usr/bin/env python3
"""
Gerar dados de veículos embebidos para o dashboard
"""

import json


def gerar_dados_embebidos():
    print("🔄 Gerando dados embebidos para o dashboard...")

    # Ler dados do JSON
    with open("dados_veiculos_diretorias.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Gerar código JavaScript
    js_code = f"""
    // DADOS DE VEÍCULOS EMBEBIDOS (atualizado automaticamente)
    const vehicleDataEmbedded = {json.dumps(data, indent=2, ensure_ascii=False)};
    """

    print("✅ Dados embebidos gerados:")
    print(f"📊 Diretorias: {len(data['diretorias'])}")
    print(f"🚗 Total veículos: {data['metadata']['total_veiculos']}")

    return js_code


if __name__ == "__main__":
    codigo = gerar_dados_embebidos()

    # Salvar em arquivo
    with open("dados_embebidos.js", "w", encoding="utf-8") as f:
        f.write(codigo)

    print("💾 Arquivo dados_embebidos.js criado!")
    print("📋 Copie e cole este código no dashboard")
