@echo off
REM check-requirements.bat - Verifica que todas las dependencias estén instaladas

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                    VERIFICADOR DE REQUISITOS                              ║
echo ║                   Sched-Anal - Dependency Checker                         ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion

REM Colores de salida (si PowerShell lo permite)
set "OK=[OK]"
set "ERROR=[ERROR]"
set "WARNING=[WARNING]"

REM Variables para tracking
set "all_ok=1"

echo 🔍 Verificando requisitos...
echo.

REM ============================================================================
REM VERIFICAR PYTHON
REM ============================================================================

echo ───────────────────────────────────────────────────────────────────────────
echo 1. PYTHON
echo ───────────────────────────────────────────────────────────────────────────

python --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Python NO encontrado
    echo.
    echo   ❌ Python no está instalado o no está en PATH
    echo.
    echo   Solución:
    echo     1. Descarga Python desde python.org
    echo     2. Instálalo y marca "Add Python to PATH"
    echo     3. Reinicia la terminal
    echo.
    set "all_ok=0"
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set "python_version=%%i"
    echo %OK% !python_version! instalado
)
echo.

REM ============================================================================
REM VERIFICAR NODE.JS
REM ============================================================================

echo ───────────────────────────────────────────────────────────────────────────
echo 2. NODE.JS
echo ───────────────────────────────────────────────────────────────────────────

node --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Node.js NO encontrado
    echo.
    echo   ❌ Node.js no está instalado o no está en PATH
    echo.
    echo   Solución:
    echo     1. Descarga Node.js LTS desde nodejs.org
    echo     2. Instálalo y marca "Add to PATH"
    echo     3. Reinicia la terminal
    echo.
    set "all_ok=0"
) else (
    for /f "tokens=*" %%i in ('node --version 2^>^&1') do set "node_version=%%i"
    echo %OK% Node.js !node_version! instalado
)
echo.

REM ============================================================================
REM VERIFICAR NPM
REM ============================================================================

echo ───────────────────────────────────────────────────────────────────────────
echo 3. NPM (Node Package Manager)
echo ───────────────────────────────────────────────────────────────────────────

npm --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% npm NO encontrado
    echo.
    echo   ❌ npm no está disponible
    echo.
    echo   Nota: npm se incluye con Node.js
    echo.
    echo   Solución:
    echo     1. Reinstala Node.js desde nodejs.org
    echo     2. Asegúrate de marcar "npm package manager"
    echo     3. Reinicia completamente (cierra todas las ventanas)
    echo.
    set "all_ok=0"
) else (
    for /f "tokens=*" %%i in ('npm --version 2^>^&1') do set "npm_version=%%i"
    echo %OK% npm !npm_version! instalado
)
echo.

REM ============================================================================
REM VERIFICAR GIT (OPCIONAL)
REM ============================================================================

echo ───────────────────────────────────────────────────────────────────────────
echo 4. GIT (Opcional)
echo ───────────────────────────────────────────────────────────────────────────

git --version >nul 2>&1
if errorlevel 1 (
    echo %WARNING% Git NO encontrado (opcional)
    echo.
    echo   ⚠️  Git no está instalado
    echo.
    echo   Nota: Esto es OPCIONAL. Solo se necesita si quieres usar Git.
    echo.
) else (
    for /f "tokens=*" %%i in ('git --version 2^>^&1') do set "git_version=%%i"
    echo %OK% Git encontrado (!git_version!)
)
echo.

REM ============================================================================
REM VERIFICAR CARPETAS
REM ============================================================================

echo ───────────────────────────────────────────────────────────────────────────
echo 5. ARCHIVOS NECESARIOS
echo ───────────────────────────────────────────────────────────────────────────

if not exist "app.py" (
    echo %ERROR% app.py NO encontrado
    set "all_ok=0"
) else (
    echo %OK% app.py encontrado
)

if not exist "package.json" (
    echo %ERROR% package.json NO encontrado
    set "all_ok=0"
) else (
    echo %OK% package.json encontrado
)

if not exist "requirements.txt" (
    echo %WARNING% requirements.txt NO encontrado (opcional)
) else (
    echo %OK% requirements.txt encontrado
)

echo.

REM ============================================================================
REM RESUMEN FINAL
REM ============================================================================

echo ═══════════════════════════════════════════════════════════════════════════
if !all_ok! equ 1 (
    echo ✅ TODOS LOS REQUISITOS ESTÁN INSTALADOS
    echo.
    echo 🚀 Próximos pasos:
    echo.
    echo    1. Instala dependencias Python:
    echo       pip install -r requirements.txt
    echo.
    echo    2. Instala dependencias Node.js:
    echo       npm install
    echo.
    echo    3. Ejecuta backend:
    echo       python app.py
    echo.
    echo    4. En otra terminal, ejecuta frontend:
    echo       npm run dev
    echo.
    echo    5. Abre navegador:
    echo       http://localhost:3000
    echo.
) else (
    echo ❌ FALTAN ALGUNOS REQUISITOS
    echo.
    echo 🔧 Por favor instala los faltantes:
    echo.
    echo    • Python:  https://python.org
    echo    • Node.js: https://nodejs.org (elige LTS)
    echo    • Git:     https://git-scm.com (opcional)
    echo.
    echo 💡 Importante:
    echo    - Marca "Add to PATH" durante la instalación
    echo    - Reinicia la terminal después de instalar
    echo    - Una terminal NEW (no reutilizar la actual)
    echo.
)
echo ═══════════════════════════════════════════════════════════════════════════
echo.

pause
