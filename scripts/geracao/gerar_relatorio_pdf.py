# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, landscape
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
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configurar encoding UTF-8 para Windows
if sys.platform.startswith("win"):
    os.environ["PYTHONIOENCODING"] = "utf-8"


class RelatorioElegantePDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.criar_estilos_customizados()

    def criar_estilos_customizados(self):
        """Cria estilos customizados para o PDF"""

        # Título principal
        self.styles.add(
            ParagraphStyle(
                name="TituloPrincipal",
                parent=self.styles["Title"],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#2C3E50"),
                fontName="Helvetica-Bold",
            )
        )

        # Subtítulo
        self.styles.add(
            ParagraphStyle(
                name="Subtitulo",
                parent=self.styles["Normal"],
                fontSize=14,
                spaceAfter=20,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#7F8C8D"),
                fontName="Helvetica",
            )
        )

        # Cabeçalho de seção
        self.styles.add(
            ParagraphStyle(
                name="CabecalhoSecao",
                parent=self.styles["Heading1"],
                fontSize=16,
                spaceAfter=15,
                spaceBefore=20,
                textColor=colors.HexColor("#2C3E50"),
                fontName="Helvetica-Bold",
            )
        )

        # Texto normal customizado
        self.styles.add(
            ParagraphStyle(
                name="CorpoTexto",
                parent=self.styles["Normal"],
                fontSize=11,
                spaceAfter=12,
                textColor=colors.HexColor("#2C3E50"),
                fontName="Helvetica",
            )
        )

        # Destaque
        self.styles.add(
            ParagraphStyle(
                name="Destaque",
                parent=self.styles["Normal"],
                fontSize=12,
                spaceAfter=12,
                textColor=colors.HexColor("#E74C3C"),
                fontName="Helvetica-Bold",
            )
        )

    def criar_graficos(self, df):
        """Cria gráficos para o relatório"""

        # Configurar estilo dos gráficos
        plt.style.use("seaborn-v0_8")
        sns.set_palette("husl")

        # Gráfico 1: Distribuição por tipo (ajustado para paisagem)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Pizza - Distribuição por tipo
        tipos = df["Tipo_Escola"].value_counts()
        colors_pie = ["#E74C3C", "#27AE60"]
        ax1.pie(
            tipos.values,
            labels=tipos.index,
            autopct="%1.1f%%",
            colors=colors_pie,
            startangle=90,
        )
        ax1.set_title("Distribuição por Tipo de Escola", fontsize=14, fontweight="bold")

        # Histograma - Distribuição de distâncias
        distancias = []
        for dist in df["Distancia_KM"]:
            try:
                if pd.notna(dist) and dist != "N/A":
                    distancias.append(float(dist))
            except:
                continue

        ax2.hist(distancias, bins=15, color="#3498DB", alpha=0.7, edgecolor="black")
        ax2.set_xlabel("Distância (km)", fontsize=12)
        ax2.set_ylabel("Número de Escolas", fontsize=12)
        ax2.set_title("Distribuição das Distâncias", fontsize=14, fontweight="bold")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(
            "relatorios/graficos/graficos_relatorio.png", dpi=300, bbox_inches="tight"
        )
        plt.close()

        # Gráfico 2: Distâncias por diretoria (ajustado para paisagem)
        fig, ax = plt.subplots(1, 1, figsize=(16, 8))

        # Agrupar por diretoria e calcular média
        df_num = df.copy()
        df_num["Distancia_Numerica"] = df_num["Distancia_KM"].apply(
            lambda x: float(x) if pd.notna(x) and x != "N/A" else 0
        )

        diretorias_dist = (
            df_num.groupby("DE_Responsavel")
            .agg({"Distancia_Numerica": "mean", "Nome_Escola": "count"})
            .round(2)
        )

        # Top 10 diretorias com maior distância média
        top_diretorias = diretorias_dist.nlargest(10, "Distancia_Numerica")

        bars = ax.barh(
            range(len(top_diretorias)),
            top_diretorias["Distancia_Numerica"],
            color="#E67E22",
            alpha=0.8,
        )
        ax.set_yticks(range(len(top_diretorias)))
        ax.set_yticklabels(
            [
                name[:25] + "..." if len(name) > 25 else name
                for name in top_diretorias.index
            ],
            fontsize=10,
        )
        ax.set_xlabel("Distância Média (km)", fontsize=12)
        ax.set_title(
            "Top 10 Diretorias - Maior Distância Média", fontsize=14, fontweight="bold"
        )
        ax.grid(True, alpha=0.3, axis="x")

        # Adicionar valores nas barras
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(
                width + 1,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}km",
                ha="left",
                va="center",
                fontsize=9,
            )

        plt.tight_layout()
        plt.savefig(
            "relatorios/graficos/diretorias_distancias.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()

    def criar_capa(self, story, df):
        """Cria a capa do relatório"""

        # Título principal
        titulo = Paragraph("RELATÓRIO DETALHADO", self.styles["TituloPrincipal"])
        story.append(titulo)

        # Subtítulo
        subtitulo = Paragraph(
            "Distâncias entre Escolas Indígenas, Quilombolas e de Assentamentos<br/>e suas Diretorias de Ensino",
            self.styles["Subtitulo"],
        )
        story.append(subtitulo)

        story.append(Spacer(1, 0.5 * inch))

        # Informações gerais
        total_escolas = len(df)
        total_indigena = len(df[df["Tipo_Escola"] == "Indígena"])
        total_quilombola = len(df[df["Tipo_Escola"] == "Quilombola/Assentamento"])

        # Calcular estatísticas
        distancias = []
        for dist in df["Distancia_KM"]:
            try:
                if pd.notna(dist) and dist != "N/A":
                    distancias.append(float(dist))
            except:
                continue

        media_dist = sum(distancias) / len(distancias) if distancias else 0

        info_data = [
            ["INFORMAÇÕES GERAIS", ""],
            ["Estado", "São Paulo"],
            ["Data do Relatório", datetime.now().strftime("%d/%m/%Y")],
            ["Total de Escolas Analisadas", f"{total_escolas}"],
            ["Escolas Indígenas", f"{total_indigena}"],
            ["Escolas Quilombolas/Assentamentos", f"{total_quilombola}"],
            ["Distância Média", f"{media_dist:.2f} km"],
            ["Período de Análise", "Junho 2025"],
        ]

        info_table = Table(info_data, colWidths=[3 * inch, 2 * inch])
        info_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#2C3E50")),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ECF0F1")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#BDC3C7")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )

        story.append(info_table)
        story.append(Spacer(1, 0.5 * inch))

        # Observações atualizadas com metodologia Haversine
        observacoes = Paragraph(
            "<b>📐 Metodologia de Cálculo - Fórmula de Haversine:</b><br/>"
            "• Distâncias calculadas com fórmula de Haversine (padrão geodésico internacional)<br/>"
            "• Considera a curvatura real da Terra - precisão científica<br/>"
            "• Sistema de coordenadas WGS84 em graus decimais<br/>"
            "• 100% das distâncias validadas automaticamente<br/>"
            "• Diferenças com Google Maps são normais (Haversine = linha reta, Maps = rodoviária)<br/>"
            "• Escolas filtradas por TIPOESC = 10 (Indígenas) e TIPOESC = 36 (Quilombolas/Assentamentos)<br/>"
            f"• Data de validação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            self.styles["CorpoTexto"],
        )
        story.append(observacoes)

    def criar_secao_estatisticas(self, story, df):
        """Cria seção com estatísticas detalhadas"""

        story.append(PageBreak())

        # Título da seção
        titulo = Paragraph("ANÁLISE ESTATÍSTICA", self.styles["CabecalhoSecao"])
        story.append(titulo)

        # Gráficos (ajustados para paisagem)
        if os.path.exists("graficos_relatorio.png"):
            img = Image("graficos_relatorio.png", width=10 * inch, height=3.8 * inch)
            story.append(img)
            story.append(Spacer(1, 0.3 * inch))

        # Estatísticas por tipo
        estatisticas_texto = []

        # Indígenas
        df_indigena = df[df["Tipo_Escola"] == "Indígena"]
        dist_indigena = [
            float(d) for d in df_indigena["Distancia_KM"] if pd.notna(d) and d != "N/A"
        ]

        if dist_indigena:
            estatisticas_texto.append(
                f"<b>Escolas Indígenas ({len(df_indigena)} escolas):</b>"
            )
            estatisticas_texto.append(
                f"• Distância média: {sum(dist_indigena)/len(dist_indigena):.2f} km"
            )
            estatisticas_texto.append(
                f"• Distância mínima: {min(dist_indigena):.2f} km"
            )
            estatisticas_texto.append(
                f"• Distância máxima: {max(dist_indigena):.2f} km"
            )
            estatisticas_texto.append("")

        # Quilombolas
        df_quilombola = df[df["Tipo_Escola"] == "Quilombola/Assentamento"]
        dist_quilombola = [
            float(d)
            for d in df_quilombola["Distancia_KM"]
            if pd.notna(d) and d != "N/A"
        ]

        if dist_quilombola:
            estatisticas_texto.append(
                f"<b>Escolas Quilombolas/Assentamentos ({len(df_quilombola)} escolas):</b>"
            )
            estatisticas_texto.append(
                f"• Distância média: {sum(dist_quilombola)/len(dist_quilombola):.2f} km"
            )
            estatisticas_texto.append(
                f"• Distância mínima: {min(dist_quilombola):.2f} km"
            )
            estatisticas_texto.append(
                f"• Distância máxima: {max(dist_quilombola):.2f} km"
            )

        texto_stats = Paragraph(
            "<br/>".join(estatisticas_texto), self.styles["CorpoTexto"]
        )
        story.append(texto_stats)

        # Gráfico de diretorias (ajustado para paisagem)
        if os.path.exists("diretorias_distancias.png"):
            story.append(Spacer(1, 0.3 * inch))
            img2 = Image("diretorias_distancias.png", width=10 * inch, height=5 * inch)
            story.append(img2)

    def criar_tabela_escolas(self, story, df, titulo, filtro_tipo=None):
        """Cria tabela com dados das escolas"""

        # Filtrar dados se necessário
        if filtro_tipo:
            df_filtrado = df[df["Tipo_Escola"] == filtro_tipo].copy()
        else:
            df_filtrado = df.copy()

        if len(df_filtrado) == 0:
            return

        # Título da seção
        titulo_secao = Paragraph(titulo, self.styles["CabecalhoSecao"])
        story.append(titulo_secao)

        # Preparar dados para tabela (mais colunas na paisagem)
        dados_tabela = [
            ["Escola", "Cidade", "Diretoria", "Distância\n(km)", "Zona", "Status"]
        ]

        for _, row in df_filtrado.iterrows():
            try:
                dist = (
                    float(row["Distancia_KM"])
                    if pd.notna(row["Distancia_KM"]) and row["Distancia_KM"] != "N/A"
                    else 0
                )

                if dist > 100:
                    status = "⚠️ Alta"
                elif dist < 20:
                    status = "✅ Baixa"
                else:
                    status = "📍 Média"

                nome_escola = (
                    row["Nome_Escola"][:45] + "..."
                    if len(row["Nome_Escola"]) > 45
                    else row["Nome_Escola"]
                )

                dados_tabela.append(
                    [
                        nome_escola,
                        row["Cidade_Escola"],
                        (
                            row["DE_Responsavel"][:25] + "..."
                            if len(row["DE_Responsavel"]) > 25
                            else row["DE_Responsavel"]
                        ),
                        f"{dist:.1f}" if dist > 0 else "N/A",
                        row["Zona"],
                        status,
                    ]
                )
            except:
                continue

        # Criar tabela com mais colunas para paisagem
        table = Table(
            dados_tabela,
            colWidths=[
                3.5 * inch,
                1.5 * inch,
                2 * inch,
                1 * inch,
                1 * inch,
                1.5 * inch,
            ],
        )

        # Estilo da tabela
        table_style = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495E")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#BDC3C7")),
        ]

        # Colorir linhas alternadas
        for i in range(1, len(dados_tabela)):
            if i % 2 == 0:
                table_style.append(
                    ("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F8F9FA"))
                )

        table.setStyle(TableStyle(table_style))
        story.append(table)
        story.append(Spacer(1, 0.2 * inch))

    def gerar_relatorio(self):
        """Gera o relatório PDF completo"""

        print("=== GERADOR DE RELATÓRIO PDF DETALHADO ===")
        print("Gerando Relatório PDF Detalhado...")

        # Ler dados
        df = pd.read_excel(
            "dados/excel/distancias_escolas_diretorias_completo_63_corrigido.xlsx"
        )

        # Criar gráficos
        self.criar_graficos(df)

        # Configurar documento em paisagem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_nome = f"relatorios/pdf/Relatorio_Paisagem_Escolas_{timestamp}.pdf"
        doc = SimpleDocTemplate(
            arquivo_nome,
            pagesize=landscape(A4),
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50,
        )

        story = []

        # Criar seções
        self.criar_capa(story, df)
        self.criar_secao_estatisticas(story, df)

        story.append(PageBreak())
        self.criar_tabela_escolas(story, df, "ESCOLAS INDÍGENAS", "Indígena")

        story.append(PageBreak())
        self.criar_tabela_escolas(
            story,
            df,
            "ESCOLAS QUILOMBOLAS E DE ASSENTAMENTOS",
            "Quilombola/Assentamento",
        )

        # Gerar PDF
        doc.build(story)

        # Limpar arquivos temporários
        for arquivo in ["graficos_relatorio.png", "diretorias_distancias.png"]:
            if os.path.exists(arquivo):
                os.remove(arquivo)

        print(f"✅ Relatório PDF criado: {arquivo_nome}")
        return arquivo_nome


def main():
    print("=== GERADOR DE RELATÓRIO PDF DETALHADO ===\n")

    try:
        relatorio = RelatorioElegantePDF()
        arquivo_gerado = relatorio.gerar_relatorio()

        print(f"\n🎉 Relatório PDF gerado com sucesso!")
        print(f"Arquivo: {arquivo_gerado}")
        print("\nO relatório inclui:")
        print("• Capa com informações gerais")
        print("• Análise estatística com gráficos")
        print("• Tabelas detalhadas por tipo de escola")
        print("• Layout profissional para impressão")
        print("• Indicadores visuais de status")

    except Exception as e:
        print(f"❌ Erro ao gerar relatório PDF: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
