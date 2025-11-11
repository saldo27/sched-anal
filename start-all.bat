@echo off
REM start-all.bat - Inicia backend y frontend en dos ventanas separadas

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                    SCHED-ANAL - INICIAR TODO                              ║
echo ║                                                                            ║
echo ║  Este script abrirá dos ventanas:                                          ║
echo ║    1. Backend (Flask) - Puerto 5000                                        ║
echo ║    2. Frontend (React) - Puerto 3000                                       ║
echo ║                                                                            ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

REM Obtener el directorio actual
set SCRIPT_DIR=%~dp0

REM Verificar que estamos en el directorio correcto
if not exist "%SCRIPT_DIR%app.py" (
    echo ❌ ERROR: app.py no encontrado
    echo.
    echo Por favor ejecuta este script desde el directorio raíz del proyecto
    echo.
    pause
    exit /b 1
)

if not exist "%SCRIPT_DIR%package.json" (
    echo ❌ ERROR: package.json no encontrado
    echo.
    echo Por favor ejecuta este script desde el directorio raíz del proyecto
    echo.
    pause
    exit /b 1
)

echo 🚀 Abriendo Backend (Flask)...
start "SCHED-ANAL Backend" cmd /k "cd /d %SCRIPT_DIR% && call python app.py"

timeout /t 3 /nobreak

echo 🚀 Abriendo Frontend (React)...
start "SCHED-ANAL Frontend" cmd /k "cd /d %SCRIPT_DIR% && call npm run dev"

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                            ║
echo ║  ✅ Ambos servidores están iniciándose                                    ║
echo ║                                                                            ║
echo ║  📊 Estado:                                                                ║
echo ║     • Backend:  http://127.0.0.1:5000    (En ventana 1)                  ║
echo ║     • Frontend: http://localhost:3000    (En ventana 2)                   ║
echo ║                                                                            ║
echo ║  ⏳ Espera 15 segundos para que ambos se inicien completamente            ║
echo ║                                                                            ║
echo ║  🌐 Luego abre en navegador:                                              ║
echo ║     http://localhost:3000                                                 ║
echo ║                                                                            ║
echo ║  🔥 Troubleshooting:                                                      ║
echo ║     • Si algo falla, revisa la ventana correspondiente                    ║
echo ║     • Si Puerto en uso: cierra la otra instancia                          ║
echo ║     • Si módulos faltan: ejecuta npm install y pip install -r req...     ║
echo ║                                                                            ║
echo ║  💡 Cierra ambas ventanas con Ctrl+C cuando termines                      ║
echo ║                                                                            ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

pause
