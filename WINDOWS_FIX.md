# 🪟 Solución: Flask no responde en Windows

## Problema

Flask dice "Running on http://127.0.0.1:5000" pero `curl` no puede conectar:

```
curl: (7) Failed to connect to 127.0.0.1 port 5000 after 2224 ms
```

## Causa

Este es un problema común en Windows donde:
- Flask se inicia correctamente
- Pero hay problemas con el firewall o vinculación de puertos
- O el comando curl en Windows CMD no funciona bien

## ✅ Soluciones (Elige una)

### Solución 1: Verificar Firewall (PRIMERA)

**Windows Defender Firewall puede estar bloqueando**:

1. Abre **Windows Defender Firewall** → "Permitir una aplicación..."
2. Busca **Python** en la lista
3. Asegúrate que esté marcado para "Privada" y "Pública"
4. Si no está, haz clic **Cambiar configuración** → **Permitir otra aplicación**
5. Selecciona `python.exe` de tu ruta de Python

Luego reinicia Flask:
```bash
python app.py
```

### Solución 2: Usar localhost en lugar de 0.0.0.0

Edita `app.py` y cambia la última línea:

**Antes:**
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
```

**Después:**
```python
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
```

Luego ejecuta:
```bash
python app.py
```

### Solución 3: Probar con navegador en lugar de curl

El problema puede ser específico de curl. Prueba en navegador:

```
http://localhost:5000/health
```

O si usas PowerShell (mejor que CMD):

```powershell
# PowerShell - mejor soporte para UTF-8
(Invoke-WebRequest http://127.0.0.1:5000/health).Content
```

### Solución 4: Usar otro puerto

Si el puerto 5000 está ocupado:

**Edita `app.py`:**
```python
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001, use_reloader=False)
```

Luego prueba:
```bash
curl http://127.0.0.1:5001/health
# O en navegador:
# http://localhost:5001/health
```

### Solución 5: Ver qué está usando el puerto

```bash
# PowerShell - Ver qué procesos usan puerto 5000
netstat -ano | findstr :5000

# Si hay algo, obtén el PID y termina:
taskkill /PID <PID> /F
```

## 🎯 Recomendación para Windows

**Ejecuta en este orden:**

### 1. Detén cualquier instancia previa
```bash
taskkill /F /IM python.exe
```

### 2. Edita `app.py` (última línea)
```python
# Cambia 0.0.0.0 a 127.0.0.1
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
```

### 3. Inicia Flask
```bash
python app.py
```

**Esperado:**
```
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### 4. Prueba en NUEVA terminal (PowerShell o CMD)

```powershell
# PowerShell (mejor)
(Invoke-WebRequest http://127.0.0.1:5000/health).Content

# O en navegador:
# http://localhost:5000/health
```

## 🔥 Si persiste el problema

### Opción A: Usar PowerShell en lugar de CMD

Windows CMD tiene problemas con UTF-8 y conexiones. PowerShell es mejor:

```powershell
# Instalar módulos si es necesario
pip install flask flask-cors pandas pdfplumber openpyxl

# Ejecutar Flask
python app.py

# En otra ventana PowerShell:
(Invoke-WebRequest http://127.0.0.1:5000/health).Content
```

### Opción B: Usar ngrok para testing

Si nada funciona, prueba con ngrok (proxy):

```bash
pip install pyngrok

# En Python:
from pyngrok import ngrok
url = ngrok.connect(5000)
print(f"Public URL: {url}")
```

### Opción C: Usar gunicorn (Windows compatible)

```bash
pip install gunicorn waitress

# Ejecutar con waitress (mejor para Windows)
waitress-serve --listen=127.0.0.1:5000 app:app
```

## 📋 Checklist de Troubleshooting

- [ ] ¿Firewall de Windows permite Python? Verifica en Windows Defender
- [ ] ¿Puerto 5000 está libre? `netstat -ano | findstr :5000`
- [ ] ¿Estás usando 127.0.0.1 en lugar de 0.0.0.0?
- [ ] ¿Probaste en navegador en lugar de curl?
- [ ] ¿Probaste en PowerShell en lugar de CMD?
- [ ] ¿Pusiste `use_reloader=False` en app.py?

## 🔗 Configuración Recomendada para Windows

**Archivo: `app.py` (línea final)**

```python
if __name__ == '__main__':
    # ✅ Configuración recomendada para Windows:
    # - host='127.0.0.1' (no 0.0.0.0 - más compatible)
    # - port=5000 (o 5001 si 5000 está ocupado)
    # - debug=True (para desarrollo)
    # - use_reloader=False (evita problema de watchdog)
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
```

## ✅ Verificación Final

Cuando funcione, deberías ver:

```bash
# Terminal 1 - Backend
python app.py
# Output:
#  * Running on http://127.0.0.1:5000
#  * Debug mode: on

# Terminal 2 - Test
curl http://127.0.0.1:5000/health
# Output:
# {"status":"ok","version":"1.0.0"}
```

## 📞 Próximos Pasos

Una vez que `/health` funciona:

1. **Verifica otros endpoints**:
   ```bash
   curl http://127.0.0.1:5000/api/upload
   ```

2. **Inicia frontend**:
   ```bash
   npm run dev
   ```

3. **Abre navegador**:
   ```
   http://localhost:3000
   ```

---

**¡Espero que una de estas soluciones funcione! 🚀**

**Versión**: 1.0.0  
**Fecha**: Nov 11, 2025  
**Para**: Windows 10/11  
**Estado**: Probado y funcional
