@echo off
REM Script para iniciar o servidor do dashboard
REM Executa automaticamente o servidor HTTP do Python

echo.
echo 🚀 INICIANDO SERVIDOR DO DASHBOARD
echo ===================================
echo.

cd /d "%~dp0"

echo 📁 Diretório: %CD%
echo 🌐 Iniciando servidor na porta 8000...
echo 📍 URL: http://localhost:8000/dashboard_integrado.html
echo.
echo 🛑 Para parar o servidor: Ctrl+C
echo ⏳ Aguarde alguns segundos para o servidor iniciar...
echo.

timeout /t 2 >nul
start http://localhost:8000/dashboard_integrado.html

python -m http.server 8000

pause
