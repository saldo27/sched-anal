import React, { useState, useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Upload, FileText, Download, AlertCircle } from 'lucide-react';
import * as XLSX from 'xlsx';

const CalendarAnalyzer = () => {
  const [calendarText, setCalendarText] = useState('');
  const [startDate, setStartDate] = useState('2025-12-22');
  const [nameMapping, setNameMapping] = useState('luis h=LUIS H\nluish=LUIS H\nreque=LUIS R\nrobert=ROBERTO\nagueda=AGUEDA\nluisH=LUIS H');
  const [sortBy, setSortBy] = useState('total');
  const [view, setView] = useState('general');
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [error, setError] = useState('');
  const [fileName, setFileName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [chartStartIndex, setChartStartIndex] = useState(0);

  // Función para limpiar y normalizar nombres (case-insensitive)
  const normalizeWorkerName = (name, nameMap, nameMapUpper) => {
    if (!name) return null;
    
    const trimmed = name.trim();
    const upper = trimmed.toUpperCase();
    
    // Búsqueda exact case-sensitive primero
    if (nameMap[trimmed]) return nameMap[trimmed];
    
    // Búsqueda case-insensitive
    if (nameMapUpper[upper]) return nameMapUpper[upper];
    
    // Buscar en el mapeo por aproximación
    for (const [key, value] of Object.entries(nameMap)) {
      if (trimmed.toUpperCase().includes(key.toUpperCase()) || 
          key.toUpperCase().includes(trimmed.toUpperCase())) {
        return value;
      }
    }
    
    return trimmed;
  };

  // Detectar si una palabra es probablemente una inicial (apellido o nombre corto)
  const isLikelyInitial = (word) => {
    // Una sola letra o dos letras máximo
    // O un patrón como "H." o "h."
    return /^[A-Za-z]\.?$|^[A-Za-z]{1,2}$/.test(word);
  };

  // Función mejorada para parsear nombres de trabajadores
  const parseWorkerNames = (rowText, dayCount, nameMap, nameMapUpper) => {
    const words = rowText.trim().split(/\s+/);
    const workers = [];
    
    // Si tenemos exactamente el número correcto de palabras, podría ser simple
    // pero aún puede haber nombres compuestos - verificar primero
    if (words.length === dayCount) {
      // Revisar si hay palabras que parecen iniciales
      let hasInitials = false;
      for (let i = 1; i < words.length; i++) {
        if (isLikelyInitial(words[i])) {
          hasInitials = true;
          break;
        }
      }
      
      // Si no hay iniciales obvias, es probablemente un mapeo simple
      if (!hasInitials) {
        return words.map(w => normalizeWorkerName(w, nameMap, nameMapUpper));
      }
    }
    
    // Agrupar nombres compuestos combinando palabras cortas (iniciales)
    let wordIndex = 0;
    for (let i = 0; i < dayCount && wordIndex < words.length; i++) {
      let currentName = words[wordIndex];
      wordIndex++;
      
      // Combinar palabras cortas (iniciales o apellidos) con el nombre
      while (wordIndex < words.length && isLikelyInitial(words[wordIndex])) {
        currentName += ' ' + words[wordIndex];
        wordIndex++;
      }
      
      workers.push(normalizeWorkerName(currentName, nameMap, nameMapUpper));
    }
    
    return workers.filter(w => w);
  };

  const parseCalendar = (text, startDateStr, mappings) => {
    try {
      setError('');
      // Crear mapeo de nombres (case-sensitive y case-insensitive)
      const nameMap = {};
      const nameMapUpper = {}; // Para búsqueda case-insensitive
      
      mappings.split('\n').forEach(line => {
        const [from, to] = line.split('=').map(s => s.trim());
        if (from && to) {
          nameMap[from] = to;
          nameMapUpper[from.toUpperCase()] = to;
        }
      });

      // Parsear el texto del calendario
      const lines = text.trim().split('\n').filter(l => l.trim());
      const calendarData = [];
      
      let currentDate = new Date(startDateStr);
      
      for (let i = 0; i < lines.length; i += 5) {
        const daysLine = lines[i].trim().split(/\s+/);
        const dayCount = daysLine.length;
        
        // Usar la función mejorada para parsear nombres
        const row1 = parseWorkerNames(lines[i + 1] || '', dayCount, nameMap, nameMapUpper);
        const row2 = parseWorkerNames(lines[i + 2] || '', dayCount, nameMap, nameMapUpper);
        const row3 = parseWorkerNames(lines[i + 3] || '', dayCount, nameMap, nameMapUpper);
        const row4 = parseWorkerNames(lines[i + 4] || '', dayCount, nameMap, nameMapUpper);
        
        for (let j = 0; j < daysLine.length; j++) {
          const day = parseInt(daysLine[j]);
          
          // Si el día es menor que el anterior, cambiar de mes
          if (j > 0 && day < parseInt(daysLine[j - 1] || 0)) {
            // Cambiar de mes
            const nextMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
            currentDate = nextMonth;
          }
          
          // Establecer el día correcto del mes actual
          currentDate.setDate(day);
          
          const workers = [row1[j], row2[j], row3[j], row4[j]]
            .filter(w => w)
            .map(w => w);
          
          calendarData.push({
            day: day,
            month: currentDate.getMonth() + 1,
            year: currentDate.getFullYear(),
            workers: workers
          });
        }
      }
      
      return calendarData;
    } catch (error) {
      console.error('Error parsing calendar:', error);
      setError(`Error al parsear el calendario: ${error.message}`);
      return [];
    }
  };

  const handlePDFUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setError('');
      setFileName(file.name);
      setIsLoading(true);
      
      const formData = new FormData();
      formData.append('file', file);
      
      // Usar el backend API para procesar el PDF
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al cargar el archivo');
      }
      
      const data = await response.json();
      setCalendarText(data.text);
      setIsLoading(false);
    } catch (err) {
      setError(`Error al cargar PDF: ${err.message}`);
      setFileName('');
      setIsLoading(false);
    }
  };

  const handleExcelUpload = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setError('');
      setFileName(file.name);
      const reader = new FileReader();
      
      reader.onload = (e) => {
        try {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: 'array' });
          
          // Obtener la primera hoja
          const firstSheet = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[firstSheet];
          
          // Convertir a CSV para mantener el formato de texto
          const csv = XLSX.utils.sheet_to_csv(worksheet, { blankrows: false });
          
          // Convertir CSV a formato similar al del calendario
          const lines = csv.split('\n').filter(l => l.trim());
          const formattedText = lines.map(line => 
            line.split(',').map(cell => cell.trim()).filter(c => c).join(' ')
          ).join('\n');
          
          setCalendarText(formattedText);
          setIsLoading(false);
        } catch (err) {
          setError(`Error al procesar Excel: ${err.message}`);
          setFileName('');
          setIsLoading(false);
        }
      };
      
      reader.onerror = () => {
        setError('Error al leer el archivo');
        setFileName('');
        setIsLoading(false);
      };
      
      reader.readAsArrayBuffer(file);
    } catch (err) {
      setError(`Error al cargar archivo: ${err.message}`);
      setFileName('');
      setIsLoading(false);
    }
  };

  const handleTextInputChange = (e) => {
    setCalendarText(e.target.value);
    if (e.target.value.trim()) {
      setFileName('(Ingreso manual)');
    }
  };

  const calendarData = useMemo(() => {
    if (!calendarText || !showAnalysis) return [];
    return parseCalendar(calendarText, startDate, nameMapping);
  }, [calendarText, startDate, nameMapping, showAnalysis]);

  const analysis = useMemo(() => {
    if (calendarData.length === 0) return {};
    
    const workers = {};
    
    calendarData.forEach(dayData => {
      const date = new Date(dayData.year, dayData.month - 1, dayData.day);
      const dayOfWeek = date.getDay();
      
      const isFriday = dayOfWeek === 5;
      const isSaturday = dayOfWeek === 6;
      const isSunday = dayOfWeek === 0;
      const isWeekend = isFriday || isSaturday || isSunday;
      
      dayData.workers.forEach((worker, position) => {
        if (!workers[worker]) {
          workers[worker] = {
            total: 0,
            friday: 0,
            saturday: 0,
            sunday: 0,
            weekend: 0,
            lastPosition: 0,
            december: 0,
            january: 0,
            february: 0,
            march: 0,
            april: 0,
            may: 0,
            june: 0,
            july: 0,
            august: 0,
            september: 0,
            october: 0,
            november: 0
          };
        }
        
        workers[worker].total++;
        if (isFriday) workers[worker].friday++;
        if (isSaturday) workers[worker].saturday++;
        if (isSunday) workers[worker].sunday++;
        if (isWeekend) workers[worker].weekend++;
        if (position === 3) workers[worker].lastPosition++;
        
        const monthNames = ['january', 'february', 'march', 'april', 'may', 'june', 
                           'july', 'august', 'september', 'october', 'november', 'december'];
        const monthKey = monthNames[dayData.month - 1];
        if (monthKey) workers[worker][monthKey]++;
      });
    });
    
    return workers;
  }, [calendarData]);

  const sortedWorkers = useMemo(() => {
    const workerArray = Object.entries(analysis).map(([name, stats]) => ({
      name,
      ...stats,
      weekendPercentage: stats.total > 0 ? ((stats.weekend / stats.total) * 100).toFixed(1) : '0.0'
    }));
    
    return workerArray.sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      if (sortBy === 'weekendPercentage') return parseFloat(b.weekendPercentage) - parseFloat(a.weekendPercentage);
      return b[sortBy] - a[sortBy];
    });
  }, [analysis, sortBy]);

  const handleAnalyze = () => {
    if (calendarText.trim()) {
      setShowAnalysis(true);
    } else {
      setError('Por favor, carga un archivo o ingresa el texto del calendario');
    }
  };

  const handleReset = () => {
    setShowAnalysis(false);
    setCalendarText('');
    setFileName('');
    setError('');
  };

  const handleExportCSV = () => {
    let csv = 'Trabajador,Total,Viernes,Sábado,Domingo,% Fin de Semana,Rosell\n';
    sortedWorkers.forEach(worker => {
      csv += `"${worker.name}",${worker.total},${worker.friday},${worker.saturday},${worker.sunday},${worker.weekendPercentage},${worker.lastPosition}\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `analisis_turnos_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const handleExportPDF = async () => {
    try {
      // Preparar datos mensuales para PDF
      const monthlyForPDF = sortedWorkers.map(w => ({
        name: w.name,
        'Dic': w.december || 0,
        'Ene': w.january || 0,
        'Feb': w.february || 0,
        'Mar': w.march || 0,
        'Abr': w.april || 0,
        'May': w.may || 0,
        'Jun': w.june || 0,
        'Jul': w.july || 0,
        'Ago': w.august || 0,
        'Sep': w.september || 0,
        'Oct': w.october || 0,
        'Nov': w.november || 0
      }));

      console.log('Monthly data for PDF:', monthlyForPDF);

      const payload = {
        workers: sortedWorkers,
        monthlyData: monthlyForPDF,
        format: 'pdf',
        analysisPeriod: startDate ? new Date(startDate).toLocaleDateString('es-ES', { year: 'numeric', month: 'long' }) : 'Análisis de Turnos'
      };

      console.log('PDF payload:', payload);

      const response = await fetch('/api/export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        // Intentar leer el error
        let errorText = '';
        try {
          const errorData = await response.json();
          errorText = errorData.error || `Error ${response.status}`;
        } catch {
          errorText = `Error ${response.status}`;
        }
        throw new Error(errorText);
      }

      const blob = await response.blob();
      
      // Verificar que el blob sea realmente un PDF
      if (blob.type !== 'application/pdf' && !blob.type.startsWith('application/pdf')) {
        const text = await blob.text();
        console.error('Response no es PDF:', text.substring(0, 200));
        throw new Error('La respuesta no es un PDF válido');
      }
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analisis_guardias_${new Date().toISOString().split('T')[0]}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
      
      alert('PDF descargado correctamente');
    } catch (error) {
      console.error('Error exporting PDF:', error);
      alert('Error al exportar PDF: ' + error.message);
    }
  };

  // Definir todos los meses disponibles
  const allMonths = [
    { key: 'Dic', value: 'december' },
    { key: 'Ene', value: 'january' },
    { key: 'Feb', value: 'february' },
    { key: 'Mar', value: 'march' },
    { key: 'Abr', value: 'april' },
    { key: 'May', value: 'may' },
    { key: 'Jun', value: 'june' },
    { key: 'Jul', value: 'july' },
    { key: 'Ago', value: 'august' },
    { key: 'Sep', value: 'september' },
    { key: 'Oct', value: 'october' },
    { key: 'Nov', value: 'november' }
  ];

  // Calcular qué meses tienen turnos reales (suma > 0)
  const monthsWithShifts = allMonths.filter(month => {
    const total = sortedWorkers.reduce((sum, worker) => sum + (worker[month.value] || 0), 0);
    return total > 0;
  });

  const monthlyChartData = sortedWorkers.map(w => ({
    name: w.name,
    'Dic': w.december,
    'Ene': w.january,
    'Feb': w.february,
    'Mar': w.march,
    'Abr': w.april,
    'May': w.may,
    'Jun': w.june,
    'Jul': w.july,
    'Ago': w.august,
    'Sep': w.september,
    'Oct': w.october,
    'Nov': w.november
  }));

  if (!showAnalysis) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-xl p-8">
            <div className="text-center mb-8">
              <FileText className="w-16 h-16 mx-auto text-indigo-600 mb-4" />
              <h1 className="text-4xl font-bold text-gray-800 mb-2">
                Analizador de Calendarios de Guardias
              </h1>
              <p className="text-gray-600">
                Carga PDF, Excel o pega el texto de tu calendario y obtén estadísticas detalladas
              </p>
            </div>

            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex gap-2">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <p className="text-red-700">{error}</p>
              </div>
            )}

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Fecha de inicio del calendario
                </label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Mapeo de nombres (formato: NOMBRE_CORTO=NOMBRE_COMPLETO)
                </label>
                <textarea
                  value={nameMapping}
                  onChange={(e) => setNameMapping(e.target.value)}
                  rows={3}
                  placeholder="REQUE=LUIS R&#10;ROBER=ROBERTO"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-mono text-sm"
                />
              </div>

              <div className="border-2 border-dashed border-indigo-300 rounded-lg p-6 bg-indigo-50">
                <label className="block text-sm font-semibold text-gray-700 mb-4">
                  Cargar archivo o ingresar texto
                </label>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-2">
                      Cargar archivo PDF
                    </label>
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handlePDFUpload}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm cursor-pointer hover:bg-gray-50"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-2">
                      Cargar archivo Excel
                    </label>
                    <input
                      type="file"
                      accept=".xlsx,.xls,.csv"
                      onChange={handleExcelUpload}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm cursor-pointer hover:bg-gray-50"
                    />
                  </div>
                </div>

                {fileName && (
                  <div className="text-sm text-indigo-600 font-medium mb-4">
                    ✓ Archivo cargado: {fileName}
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Texto del calendario
                </label>
                <textarea
                  value={calendarText}
                  onChange={handleTextInputChange}
                  rows={15}
                  placeholder="Pega aquí el texto del calendario...&#10;&#10;22 23 24 25 26 27 28&#10;MANUEL MAR SANTI LOLA ELENA MANUEL SANTI&#10;ELENA JOSE REQUE MARINA KIKO MAR LAURA&#10;..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-mono text-sm"
                />
              </div>

              <button
                onClick={handleAnalyze}
                disabled={!calendarText.trim() || isLoading}
                className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              >
                <Upload className="w-5 h-5" />
                {isLoading ? 'Cargando...' : 'Analizar Calendario'}
              </button>
            </div>

            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <h3 className="font-semibold text-gray-700 mb-2">Instrucciones:</h3>
              <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
                <li>Establece la fecha del primer día del calendario</li>
                <li>Configura el mapeo de nombres abreviados si es necesario</li>
                <li>Carga un PDF, Excel o copia y pega el texto del calendario</li>
                <li>Haz clic en "Analizar Calendario"</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto bg-gray-50 min-h-screen">
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Análisis de Guardias</h1>
            {fileName && <p className="text-sm text-gray-500 mt-1">Archivo: {fileName}</p>}
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleExportCSV}
              className="bg-green-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-green-700 transition-colors flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Exportar CSV
            </button>
            <button
              onClick={handleExportPDF}
              className="bg-red-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-red-700 transition-colors flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Exportar PDF
            </button>
            <button
              onClick={handleReset}
              className="bg-gray-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-gray-700 transition-colors"
            >
              Nuevo Análisis
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-indigo-50 p-4 rounded-lg">
            <p className="text-sm text-indigo-600 font-semibold">Total de Días</p>
            <p className="text-2xl font-bold text-indigo-900">{calendarData.length}</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-sm text-green-600 font-semibold">Médicos</p>
            <p className="text-2xl font-bold text-green-900">{Object.keys(analysis).length}</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <p className="text-sm text-purple-600 font-semibold">Guardias por Día</p>
            <p className="text-2xl font-bold text-purple-900">4</p>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg">
            <p className="text-sm text-orange-600 font-semibold">Total Guardias</p>
            <p className="text-2xl font-bold text-orange-900">{calendarData.length * 4}</p>
          </div>
        </div>

        <div className="flex gap-4 flex-wrap mb-6">
          <div>
            <label className="mr-3 font-semibold text-gray-700">Vista:</label>
            <select 
              value={view} 
              onChange={(e) => setView(e.target.value)}
              className="border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-indigo-500"
            >
              <option value="general">Vista General</option>
              <option value="monthly">Desglose Mensual</option>
            </select>
          </div>
          <div>
            <label className="mr-3 font-semibold text-gray-700">Ordenar por:</label>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              className="border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-indigo-500"
            >
              <option value="total">Total de turnos</option>
              <option value="weekend">Turnos de fin de semana</option>
              <option value="weekendPercentage">% Fin de semana</option>
              <option value="friday">Viernes</option>
              <option value="saturday">Sábados</option>
              <option value="sunday">Domingos</option>
              <option value="lastPosition">Rosell</option>
              <option value="name">Nombre</option>
            </select>
          </div>
        </div>

        <div className="mb-8 bg-white p-4 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Gráfico de Turnos</h3>
            <div className="flex gap-2">
              <button
                onClick={() => setChartStartIndex(Math.max(0, chartStartIndex - 5))}
                disabled={chartStartIndex === 0}
                className="px-3 py-1 bg-gray-200 text-gray-700 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-300"
              >
                ← Anterior
              </button>
              <span className="px-3 py-1 text-sm text-gray-600">
                {chartStartIndex + 1}-{Math.min(chartStartIndex + 15, sortedWorkers.length)} de {sortedWorkers.length}
              </span>
              <button
                onClick={() => setChartStartIndex(Math.min(chartStartIndex + 5, Math.max(0, sortedWorkers.length - 15)))}
                disabled={chartStartIndex + 15 >= sortedWorkers.length}
                className="px-3 py-1 bg-gray-200 text-gray-700 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-300"
              >
                Siguiente →
              </button>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={view === 'general' ? sortedWorkers.slice(chartStartIndex, chartStartIndex + 15) : monthlyChartData.slice(chartStartIndex, chartStartIndex + 15)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={120} />
              <YAxis />
              <Tooltip />
              <Legend />
              {view === 'general' ? (
                <>
                  <Bar dataKey="total" fill="#3b82f6" name="Total" />
                  <Bar dataKey="weekend" fill="#ef4444" name="Fin de Semana" />
                  <Bar dataKey="lastPosition" fill="#f59e0b" name="Rosell" />
                </>
              ) : (
                <>
                  {monthsWithShifts.map((month, idx) => {
                    const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#06b6d4', '#84cc16', '#a855f7'];
                    return <Bar key={month.key} dataKey={month.key} fill={colors[idx % colors.length]} />;
                  })}
                </>
              )}
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-300 text-sm shadow-sm">
            <thead className="bg-gray-100">
              <tr>
                {view === 'general' ? (
                  <>
                    <th className="border px-2 py-2 text-left sticky left-0 bg-gray-100">Trabajador</th>
                    <th className="border px-2 py-2 text-center">Total</th>
                    <th className="border px-2 py-2 text-center">Vie</th>
                    <th className="border px-2 py-2 text-center">Sáb</th>
                    <th className="border px-2 py-2 text-center">Dom</th>
                    <th className="border px-2 py-2 text-center">% F.S.</th>
                    <th className="border px-2 py-2 text-center">Últ.Pos</th>
                  </>
                ) : (
                  <>
                    <th className="border px-2 py-2 text-left sticky left-0 bg-gray-100">Trabajador</th>
                    {monthsWithShifts.map(month => (
                      <th key={month.key} className="border px-2 py-2 text-center">{month.key}</th>
                    ))}
                    <th className="border px-2 py-2 text-center">Total</th>
                  </>
                )}
              </tr>
            </thead>
            <tbody>
              {view === 'general' ? (
                sortedWorkers.map((worker, idx) => (
                  <tr key={worker.name} className={idx % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                    <td className="border px-2 py-2 font-semibold sticky left-0 bg-inherit">{worker.name}</td>
                    <td className="border px-2 py-2 text-center font-bold">{worker.total}</td>
                    <td className="border px-2 py-2 text-center">{worker.friday}</td>
                    <td className="border px-2 py-2 text-center">{worker.saturday}</td>
                    <td className="border px-2 py-2 text-center">{worker.sunday}</td>
                    <td className="border px-2 py-2 text-center font-semibold">{worker.weekendPercentage}%</td>
                    <td className="border px-2 py-2 text-center">{worker.lastPosition}</td>
                  </tr>
                ))
              ) : (
                monthlyChartData.map((worker, idx) => {
                  const monthlyTotal = monthsWithShifts.reduce((sum, month) => sum + (worker[month.key] || 0), 0);
                  return (
                    <tr key={worker.name} className={idx % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                      <td className="border px-2 py-2 font-semibold sticky left-0 bg-inherit">{worker.name}</td>
                      {monthsWithShifts.map(month => (
                        <td key={month.key} className="border px-2 py-2 text-center">{worker[month.key] || 0}</td>
                      ))}
                      <td className="border px-2 py-2 text-center font-bold">{monthlyTotal}</td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default CalendarAnalyzer;
