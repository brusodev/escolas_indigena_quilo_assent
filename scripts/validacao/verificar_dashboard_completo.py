"""
Script para verificar se o dashboard está funcionando corretamente após as correções
Data: 07/08/2025
"""

import json

def verificar_dashboard():
    """Verificar se todos os dados estão corretos"""
    print("=== VERIFICAÇÃO COMPLETA DO DASHBOARD ===\n")
    
    # Carregar dados
    with open('dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
        escolas = json.load(f)
    
    with open('dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
        dados_veiculos = json.load(f)
    
    veiculos = dados_veiculos['diretorias']
    metadata = dados_veiculos['metadata']
    
    print(f"✅ DADOS CARREGADOS:")
    print(f"  • Total de escolas: {len(escolas)}")
    print(f"  • Total de diretorias no JSON: {len(veiculos)}")
    print(f"  • Total de veículos: {metadata['total_veiculos']}")
    print()
    
    # Verificar mapeamento de diretorias
    diretorias_escolas = set(escola['diretoria'] for escola in escolas)
    print(f"📊 DIRETORIAS COM ESCOLAS: {len(diretorias_escolas)}")
    for diretoria in sorted(diretorias_escolas):
        print(f"  • {diretoria}")
    print()
    
    # Verificar função de normalização
    def normalizeDiretoriaName(name):
        if not name:
            return ''
        
        normalized = name.upper().strip()
        
        mappings = {
            'SAO VICENTE': 'SÃO VICENTE',
            'SAO BERNARDO DO CAMPO': 'SÃO BERNARDO DO CAMPO',
            'SANTO ANASTACIO': 'SANTO ANASTÁCIO',
            'PENAPOLIS': 'PENÁPOLIS',
            'TUPA': 'TUPÃ',
            'ITARARE': 'ITARARÉ',
            'LESTE 5': 'LESTE 5',
            'SUL 3': 'SUL 3',
            'NORTE 1': 'NORTE 1'
        }
        
        return mappings.get(normalized, normalized)
    
    print("🔍 VERIFICAÇÃO DE MAPEAMENTO:")
    problemas = []
    veiculos_mapeados = 0
    
    for diretoria in sorted(diretorias_escolas):
        diretoria_normalizada = normalizeDiretoriaName(diretoria)
        if diretoria_normalizada in veiculos:
            total_veiculos = veiculos[diretoria_normalizada]['total']
            veiculos_mapeados += total_veiculos
            print(f"  ✅ {diretoria} → {diretoria_normalizada} ({total_veiculos} veículos)")
        else:
            problemas.append(diretoria)
            print(f"  ❌ {diretoria} → {diretoria_normalizada} (NÃO ENCONTRADA)")
    
    print()
    print(f"📈 RESULTADOS:")
    print(f"  • Diretorias mapeadas com sucesso: {len(diretorias_escolas) - len(problemas)}")
    print(f"  • Diretorias com problemas: {len(problemas)}")
    print(f"  • Total de veículos mapeados: {veiculos_mapeados}")
    print(f"  • Total de veículos no sistema: {metadata['total_veiculos']}")
    
    if problemas:
        print(f"\n🚨 PROBLEMAS ENCONTRADOS:")
        for problema in problemas:
            print(f"  • {problema}")
    else:
        print(f"\n🎉 TODOS OS MAPEAMENTOS ESTÃO CORRETOS!")
    
    # Verificar estatísticas finais para o dashboard
    escolas_alta_prioridade = sum(1 for escola in escolas if escola['distance'] > 50)
    
    print(f"\n📊 ESTATÍSTICAS PARA O DASHBOARD:")
    print(f"  • Total de escolas: {len(escolas)}")
    print(f"  • Total de veículos: {veiculos_mapeados}")
    print(f"  • Diretorias com escolas: {len(diretorias_escolas)}")
    print(f"  • Escolas >50km: {escolas_alta_prioridade}")
    print(f"  • Distância média: {sum(escola['distance'] for escola in escolas) / len(escolas):.1f} km")

if __name__ == "__main__":
    verificar_dashboard()
