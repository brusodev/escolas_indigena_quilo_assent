import os
import sys
from datetime import datetime


def mostrar_menu():
    """Mostra o menu de opções"""
    print("=" * 60)
    print("🎯 GERADOR DE RELATÓRIOS - ESCOLAS E DIRETORIAS")
    print("=" * 60)
    print()
    print("Escolha o tipo de relatório que deseja gerar:")
    print()
    print("1️⃣  Relatório Excel Completo")
    print("   • Formato: Planilha Excel (.xlsx)")
    print("   • Conteúdo: Dados abrangentes com 12+ colunas")
    print("   • Ideal para: Análise detalhada e gestão completa")
    print()
    print("2️⃣  Relatório PDF Paisagem")
    print("   • Formato: Documento PDF (.pdf) em orientação paisagem")
    print("   • Conteúdo: Layout elegante com gráficos expandidos")
    print("   • Ideal para: Apresentações panorâmicas e impressão A4")
    print()
    print("3️⃣  Ambos os Relatórios")
    print("   • Gera Excel + PDF")
    print("   • Conjunto completo de relatórios")
    print()
    print("4️⃣  Visualizar Arquivos Gerados")
    print("   • Lista relatórios já criados")
    print()
    print("0️⃣  Sair")
    print()
    print("=" * 60)


def verificar_dependencias():
    """Verifica se todos os arquivos necessários existem"""
    arquivos_necessarios = ["distancias_escolas_diretorias.xlsx"]

    arquivos_faltando = []
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            arquivos_faltando.append(arquivo)

    if arquivos_faltando:
        print("❌ ERRO: Arquivos necessários não encontrados:")
        for arquivo in arquivos_faltando:
            print(f"   • {arquivo}")
        print()
        print("💡 Execute primeiro: python calcular_distancias.py")
        return False

    return True


def gerar_excel():
    """Gera o relatório Excel"""
    print("\n📊 Iniciando geração do Relatório Excel...")
    try:
        os.system(f"{sys.executable} gerar_relatorio_excel.py")
        print("\n✅ Relatório Excel gerado com sucesso!")
        return True
    except Exception as e:
        print(f"\n❌ Erro ao gerar relatório Excel: {e}")
        return False


def gerar_pdf():
    """Gera o relatório PDF"""
    print("\n📄 Iniciando geração do Relatório PDF...")
    try:
        os.system(f"{sys.executable} gerar_relatorio_pdf.py")
        print("\n✅ Relatório PDF gerado com sucesso!")
        return True
    except Exception as e:
        print(f"\n❌ Erro ao gerar relatório PDF: {e}")
        return False


def listar_arquivos_gerados():
    """Lista os relatórios já gerados"""
    print("\n📁 RELATÓRIOS DISPONÍVEIS:")
    print("-" * 40)

    arquivos_relatorio = []

    # Buscar arquivos Excel
    for arquivo in os.listdir("."):
        if arquivo.startswith("Relatorio_") and arquivo.endswith(".xlsx"):
            arquivos_relatorio.append(("Excel", arquivo))
        elif arquivo.startswith("Relatorio_") and arquivo.endswith(".pdf"):
            arquivos_relatorio.append(("PDF", arquivo))

    if not arquivos_relatorio:
        print("   Nenhum relatório encontrado.")
        print("   Gere um relatório primeiro.")
    else:
        for tipo, arquivo in arquivos_relatorio:
            # Obter data de modificação
            timestamp = os.path.getmtime(arquivo)
            data = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")
            tamanho = os.path.getsize(arquivo) / 1024  # KB

            print(f"📄 {tipo:5} | {arquivo}")
            print(f"   📅 Criado: {data}")
            print(f"   📏 Tamanho: {tamanho:.1f} KB")
            print()

    print("-" * 40)


def main():
    """Função principal"""

    while True:
        mostrar_menu()

        try:
            opcao = input("👉 Digite sua opção (0-4): ").strip()

            if opcao == "0":
                print("\n👋 Obrigado por usar o gerador de relatórios!")
                break

            elif opcao == "1":
                if verificar_dependencias():
                    sucesso = gerar_excel()
                    if sucesso:
                        print("\n🎉 Relatório Excel Completo pronto para uso!")
                        print("📂 Arquivo: Relatorio_Completo_Escolas_Diretorias.xlsx")
                        print("📊 Inclui: 12+ colunas com dados abrangentes")

            elif opcao == "2":
                if verificar_dependencias():
                    sucesso = gerar_pdf()
                    if sucesso:
                        print("\n🎉 Relatório PDF Paisagem pronto para impressão!")
                        print("📂 Arquivo: Relatorio_Paisagem_Escolas_[timestamp].pdf")
                        print("📏 Orientação: Paisagem (mais espaço para tabelas)")

            elif opcao == "3":
                if verificar_dependencias():
                    print("\n🔄 Gerando ambos os relatórios...")

                    sucesso_excel = gerar_excel()
                    sucesso_pdf = gerar_pdf()

                    if sucesso_excel and sucesso_pdf:
                        print("\n🎉 Ambos os relatórios foram gerados com sucesso!")
                        print("📂 Arquivos disponíveis:")
                        print(
                            "   • Relatorio_Completo_Escolas_Diretorias.xlsx (Excel completo)"
                        )
                        print(
                            "   • Relatorio_Paisagem_Escolas_[timestamp].pdf (PDF paisagem)"
                        )
                        print("🎯 Conjunto completo para análise e apresentação!")
                    elif sucesso_excel:
                        print("\n⚠️ Apenas o relatório Excel foi gerado com sucesso.")
                    elif sucesso_pdf:
                        print("\n⚠️ Apenas o relatório PDF foi gerado com sucesso.")
                    else:
                        print("\n❌ Erro ao gerar os relatórios.")

            elif opcao == "4":
                listar_arquivos_gerados()

            else:
                print("\n❌ Opção inválida! Digite um número de 0 a 4.")

            if opcao != "4":
                input("\n📎 Pressione Enter para continuar...")

        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            input("\n📎 Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
