#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Limpeza Final
Remove arquivos desnecessários do projeto antigo
"""

import os
import shutil
from pathlib import Path


def arquivos_para_remover():
    """Lista de arquivos e diretórios para remoção"""
    return [
        # Dashboard antigo
        'dashboard_integrado.html',
        'dashboard_corrigido_final.html',
        'index.html',
        'distancias_escolas.html',

        # Scripts do dashboard
        'atualizar_dashboard_completo.py',
        'atualizar_dashboard.py',
        'criar_dashboard_corrigido_final.py',
        'servidor_corrigido_final.py',
        'menu_integrado.py',
        'mostrar_dados_atuais.py',
        'testar_dashboard_completo.py',

        # Scripts de geração antigos
        'gerar_graficos_frota.py',
        'gerar_relatorio_excel.py',
        'gerar_relatorio_pdf.py',
        'gerar_relatorios.py',
        'relatorio_final_status.py',
        'analise_frota_integrada.py',

        # Scripts de correção executados
        'corrigir_coordenadas.py',
        'corrigir_distancias.py',
        'atualizar_relatorios_haversine.py',
        'atualizar_sistema_distancias.py',
        'regenerar_tudo_atualizado.py',

        # Scripts de validação antigos
        'validar_distancias_completo.py',
        'verificar_completo.py',
        'verificar_dados.py',
        'verificar_enderecos_v2.py',

        # Outros
        'converter_dados.py',
        'criar_bases_exemplo.py',
        'main.py',

        # JSONs duplicados
        'dados_escolas_corrigidos.json',
        'dados_js_corrigidos.txt',
        'dados_veiculos.json',

        # Diretórios antigos
        'static/',
        'templates/',
        'dashboard/',
        'scripts/',
        'old_backups/',
        'backup_dashboard_20250811_223729/',
        'dados/js/',
        'documentacao/logs/',

        # Relatórios gerados (podem ser regenerados)
        'Relatorio_*.pdf',
        'Graficos_*.png',
        'Mapa_Calor_*.png',
        'Analise_Integrada_*.xlsx',
        'distancias_escolas_diretorias*.xlsx',
        'Relatorio_*.xlsx',
        'Metodologia_*.txt'
    ]


def limpar_projeto():
    """Remove arquivos desnecessários"""
    print("🧹 INICIANDO LIMPEZA FINAL DO PROJETO...")
    print("=" * 50)

    arquivos_removidos = 0
    diretorios_removidos = 0
    erros = 0

    for item in arquivos_para_remover():
        item_path = Path(item)

        try:
            if item_path.exists():
                if item_path.is_file():
                    item_path.unlink()
                    print(f"🗑️ Arquivo removido: {item}")
                    arquivos_removidos += 1
                elif item_path.is_dir():
                    shutil.rmtree(item_path)
                    print(f"📁 Diretório removido: {item}")
                    diretorios_removidos += 1
            else:
                # Verificar com glob para padrões
                for match in Path('.').glob(item):
                    if match.is_file():
                        match.unlink()
                        print(f"🗑️ Arquivo removido: {match}")
                        arquivos_removidos += 1
                    elif match.is_dir():
                        shutil.rmtree(match)
                        print(f"📁 Diretório removido: {match}")
                        diretorios_removidos += 1
        except Exception as e:
            print(f"❌ Erro ao remover {item}: {e}")
            erros += 1

    print(f"\n📊 RESUMO DA LIMPEZA:")
    print(f"   🗑️ Arquivos removidos: {arquivos_removidos}")
    print(f"   📁 Diretórios removidos: {diretorios_removidos}")
    print(f"   ❌ Erros: {erros}")

    if erros == 0:
        print("✅ LIMPEZA CONCLUÍDA COM SUCESSO!")
    else:
        print("⚠️ LIMPEZA CONCLUÍDA COM ALGUNS ERROS")

    return erros == 0


def arquivos_mantidos():
    """Lista arquivos que foram mantidos"""
    print("\n📁 ARQUIVOS MANTIDOS NO PROJETO:")
    print("-" * 40)

    mantidos = [
        # Bases de dados
        'bases_padronizadas/',
        'dados_escolas_atualizados.json',
        'dados_veiculos_diretorias.json',
        'dados_supervisao_atualizados.json',
        'estatisticas_atualizadas.json',

        # Excel importantes
        'diretorias_com_coordenadas.xlsx',
        'diretorias_ensino_completo.xlsx',
        'QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx',
        'GEP.xlsx',
        'ENDERECO_ESCOLAS_062025 (1).csv',

        # Documentação
        'README.md',
        'GUIA_RAPIDO.md',
        'relatorio_bruno.md',

        # Scripts úteis
        'calcular_distancias.py',
        'processar_dados_atualizados.py',
        'padronizar_bases.py',
        'organizar_projeto.py',

        # Projeto Flask
        'flask_sistema/'
    ]

    for item in mantidos:
        if Path(item).exists():
            print(f"✅ {item}")
        else:
            print(f"❌ {item} (não encontrado)")


def main():
    """Função principal"""
    print("🧹 LIMPEZA FINAL DO PROJETO")
    print("Remoção de arquivos desnecessários após migração para Flask")
    print("=" * 60)

    # Confirmar operação
    print("\n⚠️ ATENÇÃO: Esta operação removerá PERMANENTEMENTE:")
    print("   - Dashboard antigo e arquivos relacionados")
    print("   - Scripts de correção já executados")
    print("   - Relatórios gerados (podem ser regenerados)")
    print("   - Arquivos temporários e duplicados")

    resposta = input("\nDeseja continuar? (s/N): ").lower().strip()

    if resposta in ['s', 'sim', 'y', 'yes']:
        # Executar limpeza
        sucesso = limpar_projeto()

        # Mostrar arquivos mantidos
        arquivos_mantidos()

        if sucesso:
            print(f"\n🎉 PROJETO LIMPO E ORGANIZADO!")
            print(f"📁 Estrutura final:")
            print(f"   ✅ Bases de dados padronizadas mantidas")
            print(f"   ✅ Documentação preservada")
            print(f"   ✅ Scripts úteis mantidos")
            print(f"   ✅ Projeto Flask completo criado")
            print(f"\n🚀 PRÓXIMO PASSO:")
            print(f"   cd flask_sistema")
            print(f"   python init_db.py init")
        else:
            print(f"\n⚠️ Limpeza concluída com alguns erros")
    else:
        print("❌ Operação cancelada")


if __name__ == "__main__":
    main()
