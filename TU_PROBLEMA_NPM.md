# 🎯 Tu Nuevo Problema: npm no se reconoce

**Fecha**: Noviembre 11, 2025  
**Tu Error**: `"npm" no se reconoce como un comando interno o externo`

---

## ¿Qué Significa?

Windows no encuentra el comando `npm`.

Esto significa: **Node.js no está instalado** (o no está configurado correctamente).

---

## ✅ La Solución (3 Pasos Rápidos)

### Paso 1: Instalar Node.js

**Abre navegador y ve a:**
```
https://nodejs.org/
```

**Haz clic en el botón grande verde "Download"** (versión LTS)

Este descargará un archivo `.msi` (instalador Windows).

---

### Paso 2: Instalar

Abre el archivo descargado y:

1. Haz clic en **"Next"** varias veces
2. Cuando veas la pantalla de "Custom Setup", asegúrate que está marcado:
   - ✅ **"Add to PATH"** (CRÍTICO)
   - ✅ **"npm package manager"** (Importante)
3. Haz clic en **"Install"**
4. Espera (toma 1-2 minutos)
5. Haz clic en **"Finish"**

---

### Paso 3: Reinicia la Terminal

**Cierra completamente** la terminal actual.

Abre una **NUEVA** terminal (CMD o PowerShell).

Ejecuta:
```bash
npm --version
```

Deberías ver un número (ej: `9.6.7`), no un error.

---

## 🚀 Una Vez Que npm Funciona

En tu carpeta `C:\Py\cal`:

```bash
# 1. Instala dependencias del proyecto
npm install

# 2. Ejecuta el frontend
npm run dev

# 3. En otra terminal, ejecuta el backend
python app.py

# 4. Abre navegador
http://localhost:3000
```

---

## 🔍 Verificar que Está Instalado

Ejecuta esto en una terminal nueva:

```bash
node --version
npm --version
```

Deberías ver dos versiones. Ejemplo:
```
v18.19.0
9.6.7
```

Si ves versiones, está correcto. ✅

Si ves errores, sigue estos pasos:

1. Reinicia la computadora
2. Abre una terminal nueva
3. Prueba de nuevo

---

## 📝 Instrucciones Detalladas

Si necesitas más detalles, lee:

**[NPM_NOT_FOUND.md](NPM_NOT_FOUND.md)**

Este documento tiene:
- ✅ 4 soluciones diferentes
- ✅ Explicación de cada paso
- ✅ Troubleshooting avanzado

---

## 💡 Puntos Clave

1. **Node.js = Necesario para frontend**
   - React usa JavaScript
   - JavaScript se ejecuta con Node.js

2. **npm = Viene con Node.js**
   - Cuando instalas Node.js, npm se instala automáticamente
   - No necesitas instalarlo por separado

3. **"Add to PATH" = Crítico**
   - Sin esto, Windows no encuentra npm
   - ASEGÚRATE de marcar esta opción durante la instalación

4. **Reinicia terminal**
   - Después de instalar, cierra y abre una terminal NUEVA
   - Windows necesita leer el nuevo PATH

---

## 🎯 Tu Próximo Paso

1. Ve a: https://nodejs.org/
2. Descarga: LTS (el grande verde)
3. Instala: Marca "Add to PATH"
4. Reinicia: Terminal nueva
5. Verifica: `npm --version`
6. Ejecuta: `npm install` en C:\Py\cal
7. ¡Listo! 🎉

---

## ⏱️ Tiempo Estimado

- Descargar Node.js: 2-5 minutos
- Instalar: 2-3 minutos
- Configurar npm install: 2-3 minutos

**Total: 10-15 minutos**

---

## 📦 ¿Qué es npm?

Si no sabes qué es npm:

Lee: **[ENTENDER_NPM.md](ENTENDER_NPM.md)**

Explica:
- Qué es npm (versión simple)
- Por qué lo necesitas
- Cómo funciona

---

## ✅ Checklist

- [ ] Descargué Node.js LTS de nodejs.org
- [ ] Instalé Node.js
- [ ] Marqué "Add to PATH"
- [ ] Cerré la terminal anterior
- [ ] Abrí una NUEVA terminal
- [ ] `npm --version` funciona
- [ ] `npm install` funciona en C:\Py\cal
- [ ] ¡Listo! 🎉

---

**¡Adelante! Estás casi listo para usar la app. 🚀**

---

**Si tienes problemas:**
- Lee: NPM_NOT_FOUND.md (soluciones detalladas)
- Lee: ENTENDER_NPM.md (qué es npm)
- Corre: check-requirements.bat (verifica todo)

---

**Versión**: 1.0.0  
**Fecha**: Nov 11, 2025  
**Para**: Tu problema específico de npm
