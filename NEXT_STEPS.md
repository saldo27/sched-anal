# 🎯 Próximos Pasos - Sched-Anal

**Fecha**: Noviembre 11, 2025  
**Estado del Backend**: ✅ FUNCIONAL  
**Estado del Frontend**: 📋 LISTO PARA PROBAR

---

## 1️⃣ Verificar el Backend está ejecutándose

El backend Flask ya está corriendo en background. Verifica que funciona:

```bash
# Comprueba que el servidor responde
curl http://127.0.0.1:5000/health

# Deberías ver:
# {"status":"ok","version":"1.0.0"}
```

Si el servidor se detiene, reinicia:

```bash
cd /workspaces/sched-anal
python app.py
```

---

## 2️⃣ Ejecutar el Frontend (NUEVO)

Ahora ejecuta React en una **nueva terminal**:

```bash
cd /workspaces/sched-anal
npm run dev
```

**Resultado esperado:**
```
  VITE v4.4.9  ready in 1234 ms

  ➜  Local:   http://localhost:3000
  ➜  press h to show help
```

---

## 3️⃣ Abrir en el Navegador

Abre tu navegador y ve a:

```
http://localhost:3000
```

Deberías ver:
- 📊 Interfaz de Calendar Analyzer
- 📤 Sección de carga de archivos
- 📝 Área de entrada de texto
- 📈 Gráficos y resultados

---

## 4️⃣ Probar Funcionalidades

### A. Subir un PDF

1. Haz clic en **"📄 Cargar PDF"**
2. Selecciona un archivo PDF con horarios
3. El archivo se enviará al backend
4. Backend lo procesa con `pdfplumber`
5. Frontend muestra el texto extraído

### B. Subir un Excel

1. Haz clic en **"📊 Cargar Excel"**
2. Selecciona un archivo `.xlsx` o `.xls`
3. Frontend lo procesa localmente con la librería XLSX
4. Muestra los datos en la tabla

### C. Subir un CSV

1. Haz clic en **"📋 Cargar CSV"**
2. Selecciona un archivo `.csv`
3. Frontend lo procesa con XLSX
4. Muestra datos estructurados

### D. Entrada de Texto Manual

1. Pegue horarios directamente en el área de texto
2. Haz clic en **Analizar**
3. El sistema detecta automáticamente la estructura

---

## 5️⃣ Flujo Completo Esperado

```
Usuario sube PDF
    ↓
Frontend envía a: POST /api/upload
    ↓
Backend recibe y procesa con pdfplumber
    ↓
Backend extrae texto y detecta estructura
    ↓
Backend devuelve: JSON con texto extraído
    ↓
Frontend muestra:
  - Texto extraído
  - Estructura detectada
  - Tabla de trabajadores
  - Gráficos de análisis
    ↓
Usuario hace clic en Exportar
    ↓
Frontend envía a: POST /api/export
    ↓
Backend genera CSV o JSON
    ↓
Archivo se descarga
```

---

## 6️⃣ Archivos de Prueba

Si necesitas archivos para probar:

```bash
# Generar datos de ejemplo
python create_sample_data.py      # Crea sample_data.csv

# Generar múltiples meses
python create_multi_month_sample.py  # Crea 3 meses de datos

# Generar PDF de prueba
python create_test_pdf.py         # Crea test_calendar.pdf
```

---

## 🐛 Troubleshooting

### "Error al cargar PDF"
- Verifica que el backend está corriendo: `curl http://127.0.0.1:5000/health`
- Mira la consola de browser (F12) para ver error específico
- Mira logs del backend en su terminal

### "Cannot GET /api/upload"
- Verifica proxy en `vite.config.js` (debe tener `/api` → `http://localhost:5000`)
- Reinicia frontend: `npm run dev`
- Backend debe estar en puerto 5000

### "React component not loading"
```bash
# Limpia cache y reinstala
rm -rf node_modules
npm install
npm run dev
```

### "Port already in use"
```bash
# Detén el proceso anterior
# Linux/macOS:
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

---

## 📊 Monitorear los Servidores

### Backend (Terminal 1)
```bash
# Verifica que está corriendo
ps aux | grep "python app.py"

# Logs en vivo:
cd /workspaces/sched-anal
python app.py
# Ver output en tiempo real
```

### Frontend (Terminal 2)
```bash
# Verifica que está corriendo
ps aux | grep "vite"

# Logs en vivo:
cd /workspaces/sched-anal
npm run dev
# Ver output en tiempo real
```

---

## ✅ Checklist de Verificación

- [ ] Backend corriendo: `curl http://127.0.0.1:5000/health`
- [ ] Frontend iniciado: `npm run dev`
- [ ] Navegador abierto: http://localhost:3000
- [ ] UI visible: Interfaz de Calendar Analyzer
- [ ] Botones de carga presentes: PDF, Excel, CSV, Texto
- [ ] Gráficos visibles en la página
- [ ] Console del browser sin errores (F12)
- [ ] Logs del backend sin errores

---

## 🔄 Ciclo de Desarrollo

Cuando hagas cambios:

### Backend (Python)
```bash
# 1. Edita app.py o file_processor.py
# 2. Detén: Ctrl+C en terminal backend
# 3. Reinicia: python app.py
```

### Frontend (React)
```bash
# 1. Edita CalendarAnalyzer.jsx
# 2. Frontend se recarga automáticamente
# 3. Actualiza navegador F5
```

---

## 📚 Documentación Disponible

- **START_HERE.md** - Introducción
- **QUICKSTART.md** - Guía rápida (5 min)
- **DEVELOPMENT.md** - Desarrollo técnico
- **FILE_UPLOAD_GUIDE.md** - API endpoints
- **PDF_FIX.md** - Solución error PDF
- **WATCHDOG_FIX.md** - Solución error watchdog
- **STATUS.md** - Estado actual del proyecto

---

## 🚀 Próximas Características (Opcional)

Si quieres extender la aplicación:

- [ ] Autenticación de usuarios
- [ ] Base de datos para guardar análisis
- [ ] Gráficos más avanzados
- [ ] Exportar a PDF
- [ ] Historial de análisis
- [ ] Comparación entre períodos
- [ ] Email con resultados
- [ ] API de terceros (calendarios, notificaciones)

---

## 💡 Tips

1. **Dev Tools del navegador** (F12): Muy útil para debug
2. **Network tab**: Ve las peticiones al backend
3. **Console**: Busca errores de JavaScript
4. **Backend logs**: Terminal del servidor muestra peticiones HTTP
5. **Vite logs**: Terminal del frontend muestra cambios detectados

---

## 📞 Contacto / Soporte

Si algo no funciona:

1. Mira **STATUS.md** (estado actual)
2. Busca en **PDF_FIX.md** o **WATCHDOG_FIX.md**
3. Revisa logs en ambas terminales
4. Verifica que ambos servidores están corriendo
5. Abre console del navegador (F12)

---

**¡Listo para desarrollar! 🎉**

Ejecuta en dos terminales:
```bash
# Terminal 1
python app.py

# Terminal 2
npm run dev
```

Luego abre: http://localhost:3000
