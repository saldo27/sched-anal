@echo off
REM run-server.bat - Script para ejecutar el servidor en Windows

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                       SCHED-ANAL - SERVIDOR BACKEND                       ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en PATH
    echo.
    echo Por favor:
    echo 1. Instala Python desde python.org
    echo 2. Asegúrate de marcar "Add Python to PATH" durante la instalación
    echo 3. Reinicia esta ventana de terminal
    echo.
    pause
    exit /b 1
)

REM Verificar que estamos en el directorio correcto
if not exist "app.py" (
    echo ❌ ERROR: app.py no encontrado
    echo.
    echo Por favor ejecuta este script desde el directorio raíz del proyecto
    echo (donde está app.py, file_processor.py, requirements.txt)
    echo.
    pause
    exit /b 1
)

REM Mostrar información del sistema
echo 📊 Información del Sistema:
python --version
echo.

REM Verificar dependencias
echo 🔍 Verificando dependencias...
python -c "import flask; import flask_cors; import pandas; import pdfplumber" 2>nul
if errorlevel 1 (
    echo.
    echo ⚠️  ADVERTENCIA: Algunas dependencias no están instaladas
    echo.
    echo Instala con:
    echo    pip install -r requirements.txt
    echo.
    echo Esperando 5 segundos...
    timeout /t 5
)

echo.
echo 📋 Configuración del Servidor:
echo    • Host: 127.0.0.1 (localhost)
echo    • Puerto: 5000
echo    • Debug: ON
echo    • Reloader: OFF (Windows compatible)
echo    • CORS: Enabled
echo.
echo 🌐 Accesible desde:
echo    • Local:     http://localhost:5000
echo    • Localhost: http://127.0.0.1:5000
echo.
echo 📝 Endpoints disponibles:
echo    • GET  /health           - Server health check
echo    • POST /api/upload       - Upload file (PDF, Excel, CSV)
echo    • POST /api/analyze      - Analyze calendar data
echo    • POST /api/export       - Export results (CSV/JSON)
echo.
echo 🔧 Troubleshooting:
echo    • Si dice "Port already in use": Cambia puerto en app.py
echo    • Si no conecta: Verifica Firewall de Windows
echo    • Si error de módulos: Ejecuta: pip install -r requirements.txt
echo.
echo ✅ Para probar en otra terminal:
echo    PowerShell:  (Invoke-WebRequest http://127.0.0.1:5000/health).Content
echo    CMD:         curl http://127.0.0.1:5000/health
echo    Navegador:   http://localhost:5000/health
echo.
echo 🚀 Iniciando servidor...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Ejecutar Flask
python app.py

REM Si Flask se cierra, mostrar mensaje
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🛑 Servidor detenido
echo.
pause
