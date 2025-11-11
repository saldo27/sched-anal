@echo off
REM Script para ejecutar la aplicación de Análisis de Turnos

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo   Análisis de Turnos - Aplicación
echo ===============================================
echo.

REM Verificar si el entorno virtual existe
if not exist venv (
    echo [ERROR] Entorno virtual no encontrado
    echo Por favor ejecuta primero: install.bat
    echo.
    pause
    exit /b 1
)

REM Activar virtual environment
call venv\Scripts\activate.bat

REM Iniciar backend (Flask) en background
echo [1/2] Iniciando servidor backend (Flask)...
start "" cmd /c "python app.py"
timeout /t 3 >nul

REM Iniciar frontend (Vite)
echo [2/2] Iniciando servidor frontend (Vite)...
echo.
echo ===============================================
echo   ✓ Aplicación iniciada
echo ===============================================
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:5000
echo.
echo Abre http://localhost:3000 en tu navegador
echo.
echo Presiona Ctrl+C para detener los servidores
echo ===============================================
echo.

cd /d "%~dp0"
call npm run dev -- --host 127.0.0.1 --port 3000
