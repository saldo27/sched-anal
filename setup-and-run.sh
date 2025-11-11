#!/bin/bash
# setup-and-run.sh - Script para instalar y ejecutar la aplicación
# Uso: bash setup-and-run.sh [frontend|backend|both]

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Analizador de Calendarios de Turnos - Setup Script      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

# Detectar sistema operativo
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS="Linux";;
    Darwin*)    OS="Mac";;
    CYGWIN*)    OS="Cygwin";;
    MINGW*)     OS="MinGw";;
    *)          OS="UNKNOWN";;
esac

info "Sistema detectado: $OS"
echo ""

# Función para instalar Python dependencies
install_python_deps() {
    info "Instalando dependencias Python..."
    
    if ! command -v python3 &> /dev/null; then
        error "Python3 no está instalado"
        exit 1
    fi
    
    success "Python3 encontrado"
    
    pip install -q -r requirements.txt
    success "Dependencias Python instaladas"
}

# Función para instalar Node dependencies
install_node_deps() {
    info "Instalando dependencias Node.js..."
    
    if ! command -v npm &> /dev/null; then
        error "Node.js/npm no está instalado"
        exit 1
    fi
    
    success "npm encontrado"
    
    npm install > /dev/null 2>&1
    success "Dependencias Node.js instaladas"
}

# Función para verificar puertos
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        warning "Puerto $port ya está en uso"
        return 1
    else
        return 0
    fi
}

# Función para ejecutar backend
run_backend() {
    info "Iniciando Backend (Flask)..."
    echo ""
    if check_port 5000; then
        info "Backend se ejecutará en http://0.0.0.0:5000"
        python app.py
    else
        error "Puerto 5000 ya está en uso"
        echo "  Intenta en otro puerto:"
        echo "  - Edita app.py"
        echo "  - Cambia: app.run(..., port=5001)"
        exit 1
    fi
}

# Función para ejecutar frontend
run_frontend() {
    info "Iniciando Frontend (Vite)..."
    echo ""
    if check_port 3000; then
        info "Frontend se ejecutará en http://localhost:3000"
        npm run dev
    else
        error "Puerto 3000 ya está en uso"
        echo "  Intenta: npm run dev -- --port 3001"
        exit 1
    fi
}

# Función para ejecutar ambos
run_both() {
    install_python_deps
    install_node_deps
    
    echo ""
    success "Todas las dependencias están instaladas"
    echo ""
    info "Para ejecutar:"
    echo "  Terminal 1: python app.py (Backend)"
    echo "  Terminal 2: npm run dev (Frontend)"
    echo ""
    info "Luego abre: http://localhost:3000"
}

# Main
MODE=${1:-"help"}

case $MODE in
    backend)
        install_python_deps
        run_backend
        ;;
    frontend)
        install_node_deps
        run_frontend
        ;;
    both)
        run_both
        ;;
    *)
        echo "Uso: bash setup-and-run.sh [backend|frontend|both]"
        echo ""
        echo "Ejemplos:"
        echo "  bash setup-and-run.sh backend    # Ejecutar solo backend"
        echo "  bash setup-and-run.sh frontend   # Ejecutar solo frontend"
        echo "  bash setup-and-run.sh both       # Instalar dependencias"
        echo ""
        echo "Si ejecutas 'both', se instalarán las dependencias"
        echo "Luego ejecuta en dos terminales diferentes:"
        echo "  Terminal 1: python app.py"
        echo "  Terminal 2: npm run dev"
        ;;
esac
