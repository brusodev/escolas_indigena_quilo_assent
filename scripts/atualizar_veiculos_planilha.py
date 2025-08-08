# -*- coding: utf-8 -*-
import pandas as pd
import json
import os
from datetime import datetime


def atualizar_dados_veiculos():
    """Atualiza os dados de veículos com base na planilha QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx"""
    print("🔄 ATUALIZANDO DADOS DE VEÍCULOS...")
    print("=" * 60)

    try:
        # 1. Carregar a planilha atualizada
        print("📂 Carregando planilha de veículos...")
        df_veiculos = pd.read_excel(
            "QUANTIDADE DE VEÍCULOS LOCADOS - DIRETORIAS.xlsx")
        print(f"   ✅ {len(df_veiculos)} diretorias carregadas")

        # 2. Processar dados de veículos
        print("\n🚗 Processando dados de veículos...")
        veiculos_por_diretoria = {}
        total_veiculos = 0
        diretorias_com_veiculos = 0

        for _, row in df_veiculos.iterrows():
            diretoria = row["DIRETORIA"]
            s1 = row.get("QUANTIDADE S-1", 0) or 0
            s2 = row.get("QUANTIDADE S-2", 0) or 0
            # Note o espaço no final
            s2_4x4 = row.get("QUANTIDADE S-2 4X4 ", 0) or 0
            total = s1 + s2 + s2_4x4

            veiculos_por_diretoria[diretoria.upper()] = {
                "total": int(total),
                "s1": int(s1),
                "s2": int(s2),
                "s2_4x4": int(s2_4x4),
                "diretoria_original": diretoria,
            }
            total_veiculos += total

            if total > 0:
                diretorias_com_veiculos += 1
                print(
                    f"   ✅ {diretoria}: {total} veículos (S-1: {s1}, S-2: {s2}, S-2 4X4: {s2_4x4})")
            else:
                print(f"   ⭕ {diretoria}: 0 veículos")

        # 3. Salvar dados atualizados
        print(f"\n💾 Salvando dados atualizados...")

        # Backup do arquivo anterior
        if os.path.exists("dados_veiculos_atualizados.json"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"dados_veiculos_backup_{timestamp}.json"
            os.rename("dados_veiculos_atualizados.json", backup_name)
            print(f"   📦 Backup criado: {backup_name}")

        # Salvar novos dados
        with open("dados_veiculos_atualizados.json", "w", encoding="utf-8") as f:
            json.dump(veiculos_por_diretoria, f, ensure_ascii=False, indent=2)
        print("   ✅ dados_veiculos_atualizados.json atualizado")

        # 4. Atualizar estatísticas
        print(f"\n📊 Atualizando estatísticas...")
        try:
            with open("estatisticas_atualizadas.json", "r", encoding="utf-8") as f:
                stats = json.load(f)

            # Atualizar estatísticas de veículos
            stats["total_veiculos"] = total_veiculos
            stats["diretorias_com_veiculos"] = diretorias_com_veiculos
            stats["veiculos_s1"] = sum(v["s1"]
                                       for v in veiculos_por_diretoria.values())
            stats["veiculos_s2"] = sum(v["s2"]
                                       for v in veiculos_por_diretoria.values())
            stats["veiculos_s2_4x4"] = sum(v["s2_4x4"]
                                           for v in veiculos_por_diretoria.values())

            with open("estatisticas_atualizadas.json", "w", encoding="utf-8") as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            print("   ✅ estatisticas_atualizadas.json atualizado")

        except FileNotFoundError:
            print(
                "   ⚠️  Arquivo de estatísticas não encontrado, será criado no próximo processamento completo")

        # 5. Resumo da atualização
        print(f"\n📋 RESUMO DA ATUALIZAÇÃO:")
        print("=" * 40)
        print(f"🚗 Total de veículos: {total_veiculos}")
        print(
            f"   📍 S-1: {sum(v['s1'] for v in veiculos_por_diretoria.values())}")
        print(
            f"   📍 S-2: {sum(v['s2'] for v in veiculos_por_diretoria.values())}")
        print(
            f"   📍 S-2 4X4: {sum(v['s2_4x4'] for v in veiculos_por_diretoria.values())}")
        print(
            f"📍 Diretorias com veículos: {diretorias_com_veiculos}/{len(df_veiculos)}")

        # Listar diretorias com mais veículos
        diretorias_ordenadas = sorted(
            [(d, v["total"], v["diretoria_original"])
             for d, v in veiculos_por_diretoria.items() if v["total"] > 1],
            key=lambda x: x[1],
            reverse=True
        )

        if diretorias_ordenadas:
            print(f"\n🏆 DIRETORIAS COM MAIS VEÍCULOS:")
            for i, (_, total, nome) in enumerate(diretorias_ordenadas[:10], 1):
                print(f"   {i:2d}. {nome}: {total} veículos")

        # Verificar diretorias sem veículos
        diretorias_sem_veiculos = [
            v["diretoria_original"] for v in veiculos_por_diretoria.values() if v["total"] == 0
        ]

        if diretorias_sem_veiculos:
            print(
                f"\n⭕ DIRETORIAS SEM VEÍCULOS ({len(diretorias_sem_veiculos)}):")
            # Mostrar só as primeiras 10
            for diretoria in sorted(diretorias_sem_veiculos)[:10]:
                print(f"   • {diretoria}")
            if len(diretorias_sem_veiculos) > 10:
                print(
                    f"   ... e mais {len(diretorias_sem_veiculos) - 10} diretorias")

        print(f"\n✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar dados de veículos: {e}")
        return False


def atualizar_dashboard():
    """Atualiza o dashboard HTML com os novos dados de veículos"""
    print(f"\n🎨 ATUALIZANDO DASHBOARD...")

    try:
        # Importar e executar o script de atualização do dashboard
        import subprocess
        import sys

        result = subprocess.run([sys.executable, "atualizar_dashboard.py"],
                                capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            print("   ✅ Dashboard atualizado com sucesso!")
            print("   📊 Visualizações atualizadas com novos dados de veículos")
        else:
            print(f"   ⚠️  Aviso ao atualizar dashboard: {result.stderr}")

    except Exception as e:
        print(f"   ❌ Erro ao atualizar dashboard: {e}")


if __name__ == "__main__":
    if atualizar_dados_veiculos():
        atualizar_dashboard()
        print(f"\n🎯 PRÓXIMOS PASSOS:")
        print("   1. Verifique o arquivo dados_veiculos_atualizados.json")
        print("   2. Execute processar_dados_atualizados.py para atualização completa")
        print("   3. Confira o dashboard atualizado em distancias_escolas.html")
