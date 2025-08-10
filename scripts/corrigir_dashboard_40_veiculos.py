import json
import os
import shutil
from datetime import datetime


def fazer_backup():
    """Faz backup dos arquivos antes de alterar"""
    print("🛡️ Fazendo backup dos arquivos...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"dados/json/old/backup_correcao_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)

    arquivos_backup = [
        'static/js/dash.js',
        'dados/json/estatisticas_atualizadas.json',
        'README.md'
    ]

    for arquivo in arquivos_backup:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, backup_dir)
            print(f"✅ Backup: {arquivo}")

    print(f"🛡️ Backup completo em: {backup_dir}")
    return backup_dir


def calcular_veiculos_corretos():
    """Calcula o número correto de veículos nas diretorias com escolas"""
    print("📊 Calculando veículos corretos...")

    try:
        # Carregar dados de escolas
        with open('dados/json/dados_escolas_atualizados.json', 'r', encoding='utf-8') as f:
            escolas = json.load(f)

        # Carregar dados de veículos
        with open('dados_veiculos_diretorias.json', 'r', encoding='utf-8') as f:
            veiculos = json.load(f)

        # Calcular estatísticas
        total_escolas = len(escolas)
        indigenas = len([e for e in escolas if e['Tipo_Escola'] == 'Indígena'])
        quilombolas = len(
            [e for e in escolas if e['Tipo_Escola'] == 'Quilombola/Assentamento'])

        # Identificar diretorias que atendem escolas
        diretorias_com_escolas = set(
            escola['DE_Responsavel'] for escola in escolas)
        total_veiculos_relevantes = 0
        detalhamento = {}

        print(
            f"📋 Diretorias que atendem escolas: {len(diretorias_com_escolas)}")

        for diretoria in sorted(diretorias_com_escolas):
            diretoria_key = diretoria.upper()
            if diretoria_key in veiculos['diretorias']:
                qtd_veiculos = veiculos['diretorias'][diretoria_key]['total']
                total_veiculos_relevantes += qtd_veiculos
                detalhamento[diretoria] = qtd_veiculos
                print(f"   • {diretoria}: {qtd_veiculos} veículos")
            else:
                print(f"   ❌ {diretoria}: DIRETORIA NÃO ENCONTRADA")

        print(f"\n🎯 TOTAL DE VEÍCULOS CORRETO: {total_veiculos_relevantes}")

        # Calcular outras estatísticas
        distancia_media = sum(e['Distancia_KM']
                              for e in escolas) / len(escolas)
        escolas_acima_50 = len([e for e in escolas if e['Distancia_KM'] > 50])

        # Retornar dados calculados
        return {
            "total_escolas": total_escolas,
            "escolas_indigenas": indigenas,
            "escolas_quilombolas": quilombolas,
            "total_diretorias": len(diretorias_com_escolas),
            "total_veiculos_diretorias_escolas": total_veiculos_relevantes,
            "distancia_media_km": round(distancia_media, 2),
            "escolas_acima_50km": escolas_acima_50,
            "detalhamento_veiculos": detalhamento
        }

    except Exception as e:
        print(f"❌ Erro ao calcular veículos: {e}")
        return None


