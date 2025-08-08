#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def limpar_dashboard():
    """Remove duplicações e limpa o dashboard"""

    with open('dashboard_integrado.html', 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Remover duplicações do objeto escolasPorDiretoria
    # Manter apenas a primeira ocorrência
    pattern = r'(// Dados das escolas por diretoria\s+const escolasPorDiretoria = \{[^}]+\};)'
    matches = re.findall(pattern, conteudo, re.DOTALL)

    if len(matches) > 1:
        print("🧹 Removendo duplicações dos dados das escolas por diretoria...")
        # Remover todas as ocorrências depois da primeira
        for i in range(1, len(matches)):
            conteudo = conteudo.replace(matches[i], '', 1)

    # Remover duplicações da seção de gráficos
    pattern = r'(// Gráfico de escolas por diretoria.*?}\);)'
    matches = re.findall(pattern, conteudo, re.DOTALL)

    if len(matches) > 1:
        print("🧹 Removendo duplicações do gráfico de escolas por diretoria...")
        # Remover todas as ocorrências depois da primeira
        for i in range(1, len(matches)):
            conteudo = conteudo.replace(matches[i], '', 1)

    # Remover duplicações da seção HTML dos gráficos
    pattern = r'(<div class="chart-panel">\s*<h3>🏫 Escolas por Diretoria</h3>.*?</div>)'
    matches = re.findall(pattern, conteudo, re.DOTALL)

    if len(matches) > 1:
        print("🧹 Removendo duplicações do HTML dos gráficos...")
        # Remover todas as ocorrências depois da primeira
        for i in range(1, len(matches)):
            conteudo = conteudo.replace(matches[i], '', 1)

    # Verificar se temos exatamente 3 gráficos na seção charts-container
    charts_section = re.search(
        r'<div class="charts-container"[^>]*>(.*?)</div>', conteudo, re.DOTALL)
    if charts_section:
        chart_panels = re.findall(
            r'<div class="chart-panel">', charts_section.group(1))
        print(f"📊 Encontrados {len(chart_panels)} painéis de gráfico")

    # Salvar arquivo limpo
    with open('dashboard_integrado.html', 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print("✅ Dashboard limpo com sucesso!")


def main():
    limpar_dashboard()


if __name__ == "__main__":
    main()
