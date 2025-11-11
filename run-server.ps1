# run-server.ps1 - Script para ejecutar el servidor en Windows (PowerShell)
# Uso: .\run-server.ps1

# Estilos de color
$Success = "Green"
$Warning = "Yellow"
$Error = "Red"
$Info = "Cyan"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor $Info
Write-Host "║                       SCHED-ANAL - SERVIDOR BACKEND                       ║" -ForegroundColor $Info
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor $Info
Write-Host ""

# Verificar que Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor $Success
} catch {
    Write-Host "❌ ERROR: Python no está instalado o no está en PATH" -ForegroundColor $Error
    Write-Host ""
    Write-Host "Por favor:" -ForegroundColor $Warning
    Write-Host "1. Instala Python desde python.org" -ForegroundColor $Warning
    Write-Host "2. Asegúrate de marcar 'Add Python to PATH' durante la instalación" -ForegroundColor $Warning
    Write-Host "3. Reinicia PowerShell" -ForegroundColor $Warning
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar que app.py existe
if (-not (Test-Path "app.py")) {
    Write-Host "❌ ERROR: app.py no encontrado" -ForegroundColor $Error
    Write-Host ""
    Write-Host "Por favor ejecuta este script desde el directorio raíz del proyecto" -ForegroundColor $Warning
    Write-Host "(donde está app.py, file_processor.py, requirements.txt)" -ForegroundColor $Warning
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "🔍 Verificando dependencias..." -ForegroundColor $Info
$missingDeps = @()

# Verificar cada dependencia
$dependencies = @("flask", "flask_cors", "pandas", "pdfplumber", "openpyxl")
foreach ($dep in $dependencies) {
    try {
        python -c "import $dep" 2>$null
        Write-Host "  ✅ $dep" -ForegroundColor $Success
    } catch {
        Write-Host "  ❌ $dep (falta)" -ForegroundColor $Error
        $missingDeps += $dep
    }
}

if ($missingDeps.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  Faltan dependencias: $($missingDeps -join ', ')" -ForegroundColor $Warning
    Write-Host ""
    Write-Host "Instala con:" -ForegroundColor $Info
    Write-Host "  pip install -r requirements.txt" -ForegroundColor $Info
    Write-Host ""
    $install = Read-Host "¿Deseas instalarlas ahora? (s/n)"
    if ($install -eq "s" -or $install -eq "S") {
        python -m pip install -r requirements.txt
    }
    Write-Host ""
}

Write-Host "📋 Configuración del Servidor:" -ForegroundColor $Info
Write-Host "   • Host: 127.0.0.1 (localhost)" -ForegroundColor $Info
Write-Host "   • Puerto: 5000" -ForegroundColor $Info
Write-Host "   • Debug: ON" -ForegroundColor $Info
Write-Host "   • Reloader: OFF (Windows compatible)" -ForegroundColor $Info
Write-Host "   • CORS: Enabled" -ForegroundColor $Info
Write-Host ""

Write-Host "🌐 Accesible desde:" -ForegroundColor $Info
Write-Host "   • Local:     http://localhost:5000" -ForegroundColor $Info
Write-Host "   • Localhost: http://127.0.0.1:5000" -ForegroundColor $Info
Write-Host ""

Write-Host "📝 Endpoints disponibles:" -ForegroundColor $Info
Write-Host "   • GET  /health           - Server health check" -ForegroundColor $Info
Write-Host "   • POST /api/upload       - Upload file (PDF, Excel, CSV)" -ForegroundColor $Info
Write-Host "   • POST /api/analyze      - Analyze calendar data" -ForegroundColor $Info
Write-Host "   • POST /api/export       - Export results (CSV/JSON)" -ForegroundColor $Info
Write-Host ""

Write-Host "✅ Para probar en otra ventana PowerShell:" -ForegroundColor $Success
Write-Host '   (Invoke-WebRequest http://127.0.0.1:5000/health).Content' -ForegroundColor $Success
Write-Host ""
Write-Host "🔥 O abre en navegador:" -ForegroundColor $Info
Write-Host "   http://localhost:5000/health" -ForegroundColor $Info
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor $Info
Write-Host "🚀 Iniciando servidor..." -ForegroundColor $Success
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor $Info
Write-Host ""

# Ejecutar Flask
python app.py

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor $Info
Write-Host "🛑 Servidor detenido" -ForegroundColor $Warning
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor $Info
Write-Host ""
Read-Host "Presiona Enter para salir"
