#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar o dashboard HTML com as distâncias corrigidas
"""

import re

def atualizar_dashboard_html():
    """
    Atualiza o arquivo distancias_escolas.html com os dados corrigidos
    """
    print("🔄 Atualizando dashboard HTML com distâncias corrigidas...")
    print("=" * 55)
    
    try:
        # Ler dados corrigidos
        with open('dados_js_corrigidos.txt', 'r', encoding='utf-8') as f:
            dados_corrigidos = f.read()
        
        # Ler dashboard atual
        with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Encontrar início e fim da seção schoolsData
        inicio_pattern = r'const schoolsData = \['
        fim_pattern = r'\];;;;;;;;;;'
        
        inicio_match = re.search(inicio_pattern, html_content)
        fim_match = re.search(fim_pattern, html_content)
        
        if not inicio_match or not fim_match:
            print("❌ Não foi possível encontrar a seção schoolsData no HTML")
            return False
        
        # Extrair novos dados (remover "const schoolsData = ")
        novos_dados = dados_corrigidos.replace('const schoolsData = ', '').rstrip(';')
        
        # Substituir seção no HTML
        novo_html = (
            html_content[:inicio_match.start()] +
            'const schoolsData = ' + novos_dados + ';;;;;;;;;;\n\n    // Calcular estatísticas' +
            html_content[fim_match.end():]
        )
        
        # Salvar arquivo atualizado
        with open('distancias_escolas.html', 'w', encoding='utf-8') as f:
            f.write(novo_html)
        
        print("✅ Dashboard HTML atualizado com sucesso!")
        
        # Verificar algumas distâncias específicas
        print("\n📊 Verificando distâncias atualizadas:")
        
        verificacoes = [
            ("ALDEIA KOPENOTI", "27.16"),
            ("DJEKUPE AMBA ARANDY", "9.43"),
            ("ALDEIA DE PARANAPUA", "1.85"),
            ("ALDEIA TEKOA MIRIM", "15.16")
        ]
        
        for escola, dist_esperada in verificacoes:
            if f'"name": "{escola}"' in novo_html and f'"distance": {dist_esperada}' in novo_html:
                print(f"✅ {escola}: {dist_esperada} km")
            else:
                print(f"⚠️  {escola}: verificar manualmente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar dashboard: {e}")
        return False

def atualizar_estatisticas():
    """
    Atualiza as estatísticas do dashboard baseadas nas novas distâncias
    """
    print("\n📊 Recalculando estatísticas...")
    
    try:
        import pandas as pd
        
        # Ler dados corrigidos
        df = pd.read_excel('distancias_escolas_diretorias_corrigido.xlsx')
        
        # Calcular novas estatísticas
        total_escolas = len(df)
        distancia_media = df['Distancia_KM'].mean()
        escolas_alta_prioridade = len(df[df['Distancia_KM'] > 50])
        diretorias_unicas = df['Nome_Diretoria'].nunique()
        
        print(f"📈 Nova estatísticas:")
        print(f"• Total de escolas: {total_escolas}")
        print(f"• Distância média: {distancia_media:.1f} km")
        print(f"• Escolas >50km: {escolas_alta_prioridade}")
        print(f"• Diretorias únicas: {diretorias_unicas}")
        
        # Ler e atualizar HTML
        with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Atualizar estatísticas no HTML
        html_content = re.sub(
            r'<div class="stat-number" id="avg-distance">\d+\.?\d*</div>',
            f'<div class="stat-number" id="avg-distance">{distancia_media:.1f}</div>',
            html_content
        )
        
        html_content = re.sub(
            r'<div class="stat-number" id="high-priority">\d+</div>',
            f'<div class="stat-number" id="high-priority">{escolas_alta_prioridade}</div>',
            html_content
        )
        
        # Salvar
        with open('distancias_escolas.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Estatísticas atualizadas no dashboard")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar estatísticas: {e}")
        return False

def validar_atualizacao():
    """
    Valida se a atualização foi bem-sucedida
    """
    print("\n🔍 Validando atualização...")
    
    try:
        with open('distancias_escolas.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Verificar se KOPENOTI não tem mais 286.65 km
        if '"distance": 286.65' in html_content:
            print("❌ ERRO: Ainda há distâncias não corrigidas (286.65)")
            return False
        
        # Verificar se KOPENOTI tem 27.16 km
        if '"name": "ALDEIA KOPENOTI"' in html_content and '"distance": 27.16' in html_content:
            print("✅ KOPENOTI corrigida: 27.16 km")
        else:
            print("⚠️  KOPENOTI: verificar correção")
        
        # Contar total de escolas no JS
        escolas_count = html_content.count('"name":')
        print(f"✅ Total de escolas no dashboard: {escolas_count}")
        
        if escolas_count == 59:
            print("✅ Todas as 59 escolas estão presentes")
            return True
        else:
            print(f"⚠️  Esperado 59 escolas, encontrado {escolas_count}")
            return False
        
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return False

if __name__ == "__main__":
    # Executar atualizações
    sucesso_dashboard = atualizar_dashboard_html()
    
    if sucesso_dashboard:
        sucesso_stats = atualizar_estatisticas()
        sucesso_validacao = validar_atualizacao()
        
        if sucesso_stats and sucesso_validacao:
            print("\n" + "=" * 55)
            print("🎉 DASHBOARD ATUALIZADO COM SUCESSO!")
            print("📁 Arquivo atualizado: distancias_escolas.html")
            print("📊 Estatísticas recalculadas")
            print("✅ Validação concluída")
            print()
            print("🚀 Principais melhorias:")
            print("• ALDEIA KOPENOTI: 286.65 km → 27.16 km")
            print("• DJEKUPE AMBA ARANDY: 72.40 km → 9.43 km")
            print("• Distância média reduzida significativamente")
            print("• Cálculos mais precisos com fórmula Haversine")
            print("=" * 55)
        else:
            print("\n❌ Houve problemas na atualização. Verifique os logs acima.")
    else:
        print("\n❌ Falha ao atualizar dashboard. Verificar dados de entrada.")
