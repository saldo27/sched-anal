# 📦 ¿Qué es npm? ¿Por qué lo necesitas?

## 🤔 Explicación Simple

### ¿Qué es npm?

**npm = Node Package Manager**

Es como el "store" de aplicaciones, pero para código JavaScript.

- **pip** (Python) = Instala librerías Python
- **npm** (Node.js) = Instala librerías JavaScript

Así como usas `pip install flask` en Python, usas `npm install` en JavaScript/Node.js.

---

## 📊 Analogía

```
Tienda de aplicaciones:

Python:     pip install requests
            (Descarga la librería 'requests' para Python)

Node.js:    npm install express
            (Descarga la librería 'express' para Node.js)
```

---

## 🎯 ¿Por qué lo necesitas en Sched-Anal?

Tu proyecto tiene dos partes:

### Backend (Python)
```
Python → Flask → Python packages (pandas, pdfplumber, etc.)
Instalas con: pip install -r requirements.txt
```

### Frontend (React)
```
Node.js → React → JavaScript packages (react, vite, etc.)
Instalas con: npm install
```

**npm es como pip, pero para el frontend.**

---

## 🔄 El Flujo

```
1. Descargaste el proyecto
        ↓
2. Proyecto tiene archivo: package.json
   (Similar a requirements.txt pero para JavaScript)
        ↓
3. Para ejecutar frontend necesitas: npm install
   (Descarga todas las librerías listadas en package.json)
        ↓
4. Luego ejecutas: npm run dev
   (Inicia el servidor de desarrollo)
```

---

## 📄 Ejemplo: package.json

Tu proyecto tiene un `package.json` que se ve así:

```json
{
  "name": "sched-anal",
  "version": "1.0.0",
  "dependencies": {
    "react": "18.2.0",
    "recharts": "2.8.0",
    "vite": "4.4.0",
    "tailwindcss": "3.3.0",
    "xlsx": "0.18.5"
  }
}
```

Cuando ejecutas `npm install`, npm:
1. Lee este archivo
2. Descarga cada librería
3. Las guarda en carpeta `node_modules/`
4. Crea archivo `package-lock.json` (versiones exactas)

---

## 🔗 Relación entre Node.js, npm y tu Proyecto

```
Node.js
  │
  ├─ Lenguaje: JavaScript
  ├─ Runtime: Ejecuta código JavaScript
  └─ Incluye: npm (automático)
      │
      └─ npm
          │
          ├─ Gestor de paquetes
          ├─ Descarga librerías JavaScript
          └─ Se usa así:
              npm install (instala dependencias)
              npm run dev (ejecuta scripts)
              npm run build (construye proyecto)
```

---

## 💾 ¿Qué se Descarga?

Cuando haces `npm install`, se crea:

```
sched-anal/
├── node_modules/           ← Todas las librerías descargadas (500+ MB)
├── package.json           ← Tu lista de dependencias
├── package-lock.json      ← Versiones exactas instaladas
└── ...
```

### ¿Por qué es tan grande?

Porque `node_modules/` contiene:
- React (UI framework)
- Vite (build tool)
- Tailwind CSS (estilos)
- XLSX (manejo de Excel)
- Y todas sus sub-dependencias (pueden ser cientos)

---

## 🎯 El Proceso Paso a Paso

### Paso 1: Instalar Node.js
```
Descargas de nodejs.org
Instalas
Se incluye npm automáticamente
```

### Paso 2: Verificar
```bash
node --version    # Verifica Node.js
npm --version     # Verifica npm
```

### Paso 3: Instalar Dependencias del Proyecto
```bash
npm install       # Lee package.json y descarga todo
```

### Paso 4: Ejecutar Proyecto
```bash
npm run dev       # Inicia el servidor de desarrollo
```

---

## 🔍 Comparación: pip vs npm

| Aspecto | pip (Python) | npm (JavaScript) |
|---------|--------------|------------------|
| **Qué es** | Package manager | Package manager |
| **Para** | Python | JavaScript/Node.js |
| **Instalas con** | `pip install <package>` | `npm install <package>` |
| **Archivo config** | `requirements.txt` | `package.json` |
| **Carpeta de librerías** | `site-packages/` | `node_modules/` |
| **Script runner** | No tiene | `npm run <script>` |
| **Instalar proyecto** | `pip install -r requirements.txt` | `npm install` |

---

## 📦 Tu Proyecto Necesita

### Backend (Python)
```bash
pip install -r requirements.txt
# Instala: Flask, pandas, pdfplumber, etc.
```

### Frontend (JavaScript)
```bash
npm install
# Instala: React, Vite, Tailwind, XLSX, etc.
```

---

## 🚀 Flujo Completo

```
1. Instalar Python
   ↓
2. Instalar Node.js (que incluye npm)
   ↓
3. Ir a carpeta del proyecto
   ↓
4. Instalar dependencias Python:    pip install -r requirements.txt
   Instalar dependencias JavaScript: npm install
   ↓
5. Ejecutar backend:                python app.py
   Ejecutar frontend:                npm run dev
   ↓
6. Abrir navegador:                 http://localhost:3000
   ↓
7. ✅ ¡Funciona!
```

---

## ❓ Preguntas Frecuentes

### ¿Necesito npm si solo uso Python?

No. npm es solo para el frontend (React).

Pero tu proyecto tiene frontend, así que sí lo necesitas.

---

### ¿Por qué npm descarga 500 MB?

Porque:
- React necesita muchas librerías
- Cada librería tiene sus propias dependencias
- Ejemplo: Tailwind CSS necesita postcss, que necesita otras cosas, etc.

Es normal. Después de `npm install` puedes eliminar `node_modules/` y reinstalar sin perder nada (guarda `package.json`).

---

### ¿Puedo usar npm en Mac/Linux?

Sí. npm funciona igual en todas las plataformas.

---

### ¿Qué es `npm run dev`?

Es un **comando definido** en `package.json`:

```json
"scripts": {
  "dev": "vite",
  "build": "vite build"
}
```

Cuando haces `npm run dev`, ejecuta `vite`.

Simplemente es un alias para escribir menos.

---

### ¿Qué es `package-lock.json`?

Archivo que guarda las **versiones exactas** instaladas.

Ejemplo:
- `package.json`: `"react": "18.2"`
- `package-lock.json`: `"react": "18.2.0"` (versión exacta con todas las sub-dependencias)

Esto asegura que todos usen exactamente lo mismo.

---

## 💡 Tips

1. **Primero instala Node.js** (con npm incluido)
   - Desde: https://nodejs.org/
   - Elige: LTS (Long Term Support)

2. **Marca "Add to PATH"** durante instalación
   - Crítico para que npm funcione desde terminal

3. **Reinicia terminal** después de instalar
   - Windows necesita leer el nuevo PATH

4. **`npm install` descarga 500+ MB**
   - Es normal
   - Solo necesitas hacerlo una vez
   - Después está todo en carpeta `node_modules/`

---

## 🔗 Instalación Rápida

```bash
# 1. Descargar Node.js LTS desde nodejs.org
# 2. Instalar y marcar "Add to PATH"
# 3. Reiniciar terminal
# 4. En tu proyecto:

npm install        # Descarga dependencias (toma 1-2 minutos)
npm run dev        # Inicia servidor de desarrollo
```

---

**¡Eso es npm en resumen! 🎉**

Es solo el "package manager" para JavaScript, como pip para Python.

---

**Versión**: 1.0.0  
**Fecha**: Nov 11, 2025  
**Tema**: npm/Node.js explicado
