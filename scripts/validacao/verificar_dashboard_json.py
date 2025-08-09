#!/usr/bin/env python3
"""
Verificar se o dashboard está usando dados atualizados
"""

import json
import os


def verificar_json_dashboard():
    print("🔍 VERIFICAÇÃO DOS DADOS DO DASHBOARD")
    print("=" * 60)

    # JSON usado pelo dashboard
    dashboard_json = "dados_veiculos_diretorias.json"

    if os.path.exists(dashboard_json):
        with open(dashboard_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"📄 Arquivo: {dashboard_json}")
        print(f"📊 Estrutura: {list(data.keys())}")

        # Verificar metadata
        if "metadata" in data:
            metadata = data["metadata"]
            print("\n📋 Metadata:")
            for key, value in metadata.items():
                print(f"   {key}: {value}")

    # Verificar arquivos com dados de escolas
    arquivos_escolas = [
        "dados_escolas_atualizados.json",
        "dados_escolas_corrigidos.json",
    ]

    print("\n🏫 DADOS DE ESCOLAS:")
    print("-" * 40)

    for arquivo in arquivos_escolas:
        if os.path.exists(arquivo):
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    data = json.load(f)

                print(f"\n📄 {arquivo}:")

                # Procurar KOPENOTI
                kopenoti_encontrado = False

                if isinstance(data, list):
                    for item in data:
                        nome = item.get("nome", item.get("Nome_Escola", ""))
                        if "KOPENOTI" in str(nome).upper():
                            distancia = item.get(
                                "distancia_km", item.get("Distancia_KM")
                            )
                            print(f"   ✅ KOPENOTI encontrado: {distancia} km")

                            if isinstance(distancia, (int, float)) and distancia < 30:
                                print("   ✅ Status: DADOS CORRETOS (Haversine)")
                            else:
                                print("   ❌ Status: DADOS ANTIGOS")
                            kopenoti_encontrado = True
                            break

                elif "escolas" in data:
                    for escola in data["escolas"]:
                        if "KOPENOTI" in str(escola.get("nome", "")).upper():
                            distancia = escola.get("distancia_km")
                            print(f"   ✅ KOPENOTI encontrado: {distancia} km")
                            kopenoti_encontrado = True
                            break

                if not kopenoti_encontrado:
                    print("   ⚠️  KOPENOTI não encontrado neste arquivo")

            except Exception as e:
                print(f"   ❌ Erro ao ler {arquivo}: {e}")
        else:
            print(f"\n❌ {arquivo} não encontrado")


if __name__ == "__main__":
    verificar_json_dashboard()
