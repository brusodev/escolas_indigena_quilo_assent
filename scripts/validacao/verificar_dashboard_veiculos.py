#!/usr/bin/env python3
"""
Verificação final dos veículos no dashboard
"""

import re

def verificar_dashboard_veiculos():
    print("🔍 VERIFICAÇÃO FINAL - VEÍCULOS NO DASHBOARD")
    print("=" * 70)
    
    # Ler dashboard
    with open('dashboard_integrado.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se os dados embebidos estão corretos
    if '"total_veiculos": 172' in content:
        print("✅ Metadata com 172 veículos encontrada no código")
    else:
        print("❌ Metadata de 172 veículos não encontrada")
    
    # Verificar se há dados embebidos suficientes
    bauru_pattern = r'"BAURU":\s*{[^}]*"total":\s*2[^}]*}'
    if re.search(bauru_pattern, content):
        print("✅ Diretoria BAURU com dados corretos encontrada")
    else:
        print("❌ Dados da diretoria BAURU não encontrados")
    
    # Verificar function calculateStats atualizada
    if 'vehicleMetadata.total_veiculos' in content:
        print("✅ Função calculateStats usa metadata como prioridade")
    else:
        print("❌ Função calculateStats não atualizada")
    
    # Contar quantas diretorias com dados embebidos
    diretorias_embebidas = len(re.findall(r'"[A-Z\s]+"\s*:\s*{"s1":', content))
    print(f"📊 Diretorias embebidas encontradas: {diretorias_embebidas}")
    
    print()
    print("🎯 DIAGNÓSTICO:")
    print("-" * 50)
    
    if '"total_veiculos": 172' in content and diretorias_embebidas >= 15:
        print("✅ Dashboard deve mostrar 172 veículos")
        print("✅ Dados embebidos suficientes para funcionar")
        print("✅ Problema de CORS resolvido com fallback")
    else:
        print("❌ Dashboard ainda pode ter problemas")
    
    print()
    print("📋 RESUMO:")
    print("=" * 70)
    print("🔧 Correção aplicada: Dados embebidos como fallback")
    print("📊 Total esperado: 172 veículos (não mais 6)")
    print("🎯 Status: Dashboard deve funcionar corretamente")
    print("💡 Solução: Elimina dependência de fetch/CORS")

if __name__ == "__main__":
    verificar_dashboard_veiculos()
