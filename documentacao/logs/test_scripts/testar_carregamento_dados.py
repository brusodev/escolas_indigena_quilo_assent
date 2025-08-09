#!/usr/bin/env python3
"""
Teste do carregamento de dados no dashboard
"""

import json
import os

def testar_dados_dashboard():
    print("🔍 TESTE DE CARREGAMENTO DOS DADOS")
    print("=" * 60)
    
    # Verificar se o JSON existe e é acessível
    json_file = "dados_veiculos_diretorias.json"
    
    if os.path.exists(json_file):
        print(f"✅ Arquivo JSON encontrado: {json_file}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print("✅ JSON carregado com sucesso")
            
            # Verificar estrutura
            if 'metadata' in data and 'diretorias' in data:
                metadata = data['metadata']
                diretorias = data['diretorias']
                
                print(f"📊 Metadata total_veiculos: {metadata.get('total_veiculos')}")
                print(f"📊 Diretorias no JSON: {len(diretorias)}")
                
                # Calcular total real
                total_calculado = sum(d.get('total', 0) for d in diretorias.values())
                print(f"📊 Total calculado: {total_calculado}")
                
                # Verificar algumas diretorias específicas mencionadas no dashboard
                diretorias_teste = ['ANDRADINA', 'AVARE', 'BAURU']
                for nome in diretorias_teste:
                    if nome in diretorias:
                        info = diretorias[nome]
                        print(f"   {nome}: {info}")
                    else:
                        print(f"   ❌ {nome} não encontrado")
                
                # Verificar diretorias com escolas
                print(f"\n🏫 DIRETORIAS COM ESCOLAS:")
                escolas_por_diretoria = {}
                
                # Ler dados das escolas do dashboard
                with open('dashboard_integrado.html', 'r', encoding='utf-8') as f:
                    dashboard_content = f.read()
                
                # Procurar por "Bauru" no dashboard
                if 'Bauru' in dashboard_content:
                    print("✅ Diretoria 'Bauru' encontrada no dashboard")
                    if 'BAURU' in diretorias:
                        print(f"✅ BAURU no JSON: {diretorias['BAURU']}")
                    else:
                        print("❌ BAURU não encontrado no JSON (problema de normalização)")
                
            else:
                print("❌ Estrutura do JSON incorreta")
                
        except Exception as e:
            print(f"❌ Erro ao processar JSON: {e}")
    else:
        print(f"❌ Arquivo JSON não encontrado: {json_file}")
    
    print(f"\n🎯 DIAGNÓSTICO:")
    print("=" * 60)
    
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        metadata_total = data['metadata']['total_veiculos']
        diretorias_count = len(data['diretorias'])
        calculated_total = sum(d.get('total', 0) for d in data['diretorias'].values())
        
        print(f"📊 Metadata diz: {metadata_total} veículos")
        print(f"📊 Cálculo real: {calculated_total} veículos")
        print(f"📊 Diretorias: {diretorias_count}")
        
        if metadata_total == calculated_total == 172:
            print("✅ Dados estão corretos - problema é no JavaScript")
        else:
            print("❌ Inconsistência nos dados")
            
        # Se o dashboard mostra 6, provavelmente está usando fallback
        if calculated_total == 172:
            print("🔍 Dashboard provavelmente está usando dados de fallback")
            print("💡 Possível problema: CORS, erro de fetch, ou caminho do arquivo")

if __name__ == "__main__":
    testar_dados_dashboard()
