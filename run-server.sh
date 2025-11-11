#!/bin/bash
# run-server.sh - Script para ejecutar el servidor sin problemas de watchdog

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  SERVIDOR SCHED-ANAL                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar sistema operativo
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "🖥️  Sistema detectado: Windows"
    FLASK_ENV=development
else
    echo "🖥️  Sistema detectado: Unix-like"
    export FLASK_ENV=development
fi

echo "📊 Configuración:"
echo "  - Debug mode: ON"
echo "  - Reloader: OFF (evita problemas de watchdog)"
echo "  - Host: 0.0.0.0"
echo "  - Puerto: 5000"
echo ""
echo "🚀 Iniciando servidor..."
echo ""

# Ejecutar Flask sin reloader
python app.py

# Alternativa con gunicorn (descomenta si quieres usar gunicorn):
# echo "Usando gunicorn..."
# gunicorn -w 1 -b 0.0.0.0:5000 --reload app:app
