# Script de organização do projeto
$basePath = "c:\Users\bruno\Desktop\escolas_indigina_quilo_assent"
Set-Location $basePath

# Criar estrutura de archive se não existir
if (!(Test-Path "archive")) { New-Item -ItemType Directory -Name "archive" }
if (!(Test-Path "archive\docs_antigos")) { New-Item -ItemType Directory -Path "archive\docs_antigos" }
if (!(Test-Path "archive\scripts_auxiliares")) { New-Item -ItemType Directory -Path "archive\scripts_auxiliares" }

# Mover arquivos de documentação desnecessários
$docsParaMover = @(
    "CORRECOES_*.md",
    "ERRO_*.md", 
    "MAPA_*.md",
    "MARCADORES_*.md",
    "MODULARIZACAO_*.md",
    "ORGANIZACAO_*.md",
    "RELATORIO_*.md",
    "SOLUCAO_*.md",
    "STATUS_*.md",
    "README_backup.md",
    "SUMMARY.md"
)

foreach ($pattern in $docsParaMover) {
    Get-ChildItem -Path . -Name $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        Move-Item -Path $_ -Destination "archive\docs_antigos\" -Force -ErrorAction SilentlyContinue
    }
}

# Mover scripts Python auxiliares
$scriptsParaMover = @(
    "analisar_bases_atualizadas.py",
    "categorizar_arquivos_raiz.py",
    "main.py"
)

foreach ($script in $scriptsParaMover) {
    if (Test-Path $script) {
        Move-Item -Path $script -Destination "archive\scripts_auxiliares\" -Force -ErrorAction SilentlyContinue
    }
}

# Mover outros arquivos
$outrosArquivos = @(
    "dash_dinamico_backup.js",
    "config_sistema.json"
)

foreach ($arquivo in $outrosArquivos) {
    if (Test-Path $arquivo) {
        Move-Item -Path $arquivo -Destination "archive\" -Force -ErrorAction SilentlyContinue
    }
}

# Mover JSONs duplicados para pasta dados
$jsonsParaMover = @(
    "dados_escolas_atualizados.json",
    "dados_supervisao_atualizados.json", 
    "dados_veiculos_diretorias.json",
    "estatisticas_atualizadas.json"
)

foreach ($json in $jsonsParaMover) {
    if (Test-Path $json) {
        Move-Item -Path $json -Destination "dados\" -Force -ErrorAction SilentlyContinue
    }
}

# Mover pastas grandes
$pastasParaMover = @(
    "old_backups",
    "documentacao", 
    "relatorios",
    "RESULTADOS"
)

foreach ($pasta in $pastasParaMover) {
    if (Test-Path $pasta) {
        Move-Item -Path $pasta -Destination "archive\" -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Organização concluída!"
