#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERADOR DE RELATÓRIO PDF MELHORADO
Escolas Indígenas, Quilombolas e Assentamentos
Versão com ordenação por distância e gráficos das maiores distâncias
"""

import os
import sys
import pandas as pd
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configurar matplotlib para suporte ao português
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


class RelatorioMelhoradoPDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.criar_estilos_customizados()
        self.criar_diretorios()

    def criar_diretorios(self):
        """Cria os diretórios necessários"""
        os.makedirs("relatorios/pdf", exist_ok=True)
        os.makedirs("relatorios/graficos", exist_ok=True)

    def criar_estilos_customizados(self):
        """Cria estilos customizados para o PDF"""

        # Título principal
        self.styles.add(
            ParagraphStyle(
                name="TituloPrincipal",
                parent=self.styles["Title"],
                fontSize=22,
                spaceAfter=25,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#1B4F72"),
                fontName="Helvetica-Bold",
            )
        )

        # Subtítulo
        self.styles.add(
            ParagraphStyle(
                name="Subtitulo",
                parent=self.styles["Heading1"],
                fontSize=16,
                spaceAfter=15,
                spaceBefore=20,
                alignment=TA_LEFT,
                textColor=colors.HexColor("#2874A6"),
                fontName="Helvetica-Bold",
            )
        )

        # Texto normal
        self.styles.add(
            ParagraphStyle(
                name="TextoNormal",
                parent=self.styles["Normal"],
                fontSize=11,
                spaceAfter=10,
                alignment=TA_LEFT,
                fontName="Helvetica",
            )
        )

    def criar_graficos_maiores_distancias(self, df):
        """Cria gráficos focados nas maiores distâncias"""

        # Preparar dados numéricos
        df_num = df.copy()
        df_num["Distancia_Numerica"] = df_num["Distancia_KM"].apply(
            lambda x: float(x) if pd.notna(x) and x != "N/A" else 0
        )

        # Ordenar por distância (maior para menor)
        df_ordenado = df_num.sort_values("Distancia_Numerica", ascending=False)

        # 1. Gráfico das Top 15 Escolas com Maiores Distâncias
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))

        top_15_escolas = df_ordenado.head(15)

        # Criar nomes curtos para as escolas
        nomes_curtos = []
        for nome in top_15_escolas["Nome_Escola"]:
            if len(nome) > 30:
                nomes_curtos.append(nome[:27] + "...")
            else:
                nomes_curtos.append(nome)

        # Cores baseadas na classificação
        cores = []
        for dist in top_15_escolas["Distancia_Numerica"]:
            if dist >= 80:
                cores.append("#E74C3C")  # Vermelho para muito longe
            elif dist >= 50:
                cores.append("#F39C12")  # Laranja para longe
            else:
                cores.append("#F7DC6F")  # Amarelo para médio

        bars = ax.barh(
            range(len(top_15_escolas)),
            top_15_escolas["Distancia_Numerica"],
            color=cores,
            alpha=0.8,
        )

        ax.set_yticks(range(len(top_15_escolas)))
        ax.set_yticklabels(nomes_curtos, fontsize=10)
        ax.set_xlabel("Distância (km)", fontsize=12, fontweight="bold")
        ax.set_title(
            "🎯 TOP 15 ESCOLAS COM MAIORES DISTÂNCIAS",
            fontsize=16,
            fontweight="bold",
            color="#1B4F72",
            pad=20,
        )
        ax.grid(True, alpha=0.3, axis="x")

        # Adicionar valores nas barras
        for i, bar in enumerate(bars):
            width = bar.get_width()
            tipo = top_15_escolas.iloc[i]["Tipo_Escola"]
            tipo_abrev = "IND" if tipo == "Indígena" else "QUI"
            ax.text(
                width + 1,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}km ({tipo_abrev})",
                ha="left",
                va="center",
                fontsize=9,
                fontweight="bold",
            )

        # Adicionar legenda
        ax.text(
            0.02,
            0.98,
            "🔴 ≥80km (Muito Longe)  🟠 50-79km (Longe)  🟡 <50km (Médio)",
            transform=ax.transAxes,
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7),
            verticalalignment="top",
        )

        plt.tight_layout()
        plt.savefig(
            "relatorios/graficos/top_15_maiores_distancias.png",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
        )
        plt.close()

        # 2. Gráfico de Distribuição de Distâncias por Faixas
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # Histograma de distribuição
        ax1.hist(
            df_num["Distancia_Numerica"],
            bins=15,
            color="#3498DB",
            alpha=0.7,
            edgecolor="black",
        )
        ax1.set_xlabel("Distância (km)", fontsize=12, fontweight="bold")
        ax1.set_ylabel("Número de Escolas", fontsize=12, fontweight="bold")
        ax1.set_title(
            "📊 DISTRIBUIÇÃO DAS DISTÂNCIAS",
            fontsize=14,
            fontweight="bold",
            color="#1B4F72",
        )
        ax1.grid(True, alpha=0.3)

        # Gráfico de pizza por classificação
        classificacao_counts = df["Classificacao"].value_counts()
        colors_pie = ["#E74C3C", "#F39C12", "#27AE60"]  # Vermelho, Laranja, Verde

        wedges, texts, autotexts = ax2.pie(
            classificacao_counts.values,
            labels=classificacao_counts.index,
            autopct="%1.1f%%",
            colors=colors_pie,
            startangle=90,
            textprops={"fontsize": 10, "fontweight": "bold"},
        )

        ax2.set_title(
            "🎯 CLASSIFICAÇÃO POR DISTÂNCIA",
            fontsize=14,
            fontweight="bold",
            color="#1B4F72",
        )

        plt.tight_layout()
        plt.savefig(
            "relatorios/graficos/distribuicao_distancias.png",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
        )
        plt.close()

        # 3. Gráfico das Diretorias com Maiores Distâncias Médias
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))

        # Calcular distância média por diretoria
        diretorias_stats = (
            df_num.groupby("DE_Responsavel")
            .agg({"Distancia_Numerica": ["mean", "max", "count"]})
            .round(2)
        )

        diretorias_stats.columns = [
            "Distancia_Media",
            "Distancia_Maxima",
            "Num_Escolas",
        ]
        diretorias_stats = diretorias_stats.sort_values(
            "Distancia_Media", ascending=False
        )

        # Top 10 diretorias
        top_diretorias = diretorias_stats.head(10)

        # Nomes curtos para diretorias
        nomes_diretorias = []
        for nome in top_diretorias.index:
            if len(nome) > 25:
                nomes_diretorias.append(nome[:22] + "...")
            else:
                nomes_diretorias.append(nome)

        bars = ax.barh(
            range(len(top_diretorias)),
            top_diretorias["Distancia_Media"],
            color="#8E44AD",
            alpha=0.8,
        )

        ax.set_yticks(range(len(top_diretorias)))
        ax.set_yticklabels(nomes_diretorias, fontsize=10)
        ax.set_xlabel("Distância Média (km)", fontsize=12, fontweight="bold")
        ax.set_title(
            "🏢 TOP 10 DIRETORIAS - MAIORES DISTÂNCIAS MÉDIAS",
            fontsize=16,
            fontweight="bold",
            color="#1B4F72",
            pad=20,
        )
        ax.grid(True, alpha=0.3, axis="x")

        # Adicionar valores nas barras
        for i, bar in enumerate(bars):
            width = bar.get_width()
            num_escolas = int(top_diretorias.iloc[i]["Num_Escolas"])
            dist_max = top_diretorias.iloc[i]["Distancia_Maxima"]
            ax.text(
                width + 1,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}km (máx: {dist_max:.1f}km, {num_escolas} escolas)",
                ha="left",
                va="center",
                fontsize=9,
                fontweight="bold",
            )

        plt.tight_layout()
        plt.savefig(
            "relatorios/graficos/diretorias_maiores_distancias.png",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
        )
        plt.close()

        return df_ordenado

    def criar_tabela_melhorada(self, df_ordenado):
        """Cria tabela com ordenação por distância e coluna contador"""

        # Adicionar coluna contador
        df_ordenado = df_ordenado.reset_index(drop=True)
        df_ordenado.index = df_ordenado.index + 1  # Começar contador do 1

        # Preparar dados para a tabela
        dados_tabela = [
            ["#", "Escola", "Tipo", "Cidade", "Diretoria", "Dist.(km)", "Class."]
        ]

        for idx, row in df_ordenado.iterrows():
            nome_escola = (
                row["Nome_Escola"][:35] + "..."
                if len(row["Nome_Escola"]) > 35
                else row["Nome_Escola"]
            )

            tipo_abrev = "IND" if row["Tipo_Escola"] == "Indígena" else "QUI/ASS"

            cidade = (
                row["Cidade_Escola"][:15] + "..."
                if len(row["Cidade_Escola"]) > 15
                else row["Cidade_Escola"]
            )

            diretoria = (
                row["DE_Responsavel"][:20] + "..."
                if len(row["DE_Responsavel"]) > 20
                else row["DE_Responsavel"]
            )

            # Classificação abreviada com emoji
            if row["Distancia_KM"] >= 80:
                class_emoji = "🔴 Alta"
            elif row["Distancia_KM"] >= 50:
                class_emoji = "🟠 Média"
            else:
                class_emoji = "🟢 Baixa"

            dados_tabela.append(
                [
                    str(idx),  # Contador
                    nome_escola,
                    tipo_abrev,
                    cidade,
                    diretoria,
                    f"{row['Distancia_KM']:.1f}",
                    class_emoji,
                ]
            )

        # Criar tabela
        tabela = Table(
            dados_tabela,
            colWidths=[
                0.6 * inch,
                2.8 * inch,
                0.8 * inch,
                1.2 * inch,
                1.8 * inch,
                0.8 * inch,
                0.8 * inch,
            ],
        )

        # Estilo da tabela
        estilo_tabela = TableStyle(
            [
                # Cabeçalho
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1B4F72")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                # Corpo da tabela
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                # Zebrar linhas
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#F8F9FA")],
                ),
                # Destacar as 10 primeiras (maiores distâncias)
                ("BACKGROUND", (0, 1), (-1, 10), colors.HexColor("#FADBD8")),
                ("TEXTCOLOR", (0, 1), (-1, 10), colors.HexColor("#922B21")),
                ("FONTNAME", (0, 1), (-1, 10), "Helvetica-Bold"),
            ]
        )

        tabela.setStyle(estilo_tabela)
        return tabela

    def criar_capa_melhorada(self, story, df):
        """Cria uma capa melhorada"""

        # Título principal
        titulo = Paragraph(
            "📊 RELATÓRIO DETALHADO DE DISTÂNCIAS", self.styles["TituloPrincipal"]
        )
        story.append(titulo)
        story.append(Spacer(1, 20))

        # Subtítulo
        subtitulo = Paragraph(
            "Sistema de Gestão de Escolas Indígenas, Quilombolas e Assentamentos",
            self.styles["Subtitulo"],
        )
        story.append(subtitulo)
        story.append(Spacer(1, 30))

        # Informações gerais em destaque
        info_box = f"""
        <para alignment="center" fontSize="14" textColor="#2874A6" fontName="Helvetica-Bold">
        🎯 ANÁLISE ORDENADA POR MAIORES DISTÂNCIAS<br/>
        📅 Data do Relatório: {datetime.now().strftime('%d/%m/%Y às %H:%M')}<br/>
        📊 Total de Escolas Analisadas: {len(df)}<br/>
        🎲 Metodologia: Fórmula Haversine (Precisão Geodésica)<br/>
        📈 Ordenação: Maior para Menor Distância
        </para>
        """
        story.append(Paragraph(info_box, self.styles["TextoNormal"]))
        story.append(Spacer(1, 40))

        # Estatísticas principais
        df_num = df.copy()
        df_num["Distancia_Numerica"] = df_num["Distancia_KM"].apply(
            lambda x: float(x) if pd.notna(x) and x != "N/A" else 0
        )

        dist_max = df_num["Distancia_Numerica"].max()
        dist_min = df_num["Distancia_Numerica"].min()
        dist_media = df_num["Distancia_Numerica"].mean()

        indigenas = len(df[df["Tipo_Escola"] == "Indígena"])
        quilombolas = len(df[df["Tipo_Escola"] == "Quilombola/Assentamento"])

        alta = len(df[df["Distancia_KM"] >= 80])
        media = len(df[(df["Distancia_KM"] >= 50) & (df["Distancia_KM"] < 80)])
        baixa = len(df[df["Distancia_KM"] < 50])

        stats_texto = f"""
        <para fontSize="12" fontName="Helvetica" alignment="left">
        <b>📈 ESTATÍSTICAS PRINCIPAIS:</b><br/>
        <br/>
        🎯 <b>Distâncias:</b><br/>
        • Maior distância: {dist_max:.1f} km<br/>
        • Menor distância: {dist_min:.1f} km<br/>
        • Distância média: {dist_media:.1f} km<br/>
        <br/>
        🏛️ <b>Tipos de Escola:</b><br/>
        • Escolas Indígenas: {indigenas} ({indigenas/len(df)*100:.1f}%)<br/>
        • Escolas Quilombolas/Assentamentos: {quilombolas} ({quilombolas/len(df)*100:.1f}%)<br/>
        <br/>
        🎯 <b>Classificação por Distância:</b><br/>
        • 🔴 Alta (≥80km): {alta} escolas ({alta/len(df)*100:.1f}%)<br/>
        • 🟠 Média (50-79km): {media} escolas ({media/len(df)*100:.1f}%)<br/>
        • 🟢 Baixa (<50km): {baixa} escolas ({baixa/len(df)*100:.1f}%)<br/>
        </para>
        """
        story.append(Paragraph(stats_texto, self.styles["TextoNormal"]))
        story.append(PageBreak())

    def gerar_relatorio(self):
        """Gera o relatório PDF melhorado"""

        print("📊 Iniciando geração do relatório PDF melhorado...")

        # Carregar dados
        arquivo_excel = (
            "dados/excel/distancias_escolas_diretorias_completo_63_corrigido.xlsx"
        )
        if not os.path.exists(arquivo_excel):
            print(f"❌ Arquivo não encontrado: {arquivo_excel}")
            return None

        df = pd.read_excel(arquivo_excel)
        print(f"✅ Dados carregados: {len(df)} escolas")

        # Criar gráficos das maiores distâncias
        print("📈 Criando gráficos das maiores distâncias...")
        df_ordenado = self.criar_graficos_maiores_distancias(df)

        # Configurar arquivo PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorios/pdf/Relatorio_Distancias_Ordenado_{timestamp}.pdf"

        # Usar formato paisagem para melhor visualização
        doc = SimpleDocTemplate(
            nome_arquivo,
            pagesize=landscape(A4),
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
        )

        story = []

        # Criar capa
        print("📋 Criando capa...")
        self.criar_capa_melhorada(story, df)

        # Página de gráficos
        print("📈 Adicionando gráficos...")

        # Título da seção de gráficos
        titulo_graficos = Paragraph(
            "📊 ANÁLISE GRÁFICA DAS MAIORES DISTÂNCIAS", self.styles["TituloPrincipal"]
        )
        story.append(titulo_graficos)
        story.append(Spacer(1, 20))

        # Adicionar gráficos
        graficos = [
            (
                "relatorios/graficos/top_15_maiores_distancias.png",
                "Top 15 Escolas com Maiores Distâncias",
            ),
            (
                "relatorios/graficos/distribuicao_distancias.png",
                "Distribuição e Classificação das Distâncias",
            ),
            (
                "relatorios/graficos/diretorias_maiores_distancias.png",
                "Diretorias com Maiores Distâncias Médias",
            ),
        ]

        for caminho_grafico, legenda in graficos:
            if os.path.exists(caminho_grafico):
                # Adicionar legenda
                story.append(Paragraph(f"<b>{legenda}</b>", self.styles["Subtitulo"]))
                story.append(Spacer(1, 10))

                # Adicionar imagem
                img = Image(caminho_grafico, width=10 * inch, height=6 * inch)
                story.append(img)
                story.append(Spacer(1, 20))

        story.append(PageBreak())

        # Página da tabela ordenada
        print("📋 Criando tabela ordenada...")

        titulo_tabela = Paragraph(
            "📊 ESCOLAS ORDENADAS POR DISTÂNCIA (MAIOR → MENOR)",
            self.styles["TituloPrincipal"],
        )
        story.append(titulo_tabela)
        story.append(Spacer(1, 15))

        # Nota explicativa
        nota = Paragraph(
            "<b>Nota:</b> As escolas estão ordenadas da maior para a menor distância. "
            "As 10 primeiras escolas (destacadas em vermelho) são as que estão mais distantes "
            "de suas diretorias responsáveis e merecem atenção especial para logística de transporte.",
            self.styles["TextoNormal"],
        )
        story.append(nota)
        story.append(Spacer(1, 15))

        # Tabela melhorada
        tabela = self.criar_tabela_melhorada(df_ordenado)
        story.append(tabela)

        # Gerar PDF
        print("💾 Salvando arquivo PDF...")
        doc.build(story)

        print(f"✅ Relatório PDF melhorado criado: {nome_arquivo}")

        # Estatísticas finais
        print(f"\n📊 ESTATÍSTICAS DO RELATÓRIO:")
        print(f"   📋 Total de escolas: {len(df)}")
        print(f"   📈 Gráficos criados: 3")
        print(
            f"   📊 Escola mais distante: {df_ordenado.iloc[0]['Nome_Escola']} ({df_ordenado.iloc[0]['Distancia_KM']:.1f} km)"
        )
        print(
            f"   📊 Escola mais próxima: {df_ordenado.iloc[-1]['Nome_Escola']} ({df_ordenado.iloc[-1]['Distancia_KM']:.1f} km)"
        )
        print(f"   🎯 Ordenação: Maior para menor distância")
        print(f"   📁 Localização: {nome_arquivo}")

        return nome_arquivo


def main():
    """Função principal"""
    print("=== GERADOR DE RELATÓRIO PDF MELHORADO ===")
    print("🎯 Versão com ordenação por distância e gráficos avançados")
    print()

    try:
        relatorio = RelatorioMelhoradoPDF()
        arquivo_gerado = relatorio.gerar_relatorio()

        if arquivo_gerado:
            print(f"\n🎉 Relatório PDF melhorado gerado com sucesso!")
            print(f"📁 Arquivo: {arquivo_gerado}")
            print(f"\n✨ MELHORIAS IMPLEMENTADAS:")
            print(f"   ✅ Ordenação por distância (maior → menor)")
            print(f"   ✅ Coluna contador (#) para as escolas")
            print(f"   ✅ Gráfico das Top 15 maiores distâncias")
            print(f"   ✅ Gráfico de distribuição de distâncias")
            print(f"   ✅ Gráfico das diretorias com maiores distâncias")
            print(f"   ✅ Destaque visual para as 10 escolas mais distantes")
            print(f"   ✅ Estatísticas detalhadas na capa")
            return True
        else:
            print("❌ Falha na geração do relatório")
            return False

    except Exception as e:
        print(f"❌ Erro ao gerar relatório PDF: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
