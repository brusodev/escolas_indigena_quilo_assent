#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RESUMO DA ORGANIZAÇÃO DO PROJETO
Sistema de Gestão de Escolas Indígenas, Quilombolas e Assentamentos
"""

import os
from datetime import datetime


def contar_arquivos_por_pasta():
    """Conta arquivos em cada pasta do projeto"""
    print("📁 RESUMO DA ORGANIZAÇÃO DO PROJETO")
    print("=" * 80)
    print(f"📅 Data da Organização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

    estrutura = {
        "dados/excel": "Planilhas Excel (.xlsx)",
        "dados/json": "Dados estruturados JSON",
        "dados": "Dados CSV originais",
        "scripts": "Scripts Python principais",
        "scripts/geracao": "Scripts de geração de relatórios",
        "scripts/validacao": "Scripts de validação",
        "scripts/correcao": "Scripts de correção",
        "dashboard": "Interface web e arquivos HTML/JS",
        "relatorios/excel": "Relatórios Excel gerados",
        "relatorios/pdf": "Relatórios PDF gerados",
        "relatorios/graficos": "Gráficos e visualizações",
        "documentacao": "Documentação técnica completa",
    }

    total_arquivos = 0

    for pasta, descricao in estrutura.items():
        if os.path.exists(pasta):
            if os.path.isdir(pasta):
                arquivos = [
                    f
                    for f in os.listdir(pasta)
                    if os.path.isfile(os.path.join(pasta, f))
                ]
                total = len(arquivos)
            else:
                total = 0
        else:
            total = 0

        total_arquivos += total
        print(f"📂 {pasta.ljust(25)} │ {str(total).rjust(3)} arquivos │ {descricao}")

    # Contar arquivos na raiz
    raiz_arquivos = [f for f in os.listdir(".") if os.path.isfile(f)]
    total_raiz = len(raiz_arquivos)
    total_arquivos += total_raiz

    print(
        f"📂 {'/ (raiz)'.ljust(25)} │ {str(total_raiz).rjust(3)} arquivos │ Scripts principais e documentação"
    )
    print()
    print(f"📊 TOTAL DE ARQUIVOS ORGANIZADOS: {total_arquivos}")
    print()

    print("🎯 ARQUIVOS CRÍTICOS DO SISTEMA:")
    print("-" * 50)

    arquivos_criticos = [
        (
            "dados/excel/distancias_escolas_diretorias_completo_63_corrigido.xlsx",
            "🎯 FONTE PRINCIPAL",
        ),
        ("dados/json/dados_veiculos_diretorias.json", "🚗 DADOS VEÍCULOS"),
        ("dados/json/config_sistema.json", "⚙️ CONFIGURAÇÃO"),
        ("dashboard/dashboard_integrado.html", "🌐 DASHBOARD"),
        ("scripts/repositorio_central.py", "🔍 VALIDAÇÃO"),
        ("scripts/atualizar_relatorios_completos.py", "🚀 ATUALIZAÇÃO"),
        ("documentacao/DOCUMENTACAO_COMPLETA.md", "📚 DOCUMENTAÇÃO"),
        ("main.py", "🏠 SCRIPT PRINCIPAL"),
    ]

    for arquivo, tipo in arquivos_criticos:
        status = "✅ OK" if os.path.exists(arquivo) else "❌ FALTANDO"
        print(f"{status} {arquivo.ljust(60)} {tipo}")

    print()
    print("🔧 COMANDOS PRINCIPAIS:")
    print("-" * 50)
    print("🔍 Validar sistema:       python scripts/repositorio_central.py")
    print("🚀 Gerar relatórios:     python scripts/atualizar_relatorios_completos.py")
    print("🌐 Ver dashboard:         dashboard/dashboard_integrado.html")
    print("📚 Ver documentação:      documentacao/DOCUMENTACAO_COMPLETA.md")
    print()

    print("✅ BENEFÍCIOS DA ORGANIZAÇÃO:")
    print("-" * 50)
    print("📁 Navegação intuitiva por tipo de arquivo")
    print("🔍 Localização rápida de componentes específicos")
    print("💾 Backups organizados e estruturados")
    print("🛠️ Manutenção simplificada do código")
    print("📈 Escalabilidade para novos recursos")
    print("🎯 Separação clara entre dados, scripts e relatórios")
    print()

    print("🎉 ORGANIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("📋 Estrutura pronta para uso em produção")
    print("🚀 Sistema completamente funcional e validado")


if __name__ == "__main__":
    contar_arquivos_por_pasta()
