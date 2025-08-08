#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir incompatibilidades de nomes entre escolas e dados de veículos
"""

import json
import re
import unicodedata


def remover_acentos(texto):
    """Remove acentos de um texto"""
    return unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')


def normalizar_nome_diretoria(nome):
    """Normaliza nome de diretoria para compatibilidade"""
    # Remover acentos
    nome_sem_acentos = remover_acentos(nome)
    # Converter para maiúsculas
    nome_upper = nome_sem_acentos.upper()
    # Remover espaços extras
    nome_limpo = nome_upper.strip()
    return nome_limpo


def corrigir_incompatibilidades():
    """Corrige incompatibilidades entre nomes de diretorias"""
    print("🔧 CORRIGINDO INCOMPATIBILIDADES DE NOMES...")
    print("=" * 60)

    # 1. Carregar dados atuais
    print("📂 Carregando dados atuais...")

    with open("dados_veiculos_atualizados.json", "r", encoding="utf-8") as f:
        veiculos_dados = json.load(f)

    with open("dados_escolas_atualizados.json", "r", encoding="utf-8") as f:
        escolas_dados = json.load(f)

    print(f"   ✅ {len(veiculos_dados)} diretorias de veículos")
    print(f"   ✅ {len(escolas_dados)} escolas")

    # 2. Analisar incompatibilidades
    print("\n🔍 ANALISANDO INCOMPATIBILIDADES...")

    # Diretorias únicas nas escolas
    diretorias_escolas = set()
    for escola in escolas_dados:
        diretorias_escolas.add(escola.get('diretoria', ''))

    # Diretorias nos dados de veículos
    diretorias_veiculos = set(veiculos_dados.keys())

    print(f"   📊 Diretorias únicas nas escolas: {len(diretorias_escolas)}")
    print(f"   📊 Diretorias nos dados de veículos: {len(diretorias_veiculos)}")

    # Encontrar incompatibilidades
    problemas = []
    for diretoria_escola in diretorias_escolas:
        diretoria_normalizada = normalizar_nome_diretoria(diretoria_escola)

        if diretoria_normalizada not in diretorias_veiculos:
            # Tentar encontrar correspondência aproximada
            correspondencia = None
            for diretoria_veiculo in diretorias_veiculos:
                if remover_acentos(diretoria_veiculo.lower()) == remover_acentos(diretoria_escola.lower()):
                    correspondencia = diretoria_veiculo
                    break

            problemas.append({
                'escola': diretoria_escola,
                'normalizada': diretoria_normalizada,
                'correspondencia': correspondencia
            })

    print(f"\n❌ INCOMPATIBILIDADES ENCONTRADAS: {len(problemas)}")
    for problema in problemas:
        print(
            f"   🔸 Escola: '{problema['escola']}' → Normalizada: '{problema['normalizada']}'")
        if problema['correspondencia']:
            print(
                f"      ✅ Correspondência encontrada: '{problema['correspondencia']}'")
        else:
            print(f"      ❌ Sem correspondência nos dados de veículos")

    # 3. Criar mapeamento corrigido
    print("\n🔧 CRIANDO DADOS CORRIGIDOS...")

    # Criar novo dicionário de veículos com chaves normalizadas
    veiculos_corrigidos = {}

    for chave_original, dados in veiculos_dados.items():
        # Manter chave original
        veiculos_corrigidos[chave_original] = dados

        # Adicionar chave normalizada se diferente
        chave_normalizada = normalizar_nome_diretoria(chave_original)
        if chave_normalizada != chave_original:
            veiculos_corrigidos[chave_normalizada] = dados

    # Para cada problema, criar entrada adicional
    for problema in problemas:
        if problema['correspondencia']:
            dados_correspondencia = veiculos_dados[problema['correspondencia']]
            veiculos_corrigidos[problema['normalizada']
                                ] = dados_correspondencia

            # Também adicionar a versão original da escola
            escola_upper = problema['escola'].upper()
            if escola_upper not in veiculos_corrigidos:
                veiculos_corrigidos[escola_upper] = dados_correspondencia

    print(
        f"   ✅ Dados de veículos expandidos: {len(veiculos_dados)} → {len(veiculos_corrigidos)} entradas")

    # 4. Atualizar dados de escolas para usar nomes consistentes
    print("\n📝 ATUALIZANDO DADOS DE ESCOLAS...")

    escolas_corrigidas = []
    escolas_alteradas = 0

    for escola in escolas_dados:
        escola_corrigida = escola.copy()
        diretoria_original = escola.get('diretoria', '')
        diretoria_normalizada = normalizar_nome_diretoria(diretoria_original)

        # Verificar se precisa de correção
        if diretoria_normalizada in veiculos_corrigidos:
            if diretoria_original != diretoria_normalizada:
                escola_corrigida['diretoria'] = diretoria_normalizada
                escola_corrigida['diretoria_original'] = diretoria_original
                escolas_alteradas += 1

        escolas_corrigidas.append(escola_corrigida)

    print(f"   ✅ Escolas com nomes corrigidos: {escolas_alteradas}")

    # 5. Salvar dados corrigidos
    print("\n💾 SALVANDO DADOS CORRIGIDOS...")

    with open("dados_veiculos_corrigidos.json", "w", encoding="utf-8") as f:
        json.dump(veiculos_corrigidos, f, ensure_ascii=False, indent=2)

    with open("dados_escolas_corrigidos.json", "w", encoding="utf-8") as f:
        json.dump(escolas_corrigidas, f, ensure_ascii=False, indent=2)

    print(f"   ✅ dados_veiculos_corrigidos.json")
    print(f"   ✅ dados_escolas_corrigidos.json")

    # 6. Gerar relatório de correções
    print(f"\n📋 RELATÓRIO DE CORREÇÕES:")
    print("=" * 50)

    print(f"🔧 Correções aplicadas:")
    print(
        f"   • Dados de veículos: {len(veiculos_dados)} → {len(veiculos_corrigidos)} entradas")
    print(f"   • Escolas com nomes corrigidos: {escolas_alteradas}")
    print(
        f"   • Incompatibilidades resolvidas: {len([p for p in problemas if p['correspondencia']])}")

    # Verificar se ainda há problemas
    problemas_restantes = []
    for escola in escolas_corrigidas:
        diretoria = escola.get('diretoria', '').upper()
        if diretoria not in veiculos_corrigidos:
            problemas_restantes.append(diretoria)

    if problemas_restantes:
        print(f"\n⚠️  PROBLEMAS RESTANTES ({len(set(problemas_restantes))}):")
        for problema in set(problemas_restantes):
            print(f"   • {problema}")
    else:
        print(f"\n✅ TODAS AS INCOMPATIBILIDADES RESOLVIDAS!")

    return veiculos_corrigidos, escolas_corrigidas


def atualizar_dashboard_com_dados_corrigidos():
    """Atualiza o dashboard com os dados corrigidos"""
    print(f"\n🎨 ATUALIZANDO DASHBOARD COM DADOS CORRIGIDOS...")

    try:
        # Usar os dados normalizados da planilha que têm 172 veículos
        with open("dados_veiculos_normalizados.json", "r", encoding="utf-8") as f:
            veiculos_normalizados = json.load(f)

        print(
            f"   📊 Usando dados normalizados: {sum(v['total'] for v in veiculos_normalizados.values())} veículos")

        # Aplicar correção usando o script corrigido
        import subprocess
        import sys

        # Substituir os dados atualizados pelos normalizados
        with open("dados_veiculos_atualizados.json", "w", encoding="utf-8") as f:
            json.dump(veiculos_normalizados, f, ensure_ascii=False, indent=2)

        result = subprocess.run([sys.executable, "atualizar_dashboard_corrigido.py"],
                                capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            print("   ✅ Dashboard atualizado com dados corrigidos!")
            print(result.stdout)
        else:
            print(f"   ⚠️  Problemas na atualização: {result.stderr}")

    except Exception as e:
        print(f"   ❌ Erro na atualização: {e}")


if __name__ == "__main__":
    veiculos_corrigidos, escolas_corrigidas = corrigir_incompatibilidades()
    atualizar_dashboard_com_dados_corrigidos()
    print(f"\n✅ CORREÇÃO DE INCOMPATIBILIDADES CONCLUÍDA!")
