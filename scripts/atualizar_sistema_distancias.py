#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar todos os arquivos do sistema com as distâncias corrigidas
"""

import pandas as pd
import json

def atualizar_sistema_com_distancias_corrigidas():
    """
    Atualiza todos os arquivos do sistema com as distâncias corrigidas
    """
    print("🔄 Atualizando sistema com distâncias corrigidas...")
    print("=" * 50)
    
    try:
        # Ler arquivo corrigido
        df = pd.read_excel('distancias_escolas_diretorias_corrigido.xlsx')
        print(f"✅ Arquivo corrigido carregado: {len(df)} escolas")
        
        # Atualizar dados_escolas_atualizados.json
        print("📝 Atualizando dados_escolas_atualizados.json...")
        dados_json = []
        for _, row in df.iterrows():
            escola = {
                "name": row['Nome_Escola'],
                "type": "indigena" if row['Tipo_Escola'] == "Indígena" else "quilombola",
                "city": row['Cidade_Escola'],
                "diretoria": row['Nome_Diretoria'],
                "distance": row['Distancia_KM'],
                "lat": row['Latitude_Escola'],
                "lng": row['Longitude_Escola'],
                "de_lat": row['Latitude_Diretoria'],
                "de_lng": row['Longitude_Diretoria'],
                "endereco_escola": row['Endereco_Escola'],
                "endereco_diretoria": row['Endereco_Diretoria']
            }
            dados_json.append(escola)
        
        with open('dados_escolas_atualizados.json', 'w', encoding='utf-8') as f:
            json.dump(dados_json, f, ensure_ascii=False, indent=2)
        
        print("✅ dados_escolas_atualizados.json atualizado")
        
        # Preparar dados para os dashboards HTML
        print("📝 Preparando dados para dashboards...")
        
        # Formatar dados para JavaScript
        js_data = "const schoolsData = [\n"
        for _, row in df.iterrows():
            js_data += f"""      {{
        "name": "{row['Nome_Escola']}",
        "type": "{'indigena' if row['Tipo_Escola'] == 'Indígena' else 'quilombola'}",
        "city": "{row['Cidade_Escola']}",
        "diretoria": "{row['Nome_Diretoria']}",
        "distance": {row['Distancia_KM']},
        "lat": {row['Latitude_Escola']},
        "lng": {row['Longitude_Escola']},
        "de_lat": {row['Latitude_Diretoria']},
        "de_lng": {row['Longitude_Diretoria']}
      }},\n"""
        
        js_data = js_data.rstrip(',\n') + "\n    ];"
        
        # Salvar dados formatados
        with open('dados_js_corrigidos.txt', 'w', encoding='utf-8') as f:
            f.write(js_data)
        
        print("✅ Dados JavaScript preparados")
        
        # Estatísticas das correções
        print("\n📊 ESTATÍSTICAS DAS CORREÇÕES:")
        print(f"• Total de escolas: {len(df)}")
        print(f"• Distância média: {df['Distancia_KM'].mean():.2f} km")
        print(f"• Distância mínima: {df['Distancia_KM'].min():.2f} km")
        print(f"• Distância máxima: {df['Distancia_KM'].max():.2f} km")
        
        # Escolas com maior distância
        print(f"\n🚨 ESCOLAS MAIS DISTANTES (>80km):")
        distantes = df[df['Distancia_KM'] > 80].sort_values('Distancia_KM', ascending=False)
        for _, escola in distantes.iterrows():
            print(f"• {escola['Nome_Escola']} ({escola['Nome_Diretoria']}): {escola['Distancia_KM']:.1f} km")
        
        # Verificação específica KOPENOTI
        kopenoti = df[df['Nome_Escola'].str.contains('KOPENOTI', na=False)]
        if not kopenoti.empty:
            kopenoti = kopenoti.iloc[0]
            print(f"\n✅ VERIFICAÇÃO KOPENOTI:")
            print(f"• Nome: {kopenoti['Nome_Escola']}")
            print(f"• Distância corrigida: {kopenoti['Distancia_KM']} km")
            print(f"• Status: {'✅ CORRIGIDA' if kopenoti['Distancia_KM'] < 50 else '⚠️ VERIFICAR'}")
        
        return df
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def gerar_relatorio_correcoes():
    """
    Gera relatório detalhado das correções realizadas
    """
    print("\n📋 Gerando relatório de correções...")
    
    try:
        # Comparar arquivo original com corrigido
        df_original = pd.read_excel('distancias_escolas_diretorias.xlsx')
        df_corrigido = pd.read_excel('distancias_escolas_diretorias_corrigido.xlsx')
        
        # Identificar diferenças
        relatorio = []
        for i, (_, original) in enumerate(df_original.iterrows()):
            corrigido = df_corrigido.iloc[i]
            
            if abs(original['Distancia_KM'] - corrigido['Distancia_KM']) > 1:
                relatorio.append({
                    'Escola': original['Nome_Escola'],
                    'Diretoria': original['Nome_Diretoria'],
                    'Distancia_Original': original['Distancia_KM'],
                    'Distancia_Corrigida': corrigido['Distancia_KM'],
                    'Diferenca': abs(original['Distancia_KM'] - corrigido['Distancia_KM']),
                    'Percentual_Reducao': ((original['Distancia_KM'] - corrigido['Distancia_KM']) / original['Distancia_KM'] * 100)
                })
        
        # Salvar relatório
        df_relatorio = pd.DataFrame(relatorio)
        df_relatorio.to_excel('Relatorio_Correcoes_Distancias.xlsx', index=False)
        
        print(f"✅ Relatório salvo: Relatorio_Correcoes_Distancias.xlsx")
        print(f"📊 {len(relatorio)} escolas tiveram distâncias corrigidas")
        
        return df_relatorio
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        return None

if __name__ == "__main__":
    # Executar atualizações
    df_atualizado = atualizar_sistema_com_distancias_corrigidas()
    
    if df_atualizado is not None:
        # Gerar relatório
        relatorio = gerar_relatorio_correcoes()
        
        print("\n" + "=" * 50)
        print("🎯 SISTEMA ATUALIZADO COM SUCESSO!")
        print("📁 Arquivos atualizados:")
        print("• dados_escolas_atualizados.json")
        print("• dados_js_corrigidos.txt")
        print("• Relatorio_Correcoes_Distancias.xlsx")
        print()
        print("⚡ Próximos passos:")
        print("1. Atualizar dashboards HTML com novos dados")
        print("2. Regenerar relatórios PDF/Excel")
        print("3. Testar sistema atualizado")
        print("=" * 50)
