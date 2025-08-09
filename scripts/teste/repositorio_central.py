#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REPOSITÓRIO CENTRAL - VALIDADOR E SINCRONIZADOR DE DADOS
Mantém a integridade entre Dashboard, Excel e Relatórios
"""

import pandas as pd
import json
import os
import re
from datetime import datetime
import shutil


class RepositorioCentral:
    """Classe para gerenciar repositórios centralizados do sistema"""

    def __init__(self):
        # Arquivos principais (fonte única da verdade)
        self.arquivo_principal = (
            "distancias_escolas_diretorias_completo_63_corrigido.xlsx"
        )
        self.arquivo_veiculos = "dados_veiculos_diretorias.json"
        self.arquivo_dashboard = "dashboard_integrado.html"

        # Arquivos de relatórios (gerados)
        self.relatorio_excel = "Relatorio_Completo_Escolas_Diretorias.xlsx"

        # Configurações de validação
        self.total_escolas_esperado = 63
        self.total_veiculos_esperado = 172
        self.distancia_kopenoti_esperada = 27.16

    def validar_integridade_completa(self):
        """Executa validação completa de todos os repositórios"""
        print("🔍 VALIDAÇÃO COMPLETA DOS REPOSITÓRIOS")
        print("=" * 70)
        print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()

        resultados = {
            "arquivo_principal": self._validar_arquivo_principal(),
            "arquivo_veiculos": self._validar_arquivo_veiculos(),
            "dashboard": self._validar_dashboard(),
            "sincronizacao": self._validar_sincronizacao(),
        }

        self._gerar_relatorio_validacao(resultados)
        return all(resultados.values())

    def _validar_arquivo_principal(self):
        """Valida o arquivo Excel principal"""
        print("📊 VALIDANDO ARQUIVO PRINCIPAL")
        print("-" * 50)

        if not os.path.exists(self.arquivo_principal):
            print(f"❌ Arquivo não encontrado: {self.arquivo_principal}")
            return False

        try:
            df = pd.read_excel(self.arquivo_principal)

            # Validar número total de escolas
            if len(df) != self.total_escolas_esperado:
                print(
                    f"❌ Total de escolas incorreto: {len(df)} (esperado: {self.total_escolas_esperado})"
                )
                return False

            print(f"✅ Total de escolas: {len(df)}")

            # Validar KOPENOTI
            kopenoti = df[
                df["Nome_Escola"].str.contains("KOPENOTI", na=False, case=False)
            ]
            if kopenoti.empty:
                print("❌ KOPENOTI não encontrado")
                return False

            distancia = kopenoti.iloc[0]["Distancia_KM"]
            if abs(distancia - self.distancia_kopenoti_esperada) > 0.1:
                print(
                    f"❌ Distância KOPENOTI incorreta: {distancia:.2f} (esperado: {self.distancia_kopenoti_esperada})"
                )
                return False

            print(f"✅ KOPENOTI: {distancia:.2f} km")

            # Validar colunas obrigatórias
            colunas_obrigatorias = [
                "Nome_Escola",
                "Tipo_Escola",
                "Cidade_Escola",
                "Latitude_Escola",
                "Longitude_Escola",
                "Nome_Diretoria",
                "Distancia_KM",
            ]

            for col in colunas_obrigatorias:
                if col not in df.columns:
                    print(f"❌ Coluna obrigatória ausente: {col}")
                    return False

                nans = df[col].isna().sum()
                if nans > 0:
                    print(f"⚠️  {nans} valores NaN em {col}")

            # Validar tipos de escola
            tipos = df["Tipo_Escola"].value_counts()
            print(f"📋 Tipos de escola:")
            for tipo, count in tipos.items():
                print(f"   {tipo}: {count}")

            # Validar diretorias
            diretorias = df["Nome_Diretoria"].nunique()
            print(f"🏢 Diretorias únicas: {diretorias}")

            print("✅ Arquivo principal validado com sucesso")
            return True

        except Exception as e:
            print(f"❌ Erro ao validar arquivo principal: {e}")
            return False

    def _validar_arquivo_veiculos(self):
        """Valida o arquivo JSON de veículos"""
        print(f"\n🚗 VALIDANDO ARQUIVO DE VEÍCULOS")
        print("-" * 50)

        if not os.path.exists(self.arquivo_veiculos):
            print(f"❌ Arquivo não encontrado: {self.arquivo_veiculos}")
            return False

        try:
            with open(self.arquivo_veiculos, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validar estrutura
            if "metadata" not in data:
                print("❌ Metadata não encontrada")
                return False

            metadata = data["metadata"]
            total_veiculos = metadata.get("total_veiculos", 0)

            if total_veiculos != self.total_veiculos_esperado:
                print(
                    f"❌ Total de veículos incorreto: {total_veiculos} (esperado: {self.total_veiculos_esperado})"
                )
                return False

            print(f"✅ Total de veículos: {total_veiculos}")

            # Validar diretorias
            if "diretorias" in data:
                diretorias_com_veiculos = len(data["diretorias"])
                print(f"🏢 Diretorias com dados de veículos: {diretorias_com_veiculos}")

            print("✅ Arquivo de veículos validado com sucesso")
            return True

        except Exception as e:
            print(f"❌ Erro ao validar arquivo de veículos: {e}")
            return False

    def _validar_dashboard(self):
        """Valida o dashboard HTML"""
        print(f"\n🌐 VALIDANDO DASHBOARD")
        print("-" * 50)

        if not os.path.exists(self.arquivo_dashboard):
            print(f"❌ Arquivo não encontrado: {self.arquivo_dashboard}")
            return False

        try:
            with open(self.arquivo_dashboard, "r", encoding="utf-8") as f:
                content = f.read()

            # Contar escolas no dashboard
            match = re.search(r"const schoolsData = \[(.*?)\];", content, re.DOTALL)
            if not match:
                print("❌ schoolsData não encontrado no dashboard")
                return False

            schools_text = match.group(1)
            school_count = schools_text.count("{")

            if school_count != self.total_escolas_esperado:
                print(
                    f"❌ Escolas no dashboard: {school_count} (esperado: {self.total_escolas_esperado})"
                )
                return False

            print(f"✅ Escolas no dashboard: {school_count}")

            # Verificar se KOPENOTI está presente
            if "KOPENOTI" not in content:
                print("❌ KOPENOTI não encontrado no dashboard")
                return False

            print("✅ KOPENOTI presente no dashboard")

            print("✅ Dashboard validado com sucesso")
            return True

        except Exception as e:
            print(f"❌ Erro ao validar dashboard: {e}")
            return False

    def _validar_sincronizacao(self):
        """Valida sincronização entre sistemas"""
        print(f"\n🔄 VALIDANDO SINCRONIZAÇÃO")
        print("-" * 50)

        try:
            # Extrair nomes das escolas do Excel
            df = pd.read_excel(self.arquivo_principal)
            escolas_excel = set(df["Nome_Escola"].str.upper().str.strip())

            # Extrair nomes das escolas do dashboard
            with open(self.arquivo_dashboard, "r", encoding="utf-8") as f:
                content = f.read()

            match = re.search(r"const schoolsData = \[(.*?)\];", content, re.DOTALL)
            schools_text = match.group(1)

            # Extrair nomes usando regex
            name_matches = re.findall(r'"name":\s*"([^"]+)"', schools_text)
            escolas_dashboard = set(nome.upper().strip() for nome in name_matches)

            # Comparar
            diferenca_excel = escolas_excel - escolas_dashboard
            diferenca_dashboard = escolas_dashboard - escolas_excel

            if diferenca_excel:
                print(
                    f"❌ Escolas no Excel mas não no dashboard ({len(diferenca_excel)}):"
                )
                for escola in sorted(list(diferenca_excel)[:5]):
                    print(f"   - {escola}")
                return False

            if diferenca_dashboard:
                print(
                    f"❌ Escolas no dashboard mas não no Excel ({len(diferenca_dashboard)}):"
                )
                for escola in sorted(list(diferenca_dashboard)[:5]):
                    print(f"   - {escola}")
                return False

            print("✅ Dashboard e Excel perfeitamente sincronizados")
            print(f"✅ {len(escolas_excel)} escolas idênticas em ambos os sistemas")

            return True

        except Exception as e:
            print(f"❌ Erro ao validar sincronização: {e}")
            return False

    def _gerar_relatorio_validacao(self, resultados):
        """Gera relatório final de validação"""
        print(f"\n🎯 RELATÓRIO FINAL DE VALIDAÇÃO")
        print("=" * 70)

        total_testes = len(resultados)
        testes_aprovados = sum(resultados.values())

        print(f"📊 Testes executados: {total_testes}")
        print(f"✅ Testes aprovados: {testes_aprovados}")
        print(f"❌ Testes falharam: {total_testes - testes_aprovados}")
        print(f"📈 Taxa de sucesso: {(testes_aprovados/total_testes)*100:.1f}%")

        print(f"\n📋 DETALHAMENTO:")
        for teste, resultado in resultados.items():
            status = "✅ APROVADO" if resultado else "❌ FALHOU"
            print(f"   {teste.replace('_', ' ').title()}: {status}")

        if all(resultados.values()):
            print(f"\n🎉 TODOS OS REPOSITÓRIOS ESTÃO ÍNTEGROS E SINCRONIZADOS!")
            print(f"🚀 Sistema pronto para uso em produção")
        else:
            print(f"\n⚠️  AÇÃO NECESSÁRIA: Corrigir falhas antes de usar em produção")
            print(f"💡 Execute os scripts de correção apropriados")

    def criar_backup_repositorios(self):
        """Cria backup dos repositórios principais"""
        print(f"💾 CRIANDO BACKUP DOS REPOSITÓRIOS")
        print("-" * 50)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"backup_{timestamp}"

        try:
            os.makedirs(backup_dir, exist_ok=True)

            arquivos_backup = [
                self.arquivo_principal,
                self.arquivo_veiculos,
                self.arquivo_dashboard,
            ]

            for arquivo in arquivos_backup:
                if os.path.exists(arquivo):
                    destino = os.path.join(backup_dir, arquivo)
                    shutil.copy2(arquivo, destino)
                    print(f"✅ {arquivo} → {destino}")
                else:
                    print(f"⚠️  {arquivo} não encontrado para backup")

            print(f"💾 Backup criado em: {backup_dir}")
            return backup_dir

        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return None

    def gerar_resumo_configuracao(self):
        """Gera resumo da configuração atual"""
        print(f"\n⚙️  CONFIGURAÇÃO ATUAL DO SISTEMA")
        print("=" * 70)

        config = {
            "Arquivo Principal": self.arquivo_principal,
            "Arquivo Veículos": self.arquivo_veiculos,
            "Dashboard": self.arquivo_dashboard,
            "Total Escolas Esperado": self.total_escolas_esperado,
            "Total Veículos Esperado": self.total_veiculos_esperado,
            "Distância KOPENOTI": f"{self.distancia_kopenoti_esperada} km",
        }

        for chave, valor in config.items():
            print(f"📋 {chave}: {valor}")


def main():
    """Função principal"""
    print("🏛️  REPOSITÓRIO CENTRAL - VALIDADOR DE INTEGRIDADE")
    print("=" * 70)

    repo = RepositorioCentral()

    # Gerar resumo da configuração
    repo.gerar_resumo_configuracao()

    # Criar backup antes da validação
    backup_dir = repo.criar_backup_repositorios()

    # Executar validação completa
    integridade_ok = repo.validar_integridade_completa()

    if integridade_ok:
        print(f"\n🎯 PRÓXIMOS PASSOS RECOMENDADOS:")
        print(f"   1. ✅ Repositórios validados e íntegros")
        print(f"   2. 🚀 Sistema pronto para geração de relatórios")
        print(f"   3. 📊 Execute: python atualizar_relatorios_completos.py")
        print(f"   4. 💾 Backup disponível em: {backup_dir}")
    else:
        print(f"\n⚠️  AÇÕES NECESSÁRIAS:")
        print(f"   1. 🔧 Corrigir falhas identificadas")
        print(f"   2. 🔄 Executar validação novamente")
        print(f"   3. 💾 Restaurar backup se necessário: {backup_dir}")


if __name__ == "__main__":
    main()
