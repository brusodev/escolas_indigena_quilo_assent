#!/usr/bin/env python3
"""
Script para validar se os dados do dashboard estão corretos via servidor.
"""

import json
import os
import sys


def validar_dados_dashboard():
    """Valida se os dados JSON estão corretos e atualizados."""
    print("🔍 VALIDAÇÃO DOS DADOS DO DASHBOARD")
    print("=" * 50)

    # Verificar arquivos JSON
    base_path = os.path.dirname(os.path.dirname(__file__))

    escolas_file = os.path.join(
        base_path, 'dados', 'json', 'dados_escolas_atualizados.json')
    veiculos_file = os.path.join(base_path, 'dados_veiculos_diretorias.json')

    print(f"📁 Caminho base: {base_path}")
    print(f"📄 Arquivo escolas: {escolas_file}")
    print(f"📄 Arquivo veículos: {veiculos_file}")
    print()

    # Verificar se os arquivos existem
    if not os.path.exists(escolas_file):
        print("❌ ERRO: Arquivo de escolas não encontrado!")
        return False

    if not os.path.exists(veiculos_file):
        print("❌ ERRO: Arquivo de veículos não encontrado!")
        return False

    try:
        # Carregar dados das escolas
        with open(escolas_file, 'r', encoding='utf-8') as f:
            dados_escolas = json.load(f)

        # Carregar dados dos veículos
        with open(veiculos_file, 'r', encoding='utf-8') as f:
            dados_veiculos = json.load(f)

        print("📊 ESTATÍSTICAS DOS DADOS:")
        print("-" * 30)

        # Analisar escolas
        total_escolas = len(dados_escolas)
        escolas_indigenas = len(
            [e for e in dados_escolas if e.get('type') == 'indigena'])
        escolas_quilombolas = len(
            [e for e in dados_escolas if e.get('type') == 'quilombola'])

        print(f"🏫 Total de escolas: {total_escolas}")
        print(f"🏫 Escolas indígenas: {escolas_indigenas}")
        print(f"🏫 Escolas quilombolas: {escolas_quilombolas}")
        print()

        # Analisar veículos
        if 'diretorias' in dados_veiculos:
            diretorias_data = dados_veiculos['diretorias']
            total_veiculos = dados_veiculos.get(
                'metadata', {}).get('total_veiculos', 0)
            veiculos_com_escolas = len(
                [d for d in diretorias_data if d.get('tem_escolas', False)])
        else:
            total_veiculos = len(dados_veiculos)
            veiculos_com_escolas = len(
                [v for v in dados_veiculos if v.get('tem_escolas', False)])

        print(f"🚌 Total de veículos: {total_veiculos}")
        print(f"🚌 Veículos em diretorias com escolas: {veiculos_com_escolas}")
        print()

        # Validações específicas
        print("✅ VALIDAÇÕES:")
        print("-" * 15)

        # Validar total de escolas (deve ser 63)
        if total_escolas == 63:
            print(f"✅ Total de escolas correto: {total_escolas}")
        else:
            print(
                f"❌ Total de escolas incorreto: {total_escolas} (esperado: 63)")

        # Validar veículos em diretorias com escolas (deve ser 39)
        if veiculos_com_escolas == 39:
            print(
                f"✅ Veículos em diretorias com escolas correto: {veiculos_com_escolas}")
        else:
            print(
                f"❌ Veículos em diretorias com escolas incorreto: {veiculos_com_escolas} (esperado: 39)")

        # Validar estrutura dos dados
        escola_exemplo = dados_escolas[0] if dados_escolas else {}
        veiculo_exemplo = dados_veiculos[0] if dados_veiculos else {}

        campos_escolas_obrigatorios = [
            'name', 'type', 'lat', 'lng', 'diretoria']
        campos_veiculos_obrigatorios = [
            'nome', 'total_veiculos', 'tem_escolas']

        escolas_validas = all(
            campo in escola_exemplo for campo in campos_escolas_obrigatorios)
        veiculos_validos = all(
            campo in veiculo_exemplo for campo in campos_veiculos_obrigatorios)

        if escolas_validas:
            print("✅ Estrutura das escolas válida")
        else:
            print("❌ Estrutura das escolas inválida")
            print(f"   Campos encontrados: {list(escola_exemplo.keys())}")
            print(f"   Campos obrigatórios: {campos_escolas_obrigatorios}")

        if veiculos_validos:
            print("✅ Estrutura dos veículos válida")
        else:
            print("❌ Estrutura dos veículos inválida")
            print(f"   Campos encontrados: {list(veiculo_exemplo.keys())}")
            print(f"   Campos obrigatórios: {campos_veiculos_obrigatorios}")

        print()
        print("🎯 RESULTADO FINAL:")
        print("-" * 20)

        sucesso = (
            total_escolas == 63 and
            veiculos_com_escolas == 39 and
            escolas_validas and
            veiculos_validos
        )

        if sucesso:
            print("✅ TODOS OS DADOS ESTÃO CORRETOS!")
            print("✅ O dashboard deve mostrar os dados atualizados via servidor.")
            return True
        else:
            print("❌ PROBLEMAS ENCONTRADOS NOS DADOS!")
            print("❌ Verifique os arquivos JSON e corrija os problemas.")
            return False

    except json.JSONDecodeError as e:
        print(f"❌ ERRO: Arquivo JSON inválido - {e}")
        return False
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False


if __name__ == "__main__":
    sucesso = validar_dados_dashboard()
    sys.exit(0 if sucesso else 1)
