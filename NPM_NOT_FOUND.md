# 🔧 Solución: "npm" no se reconoce en Windows

## ❌ Problema

```
C:\Py\cal>npm install
"npm" no se reconoce como un comando interno o externo,
programa o archivo por lotes ejecutable.
```

## 🔍 Causa

- Node.js **no está instalado**, O
- Node.js está instalado pero **NO está en el PATH**, O
- La terminal no reconoce los cambios del PATH

---

## ✅ SOLUCIONES (Elige una)

### Solución 1: Instalar Node.js (PRIMERA - Más Probable)

**Paso 1: Descargar Node.js**

Abre navegador y ve a: https://nodejs.org/

Descarga la versión **LTS** (Long Term Support):
- Haz clic en "Download" (el botón más grande)
- Elige **Windows Installer (.msi)**

**Paso 2: Instalar**

1. Abre el archivo descargado (`.msi`)
2. Haz clic en "Next" varias veces
3. **IMPORTANTE**: En "Custom Setup", asegúrate que está marcado:
   - ✅ "Add to PATH" (muy importante)
   - ✅ "npm package manager"
4. Haz clic en "Install"
5. Espera a que termine
6. Haz clic en "Finish"

**Paso 3: Reinicia la terminal**

Cierra la terminal actual completamente.

Abre una **NUEVA** terminal (CMD o PowerShell).

**Paso 4: Verifica instalación**

```bash
node --version
npm --version
```

Deberías ver versiones, ejemplo:
```
v18.19.0
9.6.7
```

**Paso 5: Ahora sí puede instalar**

```bash
npm install
npm run dev
```

---

### Solución 2: Node.js Instalado pero NO en PATH

Si sabes que Node.js está instalado pero npm no funciona:

**Opción A: Agregar manualmente al PATH**

1. Busca dónde está Node.js instalado:
   - Típicamente: `C:\Program Files\nodejs`
   - O: `C:\Program Files (x86)\nodejs`

2. Abre "Variables de entorno":
   - Presiona: `Ctrl+Pause/Break` (o busca "environment variables")
   - O: Haz clic derecho en "Este Equipo" → "Propiedades" → "Configuración avanzada del sistema"

3. Haz clic en "Variables de entorno"

4. Busca "Path" en "Variables del sistema"

5. Haz clic en "Editar"

6. Haz clic en "Nuevo"

7. Agrega: `C:\Program Files\nodejs`

8. Haz clic en "Aceptar" (varias veces hasta cerrar todo)

9. **Reinicia la terminal**

10. Prueba:
```bash
npm --version
```

**Opción B: Usar ruta completa (Temporal)**

En lugar de `npm`, usa la ruta completa:

```bash
"C:\Program Files\nodejs\npm" install
```

Pero esto es solo temporal. Mejor hacer Option A.

---

### Solución 3: Reinstalar Node.js Completamente

Si nada funciona, desinstala y reinstala:

**Paso 1: Desinstalar**

1. Abre "Agregar o quitar programas"
2. Busca "Node.js"
3. Haz clic en él
4. Haz clic en "Desinstalar"
5. Sigue los pasos

**Paso 2: Limpiar PATH (Opcional pero recomendado)**

1. Abre "Variables de entorno"
2. Busca referencias a `nodejs` en Path
3. Elimínalas si existen

**Paso 3: Reinicia la computadora**

```
Windows → Reiniciar
```

**Paso 4: Descarga e instala Node.js nuevamente**

1. Ve a: https://nodejs.org/
2. Descarga LTS (Long Term Support)
3. Instala normalmente
4. **Asegúrate de marcar "Add to PATH"**

**Paso 5: Abre nueva terminal y prueba**

```bash
node --version
npm --version
```

---

### Solución 4: Usar Alternativa (Rápida - No Recomendada)

Si necesitas que funcione **YA** sin esperar a instalar:

Edita `run-frontend.bat` y cambia:

```batch
REM ANTES:
call npm run dev

REM DESPUÉS (temporal, mientras instalas Node.js):
cd /d "%SCRIPT_DIR%\.venv\Scripts" && activate && pip install nodeenv && nodeenv --node=18.19.0 && call npm run dev
```

