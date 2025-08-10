#!/usr/bin/env python3
"""
Script para corrigir veículos do dashboard - versão final
Inclui normalização de nomes de diretorias
"""

import json
import os
import shutil
import unicodedata
from datetime import datetime


def normalizar_nome(nome):
    """Remove acentos e normaliza nomes para comparação"""
    if not nome:
        return ""
    # Remove acentos
    nome_norm = unicodedata.normalize('NFD', nome)
    nome_sem_acento = ''.join(
        c for c in nome_norm if unicodedata.category(c) != 'Mn')
    return nome_sem_acento.upper().strip()


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
    """Calcula dados corretos com normalização de nomes"""
    try:
        # Carregar dados de escolas
        with open('dados/json/dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
            escolas = json.load(f)

        print(f"📊 Total de escolas: {len(escolas)}")

        # Contar por tipo e diretorias
        tipos = {}
        diretorias_escolas = {}

        for escola in escolas:
            tipo = escola.get('type', 'Desconhecido')
            if tipo not in tipos:
                tipos[tipo] = 0
            tipos[tipo] += 1

            diretoria = escola.get('diretoria', '')
            if diretoria:
                diretoria_norm = normalizar_nome(diretoria)
                if diretoria_norm not in diretorias_escolas:
                    diretorias_escolas[diretoria_norm] = diretoria

        print(f"📝 Tipos: {tipos}")
        print(f"📍 Diretorias com escolas: {len(diretorias_escolas)}")

        # Carregar dados de veículos
        with open('dados/json/dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
            veiculos_data = json.load(f)

        # Criar mapeamento normalizado de veículos
        veiculos_norm = {}
        for nome_original, dados in veiculos_data['diretorias'].items():
            nome_normalizado = normalizar_nome(nome_original)
            veiculos_norm[nome_normalizado] = {
                'nome_original': nome_original,
                'total': dados['total'],
                'dados': dados
            }

        # Calcular veículos das diretorias que atendem escolas
        total_veiculos = 0
        diretorias_atendidas = 0
        detalhamento = {}

        print("\n📋 Detalhamento por diretoria:")
        for diretoria_norm, diretoria_original in sorted(diretorias_escolas.items()):
            if diretoria_norm in veiculos_norm:
                veiculos_info = veiculos_norm[diretoria_norm]
                qtd_veiculos = veiculos_info['total']
                total_veiculos += qtd_veiculos
                diretorias_atendidas += 1
                detalhamento[diretoria_original] = qtd_veiculos
                print(f"   ✅ {diretoria_original}: {qtd_veiculos} veículos")
            else:
                print(f"   ❌ {diretoria_original}: NÃO ENCONTRADA")
                # Tentar buscar similares
                for nome_veiculo_norm in veiculos_norm.keys():
                    if diretoria_norm in nome_veiculo_norm or nome_veiculo_norm in diretoria_norm:
                        similar_info = veiculos_norm[nome_veiculo_norm]
                        print(
                            f"      💡 Similar encontrada: {similar_info['nome_original']}")

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

        # Buscar diferentes padrões e substituir
        import re

        substituicoes_feitas = 0

        # Padrão 1: totalVehicles: número
        padrao1 = re.compile(r'totalVehicles:\s*(\d+)', re.IGNORECASE)
        if padrao1.search(conteudo):
            conteudo = padrao1.sub(
                f'totalVehicles: {total_veiculos}', conteudo)
            substituicoes_feitas += 1
            print(f"✅ Corrigido padrão: totalVehicles: X")

        # Padrão 2: "vehicles": número
        padrao2 = re.compile(r'"vehicles":\s*(\d+)', re.IGNORECASE)
        if padrao2.search(conteudo):
            conteudo = padrao2.sub(f'"vehicles": {total_veiculos}', conteudo)
            substituicoes_feitas += 1
            print(f"✅ Corrigido padrão: \"vehicles\": X")

        # Padrão 3: vehicles = número
        padrao3 = re.compile(r'vehicles\s*=\s*(\d+)', re.IGNORECASE)
        if padrao3.search(conteudo):
            conteudo = padrao3.sub(f'vehicles = {total_veiculos}', conteudo)
            substituicoes_feitas += 1
            print(f"✅ Corrigido padrão: vehicles = X")

        # Salvar arquivo corrigido
        with open('static/js/dash.js', 'w', encoding='utf-8') as f:
            f.write(conteudo)

        print(f"✅ Dashboard atualizado ({substituicoes_feitas} correções)")
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
                "Contagem considera apenas diretorias que atendem escolas indígenas/quilombolas",
                "Normalização de nomes aplicada para correspondência de acentos"
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
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()

        # Buscar diferentes padrões e substituir
        padroes_substituir = [
            (r'\b6\s*veículos?\b', f"{dados['total_veiculos']} veículos"),
            (r'\b6\s*Veículos?\b', f"{dados['total_veiculos']} Veículos"),
            (r'total:\s*6\b', f"total: {dados['total_veiculos']}"),
        ]

        import re
        substituicoes = 0

        for padrao, substituicao in padroes_substituir:
            if re.search(padrao, readme, re.IGNORECASE):
                readme = re.sub(padrao, substituicao,
                                readme, flags=re.IGNORECASE)
                substituicoes += 1
                print(f"✅ README: padrão atualizado")

        # Salvar README atualizado
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme)

        print(f"✅ README atualizado ({substituicoes} alterações)")
        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar README: {e}")
        return False


def validar_correcoes(total_esperado):
    """Valida se as correções foram aplicadas corretamente"""
    print("\n🔍 Validando correções...")

    validacoes = []

    # Verificar dashboard
    try:
        with open('static/js/dash.js', 'r', encoding='utf-8') as f:
            js_content = f.read()

        import re
        # Buscar qualquer padrão que contenha o número esperado
        if re.search(rf'vehicles.*{total_esperado}', js_content, re.IGNORECASE):
            validacoes.append("✅ Dashboard JavaScript corrigido")
        else:
            validacoes.append("❌ Dashboard JavaScript não encontrado")
    except:
        validacoes.append("❌ Erro ao verificar dashboard")

    # Verificar estatísticas
    try:
        with open('dados/json/estatisticas_atualizadas.json', 'r', encoding='utf-8') as f:
            stats = json.load(f)

        if stats['resumo']['total_veiculos_diretorias_relevantes'] == total_esperado:
            validacoes.append("✅ Estatísticas corretas")
        else:
            validacoes.append(
                f"❌ Estatísticas: {stats['resumo']['total_veiculos_diretorias_relevantes']} != {total_esperado}")
    except:
        validacoes.append("❌ Erro ao verificar estatísticas")

    # Mostrar resultados
    for validacao in validacoes:
        print(f"   {validacao}")

    return all('✅' in v for v in validacoes)


def main():
    """Função principal de correção"""
    print("🚀 INICIANDO CORREÇÃO AUTOMÁTICA FINAL")
    print("=" * 50)

    try:
        # 1. Fazer backup
        backup_dir = fazer_backup()

        # 2. Calcular dados corretos
        dados = calcular_veiculos_corretos()

        if not dados:
            print("❌ Falha ao calcular dados")
            return False

        total_veiculos = dados['total_veiculos']

        # 3. Corrigir dashboard
        corrigir_dashboard_js(total_veiculos)

        # 4. Criar estatísticas
        criar_estatisticas_atualizadas(dados)

        # 5. Atualizar README
        atualizar_readme(dados)

        # 6. Validar correções
        if validar_correcoes(total_veiculos):
            print("\n🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
        else:
            print("\n⚠️ CORREÇÃO FINALIZADA - verificar detalhes")

        print(f"\n📊 RESUMO FINAL:")
        print(f"   🎯 Veículos calculados: {total_veiculos}")
        print(f"   🏫 Escolas atendidas: {dados['total_escolas']}")
        print(f"   🏢 Diretorias envolvidas: {dados['total_diretorias']}")
        print(f"   📁 Backup: {backup_dir}")

        return True

    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
