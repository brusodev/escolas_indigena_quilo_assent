import os


def main():
    """Menu principal integrado com análise de frota"""

    while True:
        print("\n" + "=" * 80)
        print("🎯 SISTEMA INTEGRADO DE ANÁLISE - ESCOLAS × DIRETORIAS × FROTA")
        print("=" * 80)

        print("Escolha uma opção:")
        print("\n📊 RELATÓRIOS BÁSICOS:")
        print("1️⃣  Relatório Excel Completo (Escolas + Endereços + Distâncias)")
        print("2️⃣  Relatório PDF Paisagem (Layout elegante para impressão)")
        print("3️⃣  Ambos os Relatórios Básicos")

        print("\n🚗 ANÁLISE DE FROTA (NOVA!):")
        print("4️⃣  Análise Integrada de Frota")
        print("   • Demanda de veículos por diretoria")
        print("   • Baseada em escolas distantes (>50km)")
        print("   • Integração com dados de supervisão")

        print("5️⃣  Gráficos de Análise de Frota")
        print("   • Visualizações estratégicas")
        print("   • Mapas de calor de necessidade")
        print("   • Análise por região e prioridade")

        print("6️⃣  Pacote Completo de Frota")
        print("   • Análise + Gráficos + Relatórios")
        print("   • Solução completa para tomada de decisão")

        print("\n🛠️ UTILITÁRIOS:")
        print("7️⃣  Recalcular Distâncias (se alterou coordenadas)")
        print("8️⃣  Regenerar Relatórios (após editar coordenadas/veículos)")
        print("9️⃣  Mostrar Dados Atuais (para edição)")
        print("🔟  Visualizar Arquivos Gerados")
        print("1️⃣1️⃣ Atualizar Bases de Dados de Frota")
        print("0️⃣  Sair")

        print("=" * 80)

        opcao = input("👉 Digite sua opção (0-11): ").strip()

        if opcao == "0":
            print("👋 Obrigado por usar o sistema de análise integrada!")
            break

        elif opcao == "1":
            print("\n📊 Gerando Relatório Excel Completo...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe gerar_relatorio_excel.py"
            )

        elif opcao == "2":
            print("\n📄 Gerando Relatório PDF Paisagem...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe gerar_relatorio_pdf.py"
            )

        elif opcao == "3":
            print("\n📊📄 Gerando Ambos os Relatórios...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe gerar_relatorio_excel.py"
            )
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe gerar_relatorio_pdf.py"
            )

        elif opcao == "4":
            print("\n🚗 Executando Análise Integrada de Frota...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe analise_frota_integrada.py"
            )

        elif opcao == "5":
            print("\n📊 Gerando Gráficos de Análise de Frota...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe gerar_graficos_frota.py"
            )

        elif opcao == "6":
            print("\n🎯 Executando Pacote Completo de Análise de Frota...")
            print("📋 Passo 1/3: Análise integrada...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe analise_frota_integrada.py"
            )
            print("\n📊 Passo 2/3: Gráficos...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe gerar_graficos_frota.py"
            )
            print("\n📄 Passo 3/3: Relatórios complementares...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe gerar_relatorio_excel.py"
            )
            print("\n✅ Pacote completo gerado com sucesso!")

        elif opcao == "7":
            print("\n🔄 Recalculando Distâncias...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe calcular_distancias.py"
            )

        elif opcao == "8":
            print("\n🔄 Regenerando TODOS os Relatórios com dados atualizados...")
            print("📋 Passo 1/4: Relatório Excel...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe gerar_relatorio_excel.py"
            )
            print("\n📄 Passo 2/4: Relatório PDF...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe gerar_relatorio_pdf.py"
            )
            print("\n🚗 Passo 3/4: Análise de Frota...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe analise_frota_integrada.py"
            )
            print("\n📊 Passo 4/4: Gráficos...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe gerar_graficos_frota.py"
            )
            print("\n✅ TODOS os relatórios regenerados com sucesso!")

        elif opcao == "9":
            print("\n📋 Mostrando Dados Atuais para Edição...")
            os.system(
                "C:/Users/es.bruno.vargas/Desktop/escolas_indigina_quilo_assent/.venv/Scripts/python.exe mostrar_dados_atuais.py"
            )

        elif opcao == "10" or opcao == "🔟":
            print("\n📁 Arquivos gerados:")
            arquivos = [
                ("Excel Completo", "Relatorio_Completo_Escolas_Diretorias.xlsx"),
                ("PDF Paisagem", "Relatorio_Paisagem_*.pdf"),
                ("Análise de Frota", "Analise_Integrada_Escolas_Frota_Supervisao.xlsx"),
                ("Gráficos de Frota", "Graficos_Analise_Frota.png"),
                ("Mapa de Calor", "Mapa_Calor_Necessidade_Veiculos.png"),
                ("Dados Base", "distancias_escolas_diretorias.xlsx"),
                ("Dados Veículos", "QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx"),
                ("Dados Supervisão", "GEP.xlsx"),
            ]

            for desc, arquivo in arquivos:
                if "*" in arquivo:
                    # Listar arquivos com padrão
                    import glob

                    files = glob.glob(arquivo)
                    if files:
                        print(
                            f"✅ {desc}: {files[0]} (e {len(files)-1} outros)"
                            if len(files) > 1
                            else f"✅ {desc}: {files[0]}"
                        )
                    else:
                        print(f"❌ {desc}: Não encontrado")
                else:
                    if os.path.exists(arquivo):
                        tamanho = os.path.getsize(arquivo) / 1024  # KB
                        print(f"✅ {desc}: {arquivo} ({tamanho:.1f} KB)")
                    else:
                        print(f"❌ {desc}: {arquivo} (Não encontrado)")

        elif opcao == "11":
            print("\n🔄 Para atualizar as bases de dados:")
            print("\n📍 COORDENADAS DAS ESCOLAS:")
            print("   Opção A (Rápida): Edite 'distancias_escolas_diretorias.xlsx'")
            print("   • Colunas G (Latitude_Escola) e H (Longitude_Escola)")
            print("   • Use opção 8️⃣ para regenerar relatórios")
            print("\n   Opção B (Permanente): Edite 'ENDERECO_ESCOLAS_062025 (1).csv'")
            print("   • Colunas DS_LATITUDE e DS_LONGITUDE")
            print("   • Use opção 7️⃣ para recalcular tudo")
            print("\n🚗 VEÍCULOS POR DIRETORIA:")
            print("   Edite: 'QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx'")
            print(
                "   • Colunas: DIRETORIA, QUANTIDADE S-1, QUANTIDADE S-2, QUANTIDADE S-2 4X4"
            )
            print("   • Use opção 8️⃣ para regenerar relatórios")
            print("\n👥 SUPERVISÃO (GEP):")
            print("   Edite: 'GEP.xlsx'")
            print(
                "   • Colunas: REGIÃO, DIRETORIA DE ENSINO SOB SUPERVISÃO, QUANTIDADE DE DEs, SUPERVISOR GEP"
            )
            print(
                "\n💡 IMPORTANTE: Use nomes de diretorias EXATAMENTE como aparecem nos relatórios!"
            )
            print("💡 Use opção 9️⃣ para ver os dados atuais antes de editar!")

        else:
            print("❌ Opção inválida! Digite um número de 0 a 11.")

        if opcao != "0":
            input("\n⏸️  Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
