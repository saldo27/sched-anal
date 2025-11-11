@echo off
REM Script de instalación para Windows
REM Este script descarga e instala todas las dependencias necesarias

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo   Instalador de Análisis de Guardias
echo ===============================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    echo Asegúrate de marcar "Add Python to PATH" durante la instalación
    echo.
    pause
    exit /b 1
)

echo [1/4] Versión de Python:
python --version
echo.

REM Crear virtual environment
echo [2/4] Creando entorno virtual...
if exist venv (
    echo     - Entorno virtual ya existe
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo     - Entorno virtual creado ✓
)
echo.

REM Activar virtual environment
echo [3/4] Instalando dependencias Python...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)

python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudo instalar las dependencias
    pause
    exit /b 1
)
echo     - Dependencias instaladas ✓
echo.

REM Instalar dependencias de Node.js (frontend)
echo [4/4] Instalando dependencias del frontend (Node.js)...
if not exist node_modules (
    npm install
    if errorlevel 1 (
        echo [ADVERTENCIA] No se pudo instalar dependencias de Node.js
        echo              Asegúrate de tener Node.js instalado desde: https://nodejs.org/
    ) else (
        echo     - Dependencias del frontend instaladas ✓
    )
) else (
    echo     - Dependencias del frontend ya instaladas
)
echo.

echo ===============================================
echo   ✓ Instalación completada con éxito
echo ===============================================
echo.
echo Para iniciar la aplicación, ejecuta:
echo   run.bat
echo.
pause
