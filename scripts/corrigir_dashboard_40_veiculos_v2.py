#!/usr/bin/env python3
"""
Script para corrigir veículos do dashboard
Atualizado para a estrutura correta dos dados JSON
"""

import json
import os
import shutil
from datetime import datetime


def fazer_backup():
    """Faz backup dos arquivos que serão alterados"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"dados/json/old/backup_correcao_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)

    arquivos_backup = [
        'static/js/dash.js',
        'dados/json/estatisticas_atualizadas.json',
        'README.md'
    ]

    print("🛡️ Fazendo backup dos arquivos...")
    for arquivo in arquivos_backup:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, backup_dir)
            print(f"✅ Backup: {arquivo}")

    print(f"🛡️ Backup completo em: {backup_dir}")
    return backup_dir


def calcular_veiculos_corretos():
    """Calcula dados corretos baseado nos arquivos JSON com estrutura real"""
    try:
        # Carregar dados de escolas (estrutura real)
        with open('dados/json/dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
            escolas = json.load(f)

        # Verificar a estrutura real dos dados
        print(f"📊 Total de escolas: {len(escolas)}")
        if escolas:
            print(f"🔍 Campos disponíveis: {list(escolas[0].keys())}")

        # Contar por tipo usando a estrutura real
        tipos = {}
        diretorias_com_escolas = set()

        for escola in escolas:
            # Usar 'type' que é o campo real
            tipo = escola.get('type', 'Desconhecido')
            if tipo not in tipos:
                tipos[tipo] = 0
            tipos[tipo] += 1

            # Usar 'diretoria' que é o campo real
            diretorias_com_escolas.add(escola.get('diretoria', ''))

        print(f"📝 Tipos encontrados: {tipos}")
        print(f"📍 Diretorias com escolas: {len(diretorias_com_escolas)}")

        # Carregar dados de veículos
        with open('dados/json/dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
            veiculos_data = json.load(f)

        # Contar veículos apenas das diretorias que atendem escolas
        total_veiculos = 0
        diretorias_atendidas = 0
        detalhamento = {}

        print("\n📋 Detalhamento por diretoria:")
        for diretoria_nome in sorted(diretorias_com_escolas):
            if not diretoria_nome:  # Pular valores vazios
                continue

            # Tentar diferentes variações do nome
            nome_upper = diretoria_nome.upper()
            encontrada = False

            for key in veiculos_data['diretorias'].keys():
                if key.upper() == nome_upper:
                    veiculos_dir = veiculos_data['diretorias'][key]['total']
                    total_veiculos += veiculos_dir
                    diretorias_atendidas += 1
                    detalhamento[diretoria_nome] = veiculos_dir
                    print(f"   ✅ {diretoria_nome}: {veiculos_dir} veículos")
                    encontrada = True
                    break

            if not encontrada:
                print(f"   ❌ {diretoria_nome}: NÃO ENCONTRADA")

        print(f"\n🎯 RESULTADO:")
        print(f"   • Total de escolas: {len(escolas)}")
        print(f"   • Indígenas: {tipos.get('indigena', 0)}")
        print(f"   • Quilombolas: {tipos.get('quilombola', 0)}")
        print(f"   • Diretorias atendidas: {diretorias_atendidas}")
        print(f"   • TOTAL DE VEÍCULOS: {total_veiculos}")

        return {
            'total_escolas': len(escolas),
            'total_veiculos': total_veiculos,
            'total_diretorias': diretorias_atendidas,
            'tipos_escola': tipos,
            'diretorias_com_escolas': list(diretorias_com_escolas),
            'detalhamento_veiculos': detalhamento
        }

    except Exception as e:
        print(f"❌ Erro ao calcular veículos: {e}")
        import traceback
        traceback.print_exc()
        return None


def corrigir_dashboard_js(total_veiculos):
    """Corrige o arquivo dash.js para mostrar o número correto de veículos"""
    print(
        f"\n🔧 Corrigindo dashboard para mostrar {total_veiculos} veículos...")

    try:
        with open('static/js/dash.js', 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # Buscar padrões que definem o total de veículos
        import re

        # Padrão para encontrar linhas como: totalVehicles: 6
        padrao_total = re.compile(r'totalVehicles:\s*(\d+)', re.IGNORECASE)
        matches = padrao_total.findall(conteudo)

        if matches:
            for match in matches:
                valor_antigo = match
                linha_antiga = f"totalVehicles: {valor_antigo}"
                linha_nova = f"totalVehicles: {total_veiculos} // CORRIGIDO de {valor_antigo}"
                conteudo = conteudo.replace(linha_antiga, linha_nova)
                print(
                    f"✅ Corrigido: {linha_antiga} → totalVehicles: {total_veiculos}")

        # Também buscar outros padrões possíveis
        outros_padroes = [
            (r'vehicles:\s*(\d+)', f'vehicles: {total_veiculos}'),
            (r'totalVehicles\s*=\s*(\d+)',
             f'totalVehicles = {total_veiculos}'),
            (r'veiculos:\s*(\d+)', f'veiculos: {total_veiculos}')
        ]

        for padrao, substituicao in outros_padroes:
            conteudo = re.sub(padrao, substituicao,
                              conteudo, flags=re.IGNORECASE)

        # Salvar arquivo corrigido
        with open('static/js/dash.js', 'w', encoding='utf-8') as f:
            f.write(conteudo)

        print(f"✅ Dashboard JavaScript atualizado")
        return True

    except Exception as e:
        print(f"❌ Erro ao corrigir dashboard: {e}")
        return False


def criar_estatisticas_atualizadas(dados):
    """Cria arquivo de estatísticas com dados corretos"""
    print("\n📈 Criando estatísticas atualizadas...")

    try:
        estatisticas = {
            "ultima_atualizacao": datetime.now().isoformat(),
            "resumo": {
                "total_escolas": dados['total_escolas'],
                "total_veiculos_diretorias_relevantes": dados['total_veiculos'],
                "total_diretorias_atendendo_escolas": dados['total_diretorias'],
                "tipos_escola": dados['tipos_escola']
            },
            "detalhamento": dados['detalhamento_veiculos'],
            "observacoes": [
                f"Dados corrigidos automaticamente em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Dashboard atualizado para mostrar {dados['total_veiculos']} veículos",
                "Contagem considera apenas diretorias que atendem escolas indígenas/quilombolas"
            ]
        }

        with open('dados/json/estatisticas_atualizadas.json', 'w', encoding='utf-8') as f:
            json.dump(estatisticas, f, indent=2, ensure_ascii=False)

        print("✅ Estatísticas atualizadas criadas")
        return True

    except Exception as e:
        print(f"❌ Erro ao criar estatísticas: {e}")
        return False


def atualizar_readme(dados):
    """Atualiza README.md com dados corretos"""
    print("\n📝 Atualizando README...")

    try:
        # Ler README atual
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()

        # Substituir valores incorretos
        substituicoes = [
            ('6 veículos', f"{dados['total_veiculos']} veículos"),
            ('6 Veículos', f"{dados['total_veiculos']} Veículos"),
            ('total: 6', f"total: {dados['total_veiculos']}"),
        ]

        for antigo, novo in substituicoes:
            if antigo in readme:
                readme = readme.replace(antigo, novo)
                print(f"✅ README: {antigo} → {novo}")

        # Salvar README atualizado
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme)

        print("✅ README atualizado")
        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar README: {e}")
        return False


def validar_correcoes():
    """Valida se as correções foram aplicadas corretamente"""
    print("\n🔍 Validando correções...")

    validacoes = []

    # Verificar se o dashboard foi corrigido
    try:
        with open('static/js/dash.js', 'r', encoding='utf-8') as f:
            js_content = f.read()

        if 'totalVehicles: 40' in js_content or 'totalVehicles = 40' in js_content:
            validacoes.append("✅ Dashboard JavaScript corrigido")
        else:
            validacoes.append("❌ Dashboard JavaScript não foi corrigido")
    except:
        validacoes.append("❌ Erro ao verificar dashboard")

    # Verificar estatísticas
    try:
        with open('dados/json/estatisticas_atualizadas.json', 'r', encoding='utf-8') as f:
            stats = json.load(f)

        if stats['resumo']['total_veiculos_diretorias_relevantes'] >= 40:
            validacoes.append("✅ Estatísticas atualizadas")
        else:
            validacoes.append("❌ Estatísticas não atualizadas")
    except:
        validacoes.append("❌ Erro ao verificar estatísticas")

    # Mostrar resultados
    for validacao in validacoes:
        print(f"   {validacao}")

    return all('✅' in v for v in validacoes)


def main():
    """Função principal de correção"""
    print("🚀 INICIANDO CORREÇÃO AUTOMÁTICA COMPLETA")
    print("=" * 50)

    try:
        # 1. Fazer backup
        backup_dir = fazer_backup()

        # 2. Calcular dados corretos
        print("\n📊 Calculando veículos corretos...")
        dados = calcular_veiculos_corretos()

        if not dados:
            print("❌ Falha ao calcular dados")
            return False

        total_veiculos = dados['total_veiculos']

        # 3. Corrigir dashboard
        if not corrigir_dashboard_js(total_veiculos):
            print("❌ Falha ao corrigir dashboard")
            return False

        # 4. Criar estatísticas
        if not criar_estatisticas_atualizadas(dados):
            print("❌ Falha ao criar estatísticas")
            return False

        # 5. Atualizar README
        if not atualizar_readme(dados):
            print("❌ Falha ao atualizar README")
            return False

        # 6. Validar correções
        if validar_correcoes():
            print("\n🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
            print(f"🎯 Dashboard agora mostra {total_veiculos} veículos")
            print(f"📁 Backup salvo em: {backup_dir}")
        else:
            print("\n⚠️ CORREÇÃO PARCIAL - verificar validações")

        return True

    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
