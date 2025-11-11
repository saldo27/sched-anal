@echo off
REM run-frontend.bat - Script para ejecutar el frontend en Windows

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                       SCHED-ANAL - FRONTEND (REACT)                       ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar que Node.js está instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js no está instalado o no está en PATH
    echo.
    echo Por favor:
    echo 1. Descarga Node.js desde nodejs.org
    echo 2. Instálalo (npm se incluye automáticamente)
    echo 3. Reinicia esta ventana de terminal
    echo.
    pause
    exit /b 1
)

REM Mostrar versión de Node.js
echo 📊 Versión de Node.js:
node --version
echo.

REM Verificar que package.json existe
if not exist "package.json" (
    echo ❌ ERROR: package.json no encontrado
    echo.
    echo Por favor ejecuta este script desde el directorio raíz del proyecto
    echo.
    pause
    exit /b 1
)

REM Verificar si node_modules existe
if not exist "node_modules" (
    echo ⚠️  node_modules no encontrado, instalando dependencias...
    echo.
    call npm install
    if errorlevel 1 (
        echo ❌ ERROR al instalar dependencias
        pause
        exit /b 1
    )
    echo.
)

echo 📋 Configuración del Frontend:
echo    • Framework: React 18
echo    • Build Tool: Vite
echo    • Port: 3000
echo    • Auto-reload: ON
echo.

echo 🌐 Accesible desde:
echo    • Local: http://localhost:3000
echo.

echo ⚙️  Requisito: Backend debe estar corriendo
echo    (en otra terminal: python app.py)
echo.

echo 🚀 Iniciando servidor de desarrollo...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Ejecutar npm dev
call npm run dev

REM Si npm se cierra, mostrar mensaje
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🛑 Servidor detenido
echo.
pause