def corrigir_dashboard_js(total_veiculos):
    """Corrige o arquivo dash.js para mostrar o número correto de veículos"""
    print("🔧 Corrigindo dashboard JavaScript...")

    try:
        with open('static/js/dash.js', 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # Buscar e substituir diferentes padrões que podem conter o valor incorreto
        padroes_incorretos = [
            'const totalVehicles = 6;',
            'totalVehicles = 6;',
            'let totalVehicles = 6;',
            'var totalVehicles = 6;'
        ]

        correcoes_feitas = 0
        for padrao in padroes_incorretos:
            if padrao in conteudo:
                novo_padrao = padrao.replace('6', str(total_veiculos))
                conteudo = conteudo.replace(
                    padrao, f"{novo_padrao} // CORRIGIDO")
                correcoes_feitas += 1
                print(f"✅ Corrigido: {padrao} → {novo_padrao}")

        # Salvar arquivo corrigido
        with open('static/js/dash.js', 'w', encoding='utf-8') as f:
            f.write(conteudo)

        print(f"✅ Dashboard corrigido: {correcoes_feitas} alterações feitas")
        return True

    except Exception as e:
        print(f"❌ Erro ao corrigir dashboard: {e}")
        return False


def criar_estatisticas_atualizadas(dados):
    """Cria ou atualiza o arquivo de estatísticas"""
    print("📈 Criando arquivo de estatísticas atualizado...")

    try:
        stats = {
            "ultima_atualizacao": datetime.now().isoformat(),
            "total_escolas": dados["total_escolas"],
            "escolas_indigenas": dados["escolas_indigenas"],
            "escolas_quilombolas": dados["escolas_quilombolas"],
            "total_diretorias": dados["total_diretorias"],
            "total_veiculos_diretorias_escolas": dados["total_veiculos_diretorias_escolas"],
            "distancia_media_km": dados["distancia_media_km"],
            "escolas_acima_50km": dados["escolas_acima_50km"],
            "metodologia": "Haversine",
            "precisao": "±0.1km",
            "status_sistema": "Corrigido automaticamente",
            "versao": "1.6_corrigida",
            "detalhes_correcao": {
                "data_correcao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "problemas_corrigidos": [
                    f"Dashboard: 6 → {dados['total_veiculos_diretorias_escolas']} veículos",
                    "Estatísticas JSON atualizadas",
                    "Backup automático criado"
                ],
                "detalhamento_veiculos": dados["detalhamento_veiculos"]
            }
        }

        # Salvar estatísticas
        os.makedirs('dados/json', exist_ok=True)
        with open('dados/json/estatisticas_atualizadas.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        print("✅ Arquivo de estatísticas criado/atualizado")
        return True

    except Exception as e:
        print(f"❌ Erro ao criar estatísticas: {e}")
        return False


def validar_correcoes(total_veiculos_esperado):
    """Valida se as correções foram aplicadas corretamente"""
    print("🔍 Validando correções...")

    sucesso = True

    # Verificar dashboard
    try:
        with open('static/js/dash.js', 'r', encoding='utf-8') as f:
            conteudo = f.read()

        if f'totalVehicles = {total_veiculos_esperado}' in conteudo:
            print(
                f"✅ Dashboard: {total_veiculos_esperado} veículos confirmados")
        else:
            print(f"❌ Dashboard: Ainda não corrigido")
            sucesso = False
    except:
        print("❌ Dashboard: Erro ao verificar")
        sucesso = False

    # Verificar estatísticas
    try:
        with open('dados/json/estatisticas_atualizadas.json', 'r', encoding='utf-8') as f:
            stats = json.load(f)

        if stats.get('total_veiculos_diretorias_escolas') == total_veiculos_esperado:
            print(
                f"✅ Estatísticas: {total_veiculos_esperado} veículos confirmados")
        else:
            print(f"❌ Estatísticas: Valor incorreto")
            sucesso = False
    except:
        print("❌ Estatísticas: Erro ao verificar")
        sucesso = False

    return sucesso


def main():
    print("🚀 INICIANDO CORREÇÃO AUTOMÁTICA COMPLETA")
    print("=" * 60)

    # 1. Fazer backup
    backup_dir = fazer_backup()

    # 2. Calcular valores corretos
    dados = calcular_veiculos_corretos()
    if not dados:
        print("❌ Falha ao calcular dados")
        return False

    total_veiculos = dados["total_veiculos_diretorias_escolas"]

    # 3. Corrigir dashboard
    if not corrigir_dashboard_js(total_veiculos):
        print("❌ Falha ao corrigir dashboard")
        return False

    # 4. Criar estatísticas
    if not criar_estatisticas_atualizadas(dados):
        print("❌ Falha ao criar estatísticas")
        return False

    # 5. Validar correções
    if not validar_correcoes(total_veiculos):
        print("❌ Validação falhou")
        return False

    # 6. Sucesso!
    print("\n" + "=" * 60)
    print("🎉 CORREÇÃO AUTOMÁTICA CONCLUÍDA COM SUCESSO!")
    print(f"📊 Sistema corrigido: {total_veiculos} veículos")
    print(
        f"🏫 {dados['total_escolas']} escolas em {dados['total_diretorias']} diretorias")
    print(f"🛡️ Backup salvo em: {backup_dir}")

    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print(f"1. python -m http.server 8000")
    print(f"2. Abrir: http://localhost:8000/dashboard_integrado.html")
    print(f"3. Verificar se mostra {total_veiculos} veículos nas estatísticas")

    return True


if __name__ == "__main__":
    sucesso = main()
    if sucesso:
        print("\n✅ SISTEMA TOTALMENTE CORRIGIDO E PRONTO PARA USO!")
    else:
        print("\n❌ CORREÇÃO FALHOU - verificar erros acima")
