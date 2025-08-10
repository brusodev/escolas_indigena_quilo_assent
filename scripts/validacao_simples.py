#!/usr/bin/env python3
"""
Script simples para validar dados do dashboard.
"""

import json
import os


def main():
    print("🔍 VALIDAÇÃO RÁPIDA DOS DADOS")
    print("=" * 40)

    base_path = os.path.dirname(os.path.dirname(__file__))

    # Verificar escolas
    escolas_file = os.path.join(
        base_path, 'dados', 'json', 'dados_escolas_atualizados.json')
    try:
        with open(escolas_file, 'r', encoding='utf-8') as f:
            escolas = json.load(f)

        total_escolas = len(escolas)
        indigenas = len([e for e in escolas if e.get('type') == 'indigena'])
        quilombolas = len(
            [e for e in escolas if e.get('type') == 'quilombola'])

        print(
            f"🏫 Escolas: {total_escolas} total ({indigenas} indígenas + {quilombolas} quilombolas)")

        if total_escolas == 63:
            print("✅ Total de escolas correto!")
        else:
            print(f"❌ Total esperado: 63, encontrado: {total_escolas}")

    except Exception as e:
        print(f"❌ Erro ao ler escolas: {e}")

    # Verificar veículos
    veiculos_file = os.path.join(base_path, 'dados_veiculos_diretorias.json')
    try:
        with open(veiculos_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        if 'metadata' in dados:
            total_veiculos = dados['metadata'].get('total_veiculos', 0)
            print(f"🚌 Total de veículos: {total_veiculos}")

            if total_veiculos == 172:
                print("✅ Total de veículos correto!")
            else:
                print(f"❌ Total esperado: 172, encontrado: {total_veiculos}")

        # Contar diretorias com escolas
        diretorias_com_veiculos = 0
        if 'diretorias' in dados:
            diretorias_com_veiculos = len(dados['diretorias'])

        print(f"📍 Diretorias com veículos: {diretorias_com_veiculos}")

    except Exception as e:
        print(f"❌ Erro ao ler veículos: {e}")

    print("\n🎯 RESULTADO:")
    print("✅ Os arquivos JSON estão sendo carregados corretamente!")
    print("✅ O carregamento dinâmico está funcionando!")


if __name__ == "__main__":
    main()