**PERO MEJOR INSTALA NODE.JS DIRECTAMENTE** (Solución 1)

---

## 🎯 RECOMENDACIÓN PARA TI

### Paso a Paso Rápido:

1. **Ve a**: https://nodejs.org/
2. **Descarga**: Versión LTS (18.x)
3. **Instala**: Haz doble clic, sigue pasos, marca "Add to PATH"
4. **Reinicia**: Cierra y abre nueva terminal
5. **Verifica**: `npm --version`
6. **Ejecuta**: `npm install`
7. **Corre**: `npm run dev`

**Tiempo total**: 5-10 minutos

---

## ✅ Verificar que Funciona

Después de instalar Node.js y reiniciar:

**En CMD o PowerShell:**

```bash
# Verifica Node.js
node --version

# Verifica npm
npm --version

# Deberías ver versiones, NO errores
```

Si ves versiones (como `v18.19.0` y `9.6.7`), ¡está correcto!

---

## 🚀 Una Vez Que npm Funciona

```bash
# En tu carpeta C:\Py\cal

# 1. Instala dependencias
npm install

# 2. Ejecuta frontend
npm run dev

# 3. Abre en navegador
http://localhost:3000
```

---

## 📋 Checklist

- [ ] Descargué Node.js LTS de nodejs.org
- [ ] Instalé Node.js
- [ ] Marcé "Add to PATH" durante instalación
- [ ] Reinicié la terminal (cerré y abrí nueva)
- [ ] `node --version` funciona
- [ ] `npm --version` funciona
- [ ] `npm install` funciona en C:\Py\cal
- [ ] ¡Listo! 🎉

---

## 💡 Tips

1. **Descarga la versión LTS** (no Latest)
   - LTS = Long Term Support = más estable
   - Actualmente es v18.x

2. **Marca "Add to PATH"** durante instalación
   - Es muy importante
   - Sin esto, npm no funcionará

3. **Reinicia la terminal** después de instalar
   - Windows necesita leer el nuevo PATH
   - No es suficiente cerrar y abrir en la misma terminal
   - Mejor: Cierra todo, abre una nueva terminal

4. **Si aún no funciona**, abre una terminal **NUEVA**
   - Algunos programas cache el PATH
   - Una nueva terminal limpia lo arreglará

---

## 🔍 Debug Avanzado

Si después de todo sigue sin funcionar:

### Opción A: Busca manualmente dónde está npm

```bash
where npm
```

Si ve una ruta, significa que SÍ está instalado.

### Opción B: Verifica que está en PATH

```bash
echo %PATH%
```

Busca `nodejs` en la salida. Si no está, necesitas agregarlo manualmente (Solución 2 Option A).

### Opción C: Usa ruta completa

Si `where npm` devuelve una ruta como:
```
C:\Program Files\nodejs\npm.cmd
```

Entonces usa:
```bash
"C:\Program Files\nodejs\npm" install
```

Esto funcionará temporalmente. Pero agrega a PATH para permanente.

---

## 🔗 Recursos

- **Node.js Oficial**: https://nodejs.org/
- **npm Documentación**: https://docs.npmjs.com/
- **Microsoft Dev Setup**: https://docs.microsoft.com/en-us/windows/dev-environment/

---

## 📞 Si Persiste el Problema

1. Verifica con `node --version` que Node.js funciona
2. Si Node.js funciona pero npm no, es un problema de PATH
3. Agrega manualmente a PATH (Solución 2 Option A)
4. Reinicia computadora completa
5. Prueba en nueva terminal

---

## ✨ Después de Resolver

Una vez que npm funciona:

```bash
# Instala dependencias del proyecto
npm install

# Ejecuta frontend
npm run dev

# Abre backend en otra terminal
python app.py

# Abre navegador
http://localhost:3000
```

---

**Versión**: 1.0.0  
**Fecha**: Nov 11, 2025  
**Para**: Windows 10/11  
**Estado**: ✅ Probado

---

**¡Gracias por usar Sched-Anal! 🚀**
