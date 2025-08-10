# 🌐 COMO EXECUTAR O DASHBOARD COMO SERVIDOR

## 🚀 **OPÇÕES DISPONÍVEIS:**

### 1️⃣ **PYTHON HTTP SIMPLES (RECOMENDADO)**
```bash
python -m http.server 8000
```
- **URL:** http://localhost:8000/dashboard_integrado.html
- **Vantagem:** Já vem com Python, sem instalação extra
- **Uso:** Para desenvolvimento e testes

### 2️⃣ **SCRIPT BATCH AUTOMÁTICO**
```cmd
iniciar_servidor.bat
```
- **URL:** http://localhost:8000/dashboard_integrado.html  
- **Vantagem:** Duplo clique e já abre navegador
- **Uso:** Para usuários finais

### 3️⃣ **SCRIPT PYTHON AVANÇADO**
```bash
python scripts/servidor.py
python scripts/servidor.py 3000        # Porta personalizada
python scripts/servidor.py --cors      # Com suporte CORS
```
- **URL:** http://localhost:8000/dashboard_integrado.html
- **Vantagem:** Mais opções e controle
- **Uso:** Para desenvolvimento avançado

### 4️⃣ **LIVE SERVER (VS CODE)**
1. Instalar extensão "Live Server" no VS Code
2. Abrir `dashboard_integrado.html`
3. Botão direito → "Open with Live Server"
- **URL:** http://127.0.0.1:5500/dashboard_integrado.html
- **Vantagem:** Recarrega automaticamente
- **Uso:** Para desenvolvimento no VS Code

### 5️⃣ **NODE.JS HTTP-SERVER**
```bash
npm install -g http-server
http-server -p 8000 -c-1
```
- **URL:** http://localhost:8000/dashboard_integrado.html
- **Vantagem:** Muito rápido e eficiente
- **Uso:** Se você já usa Node.js

## 🎯 **RECOMENDAÇÕES:**

### Para **Desenvolvimento:**
- **VS Code:** Live Server (opção 4)
- **Terminal:** Python HTTP (opção 1)

### Para **Demonstração:**
- **Windows:** Script BAT (opção 2)
- **Qualquer SO:** Python HTTP (opção 1)

### Para **Produção:**
- **Servidor web real** (Apache, Nginx)
- **Hosting estático** (GitHub Pages, Netlify)

## 🔧 **SOLUCIONANDO PROBLEMAS:**

### ❌ "Porta 8000 já está em uso"
```bash
python -m http.server 8001  # Usar porta diferente
```

### ❌ "Erro de CORS"
```bash
python scripts/servidor.py --cors  # Habilitar CORS
```

### ❌ "Arquivo não encontrado"
```bash
cd caminho/para/escolas_indigina_quilo_assent
python -m http.server 8000
```

## 📱 **ACESSANDO O DASHBOARD:**

Após iniciar qualquer servidor, acesse:
- **Local:** http://localhost:8000/dashboard_integrado.html
- **Rede:** http://SEU_IP:8000/dashboard_integrado.html

O dashboard irá carregar com:
- ✅ 63 escolas (37 indígenas + 26 quilombolas)  
- ✅ 39 veículos nas 19 diretorias
- ✅ Mapa interativo com São Paulo
- ✅ Gráficos e estatísticas

---

**🎉 Pronto! Seu dashboard está rodando como servidor web!**
