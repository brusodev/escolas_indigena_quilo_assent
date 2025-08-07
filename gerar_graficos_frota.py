# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurar encoding UTF-8 para Windows
if sys.platform.startswith("win"):
    os.environ["PYTHONIOENCODING"] = "utf-8"


def criar_graficos_frota():
    """Cria gráficos para análise visual da frota"""

    print("Gerando gráficos de análise de frota...")

    # Carregar dados da análise
    try:
        df = pd.read_excel(
            "Analise_Integrada_Escolas_Frota_Supervisao.xlsx",
            sheet_name="Análise Integrada",
            header=2,
        )
    except:
        print(
            "❌ Arquivo de análise não encontrado. Execute primeiro a análise integrada."
        )
        return

    # Configurar estilo
    plt.style.use("seaborn-v0_8")
    sns.set_palette("husl")

    # Criar figura com subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(
        "📊 ANÁLISE ESTRATÉGICA DE FROTA - ESCOLAS INDÍGENAS/QUILOMBOLAS",
        fontsize=16,
        fontweight="bold",
    )

    # Gráfico 1: Demanda vs Oferta de Veículos
    ax1 = axes[0, 0]
    diretorias_top = df.nlargest(10, "Diferença").copy()
    diretorias_top = diretorias_top[diretorias_top["Diferença"] > 0]

    if len(diretorias_top) > 0:
        y_pos = np.arange(len(diretorias_top))
        ax1.barh(y_pos, diretorias_top["Diferença"], color="#e74c3c")
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(
            [
                nome[:15] + "..." if len(nome) > 15 else nome
                for nome in diretorias_top["Diretoria"]
            ]
        )
        ax1.set_xlabel("Veículos Necessários")
        ax1.set_title("🚗 TOP Diretorias que Precisam de Veículos")
        ax1.grid(axis="x", alpha=0.3)

        # Adicionar valores nas barras
        for i, v in enumerate(diretorias_top["Diferença"]):
            ax1.text(v + 0.1, i, f"+{int(v)}", va="center", fontweight="bold")

    # Gráfico 2: Distribuição de Escolas Distantes
    ax2 = axes[0, 1]
    df_escolas_dist = df[df["Escolas Distantes (>50km)"] > 0].copy()

    if len(df_escolas_dist) > 0:
        ax2.scatter(
            df_escolas_dist["Total Escolas"],
            df_escolas_dist["Escolas Distantes (>50km)"],
            s=df_escolas_dist["Índice Necessidade"] * 50,
            c=df_escolas_dist["Total Veículos"],
            cmap="RdYlBu_r",
            alpha=0.7,
        )

        ax2.set_xlabel("Total de Escolas")
        ax2.set_ylabel("Escolas Distantes (>50km)")
        ax2.set_title(
            "📍 Relação: Total vs Escolas Distantes\n(Tamanho = Índice Necessidade, Cor = Veículos Atuais)"
        )
        ax2.grid(alpha=0.3)

        # Adicionar colorbar
        plt.colorbar(ax2.collections[0], ax=ax2, label="Veículos Atuais")

    # Gráfico 3: Análise por Região
    ax3 = axes[1, 0]
    if "Região" in df.columns:
        df_regiao = (
            df.groupby("Região")
            .agg(
                {
                    "Total Escolas": "sum",
                    "Escolas Distantes (>50km)": "sum",
                    "Total Veículos": "sum",
                    "Diferença": "sum",
                }
            )
            .reset_index()
        )

        x = np.arange(len(df_regiao))
        width = 0.35

        bars1 = ax3.bar(
            x - width / 2,
            df_regiao["Escolas Distantes (>50km)"],
            width,
            label="Escolas Distantes",
            color="#e74c3c",
            alpha=0.8,
        )
        bars2 = ax3.bar(
            x + width / 2,
            df_regiao["Total Veículos"],
            width,
            label="Veículos Atuais",
            color="#3498db",
            alpha=0.8,
        )

        ax3.set_xlabel("Região")
        ax3.set_ylabel("Quantidade")
        ax3.set_title("🗺️ Análise por Região")
        ax3.set_xticks(x)
        ax3.set_xticklabels(df_regiao["Região"], rotation=45)
        ax3.legend()
        ax3.grid(axis="y", alpha=0.3)

        # Adicionar valores nas barras
        for bar in bars1:
            height = bar.get_height()
            ax3.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.1,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

        for bar in bars2:
            height = bar.get_height()
            ax3.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.1,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    # Gráfico 4: Prioridades de Atendimento
    ax4 = axes[1, 1]
    if "Prioridade" in df.columns:
        prioridades = df["Prioridade"].value_counts()
        colors = {"ALTA": "#e74c3c", "MÉDIA": "#f39c12", "BAIXA": "#27ae60"}
        pie_colors = [colors.get(p, "#95a5a6") for p in prioridades.index]

        wedges, texts, autotexts = ax4.pie(
            prioridades.values,
            labels=prioridades.index,
            autopct="%1.1f%%",
            colors=pie_colors,
            startangle=90,
            explode=(0.1, 0.05, 0),
        )

        ax4.set_title(
            "🚨 Distribuição de Prioridades\n(Baseada na Necessidade de Veículos)"
        )

        # Melhorar aparência do texto
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")

    plt.tight_layout()

    # Salvar gráfico
    arquivo_grafico = "Graficos_Analise_Frota.png"
    plt.savefig(arquivo_grafico, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"✅ Gráficos salvos em: {arquivo_grafico}")

    # Criar gráfico adicional: Mapa de calor de necessidade
    criar_mapa_calor_necessidade(df)

    return arquivo_grafico


def criar_mapa_calor_necessidade(df):
    """Cria mapa de calor da necessidade de veículos"""

    plt.figure(figsize=(14, 8))

    # Preparar dados para o heatmap
    df_pivot = df.pivot_table(
        values=["Escolas Distantes (>50km)", "Total Veículos", "Diferença"],
        index="Diretoria",
        aggfunc="first",
    ).fillna(0)

    # Filtrar apenas diretorias com escolas
    df_pivot = df_pivot[df_pivot["Escolas Distantes (>50km)"] >= 0]

    # Criar heatmap
    sns.heatmap(
        df_pivot.T,
        annot=True,
        fmt=".0f",
        cmap="RdYlBu_r",
        center=0,
        cbar_kws={"label": "Intensidade"},
        linewidths=0.5,
    )

    plt.title(
        "🔥 MAPA DE CALOR: NECESSIDADE DE VEÍCULOS POR DIRETORIA\n"
        "Vermelho = Maior Necessidade | Azul = Situação Adequada",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("Diretorias de Ensino", fontweight="bold")
    plt.ylabel("Métricas", fontweight="bold")
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    arquivo_heatmap = "Mapa_Calor_Necessidade_Veiculos.png"
    plt.savefig(arquivo_heatmap, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"✅ Mapa de calor salvo em: {arquivo_heatmap}")
    return arquivo_heatmap


def main():
    """Executa geração de gráficos"""
    print("📊 Iniciando geração de gráficos de análise de frota...")
    criar_graficos_frota()


if __name__ == "__main__":
    main()
