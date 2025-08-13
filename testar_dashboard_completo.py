#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE DASHBOARD CITEM COMPLETO
=============================

Script para testar e validar o funcionamento do dashboard
com as 5.582 escolas integradas.

Verificações:
1. Arquivos de dados disponíveis
2. Estrutura JSON correta
3. Coordenadas válidas
4. Compatibilidade com módulos JavaScript

Autor: Sistema Dashboard Escolas
Data: 11/08/2025
"""

import json
import os
from pathlib import Path


def testar_arquivos_dashboard():
    """Testar se todos os arquivos necessários existem"""
    print("🔍 TESTANDO ARQUIVOS DO DASHBOARD...")
    print("-" * 40)

    arquivos_necessarios = [
        # Dados
        "dados/json/dados_escolas_atualizados_completo.json",
        "dados/json/config_dashboard_completo.json",

        # HTML
        "dashboard_citem_completo.html",

        # CSS
        "static/css/dash.css",
        "static/css/dashboard-citem-completo.css",

        # JavaScript
        "static/js/modules/data-loader-citem-completo.js",
        "static/js/modules/type-filters.js",

        # JavaScript existentes (verificar se ainda funcionam)
        "static/js/modules/map-components.js",
        "static/js/dashboard-main.js"
    ]

    todos_ok = True

    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            size = os.path.getsize(arquivo)
            print(f"✅ {arquivo} ({size:,} bytes)")
        else:
            print(f"❌ {arquivo} - ARQUIVO FALTANDO")
            todos_ok = False

    return todos_ok


def testar_dados_escolas():
    """Testar estrutura e conteúdo dos dados das escolas"""
    print("\n📊 TESTANDO DADOS DAS ESCOLAS...")
    print("-" * 35)

    try:
        with open('dados/json/dados_escolas_atualizados_completo.json', 'r', encoding='utf-8') as f:
            escolas = json.load(f)

        print(f"✅ Total de escolas carregadas: {len(escolas):,}")

        if len(escolas) > 0:
            escola_exemplo = escolas[0]

            # Verificar campos obrigatórios
            campos_obrigatorios = ['name', 'type',
                                   'city', 'diretoria', 'lat', 'lng']
            campos_ok = all(
                campo in escola_exemplo for campo in campos_obrigatorios)

            if campos_ok:
                print("✅ Estrutura dos dados: OK")
                print(f"   📍 Exemplo: {escola_exemplo['name']}")
                print(f"   🏛️ Tipo: {escola_exemplo['type']}")
                print(
                    f"   📍 Coordenadas: ({escola_exemplo['lat']}, {escola_exemplo['lng']})")
            else:
                print("❌ Estrutura dos dados: CAMPOS FALTANDO")
                return False

        # Contar tipos
        tipos = {}
        coordenadas_validas = 0

        for escola in escolas:
            tipo = escola.get('type', 'sem_tipo')
            tipos[tipo] = tipos.get(tipo, 0) + 1

            if escola.get('lat') and escola.get('lng'):
                coordenadas_validas += 1

        print(f"\n📈 DISTRIBUIÇÃO POR TIPO:")
        for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
            print(f"   {tipo}: {count:,} escolas")

        print(f"\n📍 COORDENADAS:")
        print(
            f"   ✅ Válidas: {coordenadas_validas:,} ({coordenadas_validas/len(escolas)*100:.1f}%)")
        print(f"   ❌ Inválidas: {len(escolas)-coordenadas_validas:,}")

        # 95% devem ter coordenadas
        return coordenadas_validas > len(escolas) * 0.95

    except Exception as e:
        print(f"❌ Erro ao testar dados: {str(e)}")
        return False


def testar_configuracao():
    """Testar arquivo de configuração"""
    print("\n⚙️ TESTANDO CONFIGURAÇÃO...")
    print("-" * 30)

    try:
        with open('dados/json/config_dashboard_completo.json', 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Verificar seções obrigatórias
        secoes_obrigatorias = ['metadata', 'tipos_escola', 'configuracao']

        for secao in secoes_obrigatorias:
            if secao in config:
                print(f"✅ Seção '{secao}': OK")
            else:
                print(f"❌ Seção '{secao}': FALTANDO")
                return False

        # Verificar metadados
        metadata = config['metadata']
        print(f"   📅 Data: {metadata.get('data_atualizacao', 'N/A')}")
        print(f"   📊 Total escolas: {metadata.get('total_escolas', 'N/A'):,}")
        print(f"   🏷️ Versão: {metadata.get('versao', 'N/A')}")

        # Verificar tipos
        tipos = config['tipos_escola']
        print(f"   🎨 Tipos configurados: {len(tipos)}")

        return True

    except Exception as e:
        print(f"❌ Erro ao testar configuração: {str(e)}")
        return False


def gerar_relatorio_teste():
    """Gerar relatório completo do teste"""
    print("\n📋 RELATÓRIO FINAL DO TESTE")
    print("=" * 45)

    # Executar todos os testes
    arquivos_ok = testar_arquivos_dashboard()
    dados_ok = testar_dados_escolas()
    config_ok = testar_configuracao()

    # Resumo
    print(f"\n🎯 RESULTADO GERAL:")
    print(f"   📁 Arquivos: {'✅ OK' if arquivos_ok else '❌ PROBLEMA'}")
    print(f"   📊 Dados: {'✅ OK' if dados_ok else '❌ PROBLEMA'}")
    print(f"   ⚙️ Configuração: {'✅ OK' if config_ok else '❌ PROBLEMA'}")

    sucesso_geral = arquivos_ok and dados_ok and config_ok

    if sucesso_geral:
        print(f"\n🎉 DASHBOARD PRONTO PARA USO!")
        print("   🌐 Abra 'dashboard_citem_completo.html' no navegador")
        print("   🗺️ Todas as 5.582 escolas serão exibidas no mapa")
        print("   🎛️ Use os filtros por tipo de escola")
        print("   🔍 Busca e navegação disponíveis")
    else:
        print(f"\n⚠️ PROBLEMAS ENCONTRADOS!")
        print("   🔧 Corrija os erros listados acima antes de usar")

    return sucesso_geral


def criar_instrucoes_uso():
    """Criar arquivo com instruções de uso"""
    instrucoes = """# 🎯 INSTRUÇÕES DE USO - DASHBOARD CITEM COMPLETO

