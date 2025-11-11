# 🪟 Guía Rápida para Windows - Sched-Anal

**Tabla de contenidos**:
1. [Requisitos](#requisitos)
2. [Instalación rápida](#instalación-rápida) 
3. [Ejecutar la aplicación](#ejecutar-la-aplicación)
4. [Solucionar problemas](#solucionar-problemas)

---

## ✅ Requisitos

- **Python 3.8+**: Descargar de [python.org](https://www.python.org/downloads/)
- **Node.js 16+**: Descargar de [nodejs.org](https://nodejs.org/)
- **Git** (opcional): Descargar de [git-scm.com](https://git-scm.com/)

### Verificar que está instalado:

Abre **PowerShell** o **CMD** y ejecuta:

```bash
python --version
node --version
npm --version
```

---

## 📥 Instalación Rápida

### 1. Clonar o descargar el proyecto

**Opción A - Con Git:**
```bash
git clone https://github.com/saldo27/sched-anal.git
cd sched-anal
```

**Opción B - Manual:**
1. Descarga el proyecto como ZIP desde GitHub
2. Extrae en una carpeta
3. Abre esa carpeta

### 2. Instalar dependencias Python

En **PowerShell** o **CMD**, en la carpeta del proyecto:

```bash
pip install -r requirements.txt
```

Si falla, intenta:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Instalar dependencias Node.js

```bash
npm install
```

---

## 🚀 Ejecutar la Aplicación

### Opción 1: Script Todo en Uno (RECOMENDADO)

Simplemente haz **doble clic** en:

```
start-all.bat
```

✅ Esto abre automáticamente:
- Terminal 1: Backend (Flask) en puerto 5000
- Terminal 2: Frontend (React) en puerto 3000

Espera 15-20 segundos, luego abre en navegador:

```
http://localhost:3000
```

---

### Opción 2: Ejecución Manual (Dos Terminales)

**Terminal 1 - Backend:**

Haz doble clic en:
```
run-server.bat
```

O ejecuta manualmente:
```bash
python app.py
```

**Esperado:**
```
Running on http://127.0.0.1:5000
```

---

**Terminal 2 - Frontend** (Abre una NUEVA terminal):

Haz doble clic en:
```
run-frontend.bat
```

O ejecuta manualmente:
```bash
npm run dev
```

**Esperado:**
```
Local: http://localhost:3000
```

---

### Opción 3: PowerShell (Mejor para debugging)

**Terminal 1:**
```powershell
.\run-server.ps1
```

**Terminal 2:**
```bash
npm run dev
```

---

## ✅ Verificar que Funciona

### Método 1: Abre en navegador

```
http://localhost:3000
```

Deberías ver la interfaz de Calendar Analyzer

---

### Método 2: Prueba el backend en PowerShell

En una nueva terminal PowerShell:

```powershell
(Invoke-WebRequest http://127.0.0.1:5000/health).Content
```

**Resultado esperado:**
```json
{"status":"ok","version":"1.0.0"}
```

---

## 🧪 Probar Funcionalidades

### 1. Subir un PDF

- Haz clic en "📄 Cargar PDF"
- Selecciona un PDF con un calendario/horarios
- El backend lo procesa y muestra el texto extraído

### 2. Subir un Excel

- Haz clic en "📊 Cargar Excel"
- Selecciona un `.xlsx` o `.xls` con datos
- Se muestra en la tabla

### 3. Subir un CSV

- Haz clic en "📋 Cargar CSV"
- Selecciona un archivo `.csv`

### 4. Entrada Manual de Texto

- Pega horarios en el área de texto
- Haz clic en "Analizar"
- El sistema detecta automáticamente la estructura

---

## 🐛 Solucionar Problemas

### ❌ "python: command not found" o "python no reconocido"

**Solución:**
1. Instala Python desde [python.org](https://www.python.org/downloads/)
2. **IMPORTANTE**: Marca ✅ "Add Python to PATH"
3. Reinicia terminal
4. Verifica: `python --version`

---

### ❌ "npm: command not found"

**Solución:**
1. Instala Node.js desde [nodejs.org](https://nodejs.org/)
2. El instalador incluye npm
3. Reinicia terminal
4. Verifica: `npm --version`

---

### ❌ "Port 5000 already in use"

**Solución:**
1. Cierra otra instancia de `python app.py`
2. O cambia el puerto en `app.py` (última línea)
3. O ejecuta:
   ```bash
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

---

### ❌ "Cannot GET /api/upload"

**Solución:**
- Verifica que el backend está corriendo
- Backend debe estar en puerto 5000
- Frontend proxy debe estar configurado en `vite.config.js`
- Recarga navegador: `Ctrl+F5`

---

### ❌ "ModuleNotFoundError" (flask, pandas, etc.)

**Solución:**
```bash
pip install -r requirements.txt
```

Si persiste:
```bash
python -m pip install --upgrade pip
python -m pip install flask flask-cors pandas pdfplumber openpyxl
```

---

### ❌ "npm ERR!"

**Solución:**
```bash
# Limpia cache
npm cache clean --force

# Reinstala
rm -r node_modules package-lock.json
npm install
```

---

### ❌ Firewall bloquea conexión

**Solución:**
1. Abre "Windows Defender Firewall" 
2. → "Permitir una aplicación a través del firewall"
3. Busca Python
4. Marca ✅ "Privada" y "Pública"
5. Reinicia terminal

---

## 📁 Estructura del Proyecto

```
sched-anal/
├── app.py                    ← Backend Flask
├── file_processor.py         ← Procesador de archivos
├── CalendarAnalyzer.jsx      ← Frontend React
├── package.json              ← Dependencias Node
├── requirements.txt          ← Dependencias Python
├── run-server.bat            ← Ejecutar backend
├── run-server.ps1            ← Ejecutar backend (PowerShell)
├── run-frontend.bat          ← Ejecutar frontend
├── start-all.bat             ← Ejecutar todo
└── README.md                 ← Documentación
```

---

## 📊 Configuración

### Backend (app.py)

- **Host**: 127.0.0.1 (localhost - compatible con Windows)
- **Puerto**: 5000
- **Debug**: ON
- **Reloader**: OFF (evita problemas de watchdog)

### Frontend (vite.config.js)

- **Puerto**: 3000
- **Auto-reload**: ON
- **Proxy**: /api → http://localhost:5000

---

## 💡 Tips para Windows

1. **Usa PowerShell en lugar de CMD** - Mejor soporte UTF-8
2. **Ejecuta scripts con doble clic** - Más fácil que terminal
3. **Mantén abiertos dos `cmd` o PowerShell** - Uno para cada servidor
4. **No cierres las terminales** - Los servidores se detienen
5. **Ctrl+C para detener** - Ambos servidores

---

## 🔄 Actualizar desde GitHub

```bash
git pull origin copilot/add-shift-analysis-table
pip install -r requirements.txt
npm install
```

---

## 📞 Soporte

**Si algo no funciona:**

1. Lee **WINDOWS_FIX.md** - Soluciones específicas
2. Mira los logs en la terminal de backend
3. Abre DevTools del navegador (F12) para errores frontend
4. Verifica que ambos servidores están corriendo

---

## 🎯 Próximos Pasos

1. ✅ Ejecuta `start-all.bat`
2. ✅ Espera 15-20 segundos
3. ✅ Abre http://localhost:3000
4. ✅ Prueba cargar un PDF/Excel/CSV
5. ✅ Verifica que funciona todo

---

**¡A disfrutar! 🚀**

---

**Última actualización**: Nov 11, 2025  
**Para**: Windows 10/11  
**Status**: ✅ Probado y funcional
