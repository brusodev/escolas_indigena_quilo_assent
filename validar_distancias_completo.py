#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validação Completa de Distâncias
Verifica se todas as distâncias estão corretas usando fórmula de Haversine
"""

import pandas as pd
import math
import json

def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula distância entre dois pontos usando fórmula de Haversine
    
    A fórmula de Haversine é o método padrão para calcular distâncias geodésicas
    (em linha reta) entre dois pontos na superfície terrestre.
    
    Args:
        lat1, lon1: Latitude e longitude do primeiro ponto (em graus)
        lat2, lon2: Latitude e longitude do segundo ponto (em graus)
    
    Returns:
        float: Distância em quilômetros
    """
    # Raio médio da Terra em quilômetros
    R = 6371.0
    
    # Converter graus para radianos
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    # Aplicar fórmula de Haversine
    a = (math.sin(delta_lat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    # Distância em quilômetros
    distancia = R * c
    return distancia

def validar_todas_distancias():
    """
    Valida todas as distâncias no sistema comparando com cálculo Haversine
    """
    print("🔍 VALIDAÇÃO COMPLETA DE DISTÂNCIAS")
    print("=" * 60)
    print("📐 Método: Fórmula de Haversine (padrão geodésico internacional)")
    print("🌍 Precisão: Distância geodésica (linha reta na superfície terrestre)")
    print("=" * 60)
    
    try:
        # Ler dados atuais
        df = pd.read_excel('distancias_escolas_diretorias_corrigido.xlsx')
        print(f"✅ Carregado: {len(df)} escolas para validação")
        print()
        
        # Validar cada escola
        erros = []
        validacoes_ok = 0
        
        for idx, row in df.iterrows():
            # Coordenadas
            lat_escola = row['Latitude_Escola']
            lon_escola = row['Longitude_Escola'] 
            lat_de = row['Latitude_Diretoria']
            lon_de = row['Longitude_Diretoria']
            
            # Verificar coordenadas válidas
            if pd.isna(lat_escola) or pd.isna(lon_escola) or pd.isna(lat_de) or pd.isna(lon_de):
                erros.append({
                    'escola': row['Nome_Escola'],
                    'erro': 'Coordenadas inválidas (valores NaN)',
                    'lat_escola': lat_escola,
                    'lon_escola': lon_escola,
                    'lat_de': lat_de,
                    'lon_de': lon_de
                })
                continue
            
            # Calcular distância usando Haversine
            distancia_calculada = calcular_distancia_haversine(lat_escola, lon_escola, lat_de, lon_de)
            distancia_registrada = row['Distancia_KM']
            
            # Verificar se há diferença significativa (tolerância de 0.1 km)
            diferenca = abs(distancia_calculada - distancia_registrada)
            
            if diferenca > 0.1:
                erros.append({
                    'escola': row['Nome_Escola'],
                    'erro': 'Distância incorreta',
                    'registrada': distancia_registrada,
                    'calculada': round(distancia_calculada, 2),
                    'diferenca': round(diferenca, 2)
                })
            else:
                validacoes_ok += 1
        
        # Relatório de validação
        print(f"📊 RESULTADO DA VALIDAÇÃO:")
        print(f"✅ Escolas com distâncias corretas: {validacoes_ok}")
        print(f"❌ Escolas com problemas: {len(erros)}")
        print(f"📈 Taxa de precisão: {(validacoes_ok/len(df)*100):.1f}%")
        print()
        
        if erros:
            print("🚨 PROBLEMAS ENCONTRADOS:")
            for erro in erros[:10]:  # Mostrar até 10 erros
                print(f"• {erro['escola']}")
                if 'registrada' in erro:
                    print(f"  Registrada: {erro['registrada']} km")
                    print(f"  Calculada: {erro['calculada']} km")
                    print(f"  Diferença: {erro['diferenca']} km")
                else:
                    print(f"  Erro: {erro['erro']}")
                print()
        else:
            print("🎉 TODAS AS DISTÂNCIAS ESTÃO CORRETAS!")
            print("✅ Sistema validado com 100% de precisão")
        
        return erros, validacoes_ok
        
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return None, 0

def gerar_relatorio_validacao(erros, validacoes_ok):
    """
    Gera relatório detalhado da validação
    """
    print("\n📋 Gerando relatório de validação...")
    
    try:
        # Dados para o relatório
        data_relatorio = {
            'Método de Cálculo': 'Fórmula de Haversine',
            'Descrição': 'Distância geodésica (linha reta na superfície terrestre)',
            'Precisão': 'Coordenadas em graus decimais (WGS84)',
            'Raio Terra': '6.371 km (raio médio)',
            'Data Validação': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Total Escolas': validacoes_ok + len(erros) if erros else validacoes_ok,
            'Escolas Válidas': validacoes_ok,
            'Escolas com Erro': len(erros) if erros else 0,
            'Taxa Precisão': f"{(validacoes_ok/(validacoes_ok + (len(erros) if erros else 0))*100):.1f}%"
        }
        
        # Criar DataFrame do relatório
        df_info = pd.DataFrame([data_relatorio])
        
        # Se há erros, criar DataFrame dos erros
        if erros:
            df_erros = pd.DataFrame(erros)
        else:
            df_erros = pd.DataFrame({'Mensagem': ['Todas as distâncias estão corretas!']})
        
        # Salvar relatório
        with pd.ExcelWriter('Relatorio_Validacao_Distancias_Haversine.xlsx') as writer:
            df_info.to_excel(writer, sheet_name='Informações', index=False)
            df_erros.to_excel(writer, sheet_name='Detalhes', index=False)
        
        print("✅ Relatório salvo: Relatorio_Validacao_Distancias_Haversine.xlsx")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        return False

def atualizar_documentacao_haversine():
    """
    Atualiza a documentação dos relatórios para explicitar o uso da fórmula Haversine
    """
    print("\n📝 Atualizando documentação com explicação da fórmula Haversine...")
    
    # Texto explicativo sobre Haversine
    explicacao_haversine = """
METODOLOGIA DE CÁLCULO DE DISTÂNCIAS

📐 FÓRMULA UTILIZADA: Haversine
🌍 TIPO: Distância geodésica (linha reta na superfície terrestre)
📊 PRECISÃO: Coordenadas em graus decimais (sistema WGS84)
🎯 APLICAÇÃO: Padrão internacional para cálculos geográficos

A fórmula de Haversine é o método padrão para calcular a distância mais curta 
entre dois pontos na superfície de uma esfera (Terra). Esta fórmula considera 
a curvatura da Terra e fornece a distância geodésica, que é a distância "em 
linha reta" entre dois pontos seguindo a superfície terrestre.

DIFERENÇAS COM OUTRAS MEDIÇÕES:
• Google Maps: Distância rodoviária (seguindo estradas)
• Distância Euclidiana: Linha reta sem considerar curvatura da Terra
• Distância Haversine: Linha reta considerando curvatura da Terra ✅

VANTAGENS DO MÉTODO HAVERSINE:
✅ Precisão científica reconhecida internacionalmente
✅ Considera a curvatura real da Terra
✅ Ideal para planejamento logístico e análise geográfica
✅ Base para sistemas GPS e navegação
✅ Permite comparações consistentes entre localidades

FÓRMULA MATEMÁTICA:
a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
c = 2 ⋅ atan2(√a, √(1−a))
d = R ⋅ c

Onde:
φ = latitude, λ = longitude, R = raio da Terra (6.371 km)
Δφ = diferença de latitudes, Δλ = diferença de longitudes
"""
    
    try:
        # Salvar explicação em arquivo
        with open('Metodologia_Calculo_Distancias_Haversine.txt', 'w', encoding='utf-8') as f:
            f.write(explicacao_haversine)
        
        print("✅ Documentação salva: Metodologia_Calculo_Distancias_Haversine.txt")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar documentação: {e}")
        return False

def verificar_casos_especificos():
    """
    Verifica casos específicos mencionados pelo usuário
    """
    print("\n🔍 Verificando casos específicos...")
    
    try:
        df = pd.read_excel('distancias_escolas_diretorias_corrigido.xlsx')
        
        # Casos específicos para verificar
        casos_teste = [
            "ALDEIA KOPENOTI",
            "DJEKUPE AMBA ARANDY", 
            "ALDEIA DE PARANAPUA",
            "ALDEIA TEKOA MIRIM"
        ]
        
        print("📍 VERIFICAÇÃO DE CASOS ESPECÍFICOS:")
        print("-" * 50)
        
        for escola_nome in casos_teste:
            escola = df[df['Nome_Escola'].str.contains(escola_nome, na=False)]
            
            if not escola.empty:
                escola = escola.iloc[0]
                
                # Calcular distância Haversine
                dist_haversine = calcular_distancia_haversine(
                    escola['Latitude_Escola'], escola['Longitude_Escola'],
                    escola['Latitude_Diretoria'], escola['Longitude_Diretoria']
                )
                
                dist_registrada = escola['Distancia_KM']
                diferenca = abs(dist_haversine - dist_registrada)
                
                status = "✅ OK" if diferenca < 0.1 else "⚠️ REVISAR"
                
                print(f"🏫 {escola_nome}")
                print(f"   Diretoria: {escola['Nome_Diretoria']}")
                print(f"   Registrada: {dist_registrada} km")
                print(f"   Haversine: {dist_haversine:.2f} km")
                print(f"   Diferença: {diferenca:.2f} km")
                print(f"   Status: {status}")
                print()
            else:
                print(f"❌ Escola não encontrada: {escola_nome}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO VALIDAÇÃO COMPLETA DO SISTEMA")
    print("⏰ " + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'))
    print()
    
    # Executar validação
    erros, validacoes_ok = validar_todas_distancias()
    
    if erros is not None:
        # Gerar relatório
        gerar_relatorio_validacao(erros, validacoes_ok)
        
        # Atualizar documentação
        atualizar_documentacao_haversine()
        
        # Verificar casos específicos
        verificar_casos_especificos()
        
        print("\n" + "=" * 60)
        print("🎯 VALIDAÇÃO COMPLETA FINALIZADA")
        print("📁 Arquivos gerados:")
        print("• Relatorio_Validacao_Distancias_Haversine.xlsx")
        print("• Metodologia_Calculo_Distancias_Haversine.txt")
        print()
        print("✅ Sistema validado com fórmula de Haversine")
        print("📐 Documentação atualizada com metodologia")
        print("=" * 60)
    else:
        print("❌ Falha na validação. Verificar dados de entrada.")