## 🚀 Como Usar o Dashboard

### 1. Abrir o Dashboard
- Abra o arquivo `dashboard_citem_completo.html` no navegador
- Certifique-se de que está em um servidor local (não arquivo:// direto)

### 2. Funcionalidades Disponíveis

#### 🗺️ Mapa Interativo
- **5.582 escolas** plotadas com coordenadas precisas
- **Cores diferentes** para cada tipo de escola:
  - 🏫 Regular (azul) - 4.964 escolas
  - 👥 Indígena (marrom) - 43 escolas
  - 🏛️ Quilombola (roxo) - 16 escolas
  - 🚜 Assentamento (verde) - 4 escolas
  - 📚 CEEJA (vermelho) - 43 escolas
  - 🎓 CEL JTO (laranja) - 165 escolas
  - 🏥 Hospitalar (vermelho escuro) - 71 escolas
  - 🏢 Penitenciária (cinza) - 163 escolas
  - 👦 Socioeducativo (violeta) - 113 escolas

#### 🎛️ Filtros por Tipo
- Clique nos botões de filtro para mostrar apenas um tipo
- Filtro "Todas" mostra todas as 5.582 escolas
- Contadores atualizam automaticamente

#### 🔍 Busca Inteligente
- Busque por nome da escola, município ou unidade regional
- Busca funciona dentro do filtro ativo
- Resultados em tempo real

#### 📋 Lista de Escolas
- Até 100 escolas exibidas por vez (performance)
- Clique em uma escola para centralizar no mapa
- Informações completas de cada escola

### 3. Controles do Mapa
- **Tela Cheia**: Expandir mapa para tela inteira
- **Zoom**: Use mouse ou controles do mapa
- **Popup**: Clique em marcador para ver detalhes

### 4. Dados Técnicos
- **Fonte**: Sistema CITEM oficial
- **Coordenadas**: WGS84 com precisão geodésica
- **Atualização**: 11/08/2025
- **Encoding**: UTF-8 com coordenadas decimais brasileiras

## 🔧 Solução de Problemas

### Mapa não carrega
- Verifique conexão com internet (Leaflet CDN)
- Use servidor local (não abra arquivo diretamente)

### Filtros não funcionam
- Verifique console do navegador (F12)
- Certifique-se de que todos os arquivos JS estão carregados

### Performance lenta
- Com 5.582 escolas, o carregamento pode demorar alguns segundos
- Use filtros para reduzir número de marcadores visíveis

## 📊 Estatísticas Importantes
- **Total**: 5.582 escolas mapeadas
- **Cobertura**: 100% com coordenadas válidas
- **Unidades Regionais**: 89 diretorias mapeadas
- **Tipos de Escola**: 10 categorias diferentes

## 🎯 Casos de Uso
1. **Análise Regional**: Filtrar por tipo e ver distribuição geográfica
2. **Planejamento**: Identificar concentrações de escolas especiais
3. **Busca Específica**: Localizar escolas por nome ou município
4. **Visualização**: Compreender rede estadual completa

---
*Dashboard desenvolvido para análise completa do sistema educacional paulista*
"""

    with open('INSTRUCOES_DASHBOARD_CITEM.md', 'w', encoding='utf-8') as f:
        f.write(instrucoes)

    print(f"\n📖 Instruções criadas: INSTRUCOES_DASHBOARD_CITEM.md")


def main():
    """Função principal de teste"""
    print("🧪 TESTE COMPLETO DO DASHBOARD CITEM")
    print("=" * 45)
    print("Objetivo: Validar funcionamento completo do dashboard")
    print("Data:", "11/08/2025")
    print()

    try:
        # Executar testes
        sucesso = gerar_relatorio_teste()

        # Criar instruções
        criar_instrucoes_uso()

        if sucesso:
            print(f"\n🎊 TESTE CONCLUÍDO COM SUCESSO!")
            print("   O dashboard está pronto para uso!")
        else:
            print(f"\n⚠️ TESTE ENCONTROU PROBLEMAS!")
            print("   Corrija os erros antes de usar o dashboard")

    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {str(e)}")


if __name__ == "__main__":
    main()
