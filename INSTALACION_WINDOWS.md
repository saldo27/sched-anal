# 🚀 Instalación Rápida - Windows

## Paso 1: Descargar o Clonar

```bash
git clone https://github.com/saldo27/sched-anal.git
cd sched-anal
```

O descarga el ZIP desde: https://github.com/saldo27/sched-anal

## Paso 2: Ejecutar el Instalador

**Haz doble clic en `install.bat`** o desde terminal:

```cmd
install.bat
```

Esto instala automáticamente:
- ✅ Python 3.8+
- ✅ Entorno virtual
- ✅ Dependencias Python (Flask, ReportLab, etc.)
- ✅ Node.js y npm (si no están instalados)
- ✅ Dependencias del frontend (React, Vite)

## Paso 3: Ejecutar la Aplicación

**Haz doble clic en `run.bat`** o desde terminal:

```cmd
run.bat
```

Se abrirá automáticamente: **http://localhost:3000**

---

## ¿Qué hace la app?

1. **Cargar archivo**: PDF, Excel o ingresa el calendario manualmente
2. **Análisis automático**: Genera estadísticas de guardias
3. **Exportar resultados**: CSV o PDF (A4 vertical)

---

## Requisitos Previos

- **Windows 7+**
- **Python 3.8+** (desde https://www.python.org/downloads/)
- **Node.js 16+** (desde https://nodejs.org/)

⚠️ **IMPORTANTE**: Durante la instalación de Python, marca "Add Python to PATH"

---

## Solución de Problemas

### "Python no está en el PATH"
1. Desinstala Python
2. Reinstala y marca **"Add Python to PATH"**
3. Reinicia Windows

### Puerto ocupado
```cmd
netstat -ano | findstr :5000
taskkill /PID <número> /F
```

### El instalador falla
- Abre terminal como **Administrador**
- Ejecuta: `install.bat`

---

## Para desarrolladores

```bash
# Entorno virtual
venv\Scripts\activate.bat

# Backend (Python)
python app.py                 # http://localhost:5000

# Frontend (React - terminal nueva)
npm run dev                   # http://localhost:3000
```

---

## Estructura

```
sched-anal/
├── app.py              # Backend Flask
├── file_processor.py   # Procesador de archivos
├── CalendarAnalyzer.jsx # Frontend React
├── install.bat         # Instalador
├── run.bat             # Ejecutor
├── requirements.txt    # Dependencias Python
└── package.json        # Dependencias Node.js
```

¡Listo! 🎉
