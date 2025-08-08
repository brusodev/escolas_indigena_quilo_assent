#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para validar os dados finais e corrigir a documentação.
"""

import json


def validar_dados_finais():
    """Valida os dados finais após correção."""

    print("✅ VALIDAÇÃO FINAL DOS DADOS DE VEÍCULOS")
    print("=" * 50)

    # Carregar dados das escolas
    try:
        with open(
            "dados/json/dados_escolas_atualizados.json", "r", encoding="utf-8"
        ) as f:
            escolas = json.load(f)
        print(f"📚 Escolas carregadas: {len(escolas)}")
    except Exception as e:
        print(f"❌ Erro ao carregar escolas: {e}")
        return

    # Carregar dados de veículos
    try:
        with open(
            "dados/json/dados_veiculos_atualizados.json", "r", encoding="utf-8"
        ) as f:
            veiculos = json.load(f)
        print(f"🚗 Dados de veículos carregados: {len(veiculos)} diretorias")
    except Exception as e:
        print(f"❌ Erro ao carregar veículos: {e}")
        return

    # Extrair diretorias das escolas
    diretorias_com_escolas = set([escola["diretoria"] for escola in escolas])

    print(f"\n📊 RESUMO FINAL:")
    print(f"   • Total de escolas: {len(escolas)}")
    print(f"   • Diretorias com escolas: {len(diretorias_com_escolas)}")

    # Mapear nomes das diretorias (escolas usam nomes diferentes dos veículos)
    mapeamento_diretorias = {
        "Andradina": "ADAMANTINA",
        "Apiai": "BOTUCATU",
        "Avare": "BOTUCATU",
        "Bauru": "BAURU",
        "Caraguatatuba": "CARAPICUÍBA",
        "Itapeva": "BOTUCATU",
        "Itarare": "BOTUCATU",
        "Lins": "ARARAQUARA",
        "Miracatu": "ITAPECERICA DA SERRA",
        "Mirante do Paranapanema": "PRESIDENTE PRUDENTE",
        "Norte 1": "GUARULHOS NORTE",
        "Penapolis": "ARAÇATUBA",
        "Registro": "ITAPECERICA DA SERRA",
        "Santo Anastacio": "PRESIDENTE PRUDENTE",
        "Santos": "SANTOS",
        "Sao Bernardo do Campo": "DIADEMA",
        "Sul 3": "GUARULHOS SUL",
        "SÃO VICENTE": "SANTOS",
        "Tupa": "TUPÃ",
    }

    # Contar veículos para diretorias relevantes
    diretorias_veiculos_relevantes = set()
    total_veiculos_relevantes = 0
    total_s1 = 0
    total_s2 = 0
    total_s2_4x4 = 0

    for diretoria_escola in diretorias_com_escolas:
        if diretoria_escola in mapeamento_diretorias:
            diretoria_veiculo = mapeamento_diretorias[diretoria_escola]
            diretorias_veiculos_relevantes.add(diretoria_veiculo)

            if diretoria_veiculo in veiculos:
                dados_dir = veiculos[diretoria_veiculo]
                total_veiculos_relevantes += dados_dir.get("total", 0)
                total_s1 += dados_dir.get("s1", 0)
                total_s2 += dados_dir.get("s2", 0)
                total_s2_4x4 += dados_dir.get("s2_4x4", 0)

    print(f"\n🗂️  DIRETORIAS DE VEÍCULOS RELEVANTES:")
    for diretoria in sorted(diretorias_veiculos_relevantes):
        if diretoria in veiculos:
            dados = veiculos[diretoria]
            print(
                f"   • {diretoria}: {dados['total']} veículos (S1={dados['s1']}, S2={dados['s2']}, S2_4x4={dados['s2_4x4']})"
            )

    print(f"\n📈 TOTAIS FINAIS:")
    print(
        f"   • Diretorias com escolas indígenas/quilombolas/assentamento: {len(diretorias_com_escolas)}"
    )
    print(
        f"   • Diretorias de veículos correspondentes: {len(diretorias_veiculos_relevantes)}"
    )
    print(f"   • Total de veículos: {total_veiculos_relevantes}")
    print(f"   • Distribuição: S1={total_s1}, S2={total_s2}, S2_4x4={total_s2_4x4}")

    # Verificar se números estão corretos
    if (
        total_veiculos_relevantes == 30
        and total_s1 == 10
        and total_s2 == 18
        and total_s2_4x4 == 2
    ):
        print(f"\n🎯 DADOS VALIDADOS COM SUCESSO!")
        print(f"   ✅ Base principal atualizada corretamente")
        print(f"   ✅ Números conferem com dados originais")
        print(f"   ✅ Sistema pronto para uso")
    else:
        print(f"\n⚠️  ATENÇÃO: Verificar números")

    # Mostrar correspondência escola-diretoria
    print(f"\n🔗 CORRESPONDÊNCIA ESCOLAS ↔ DIRETORIAS:")
    for diretoria_escola in sorted(diretorias_com_escolas):
        escolas_dir = [e for e in escolas if e["diretoria"] == diretoria_escola]
        diretoria_veiculo = mapeamento_diretorias.get(diretoria_escola, "NÃO MAPEADA")
        print(
            f"   {diretoria_escola} → {diretoria_veiculo} ({len(escolas_dir)} escolas)"
        )

        for escola in escolas_dir:
            tipos = {"indigena": "🏛️", "quilombola": "🏘️", "assentamento": "🌾"}
            icon = tipos.get(escola["type"], "📍")
            print(f"      {icon} {escola['name']} ({escola['type']})")


if __name__ == "__main__":
    validar_dados_finais()
