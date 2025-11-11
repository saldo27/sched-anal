"""
Flask API for calendar file processing and shift schedule analysis.
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
from pathlib import Path
from file_processor import CalendarFileProcessor
import traceback
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
ALLOWED_EXTENSIONS = {'pdf', 'xlsx', 'xls', 'csv'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
TEMP_DIR = tempfile.gettempdir()


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'version': '1.0.0'})


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Upload and process a calendar file.
    
    Expected: multipart/form-data with 'file' field
    Returns: JSON with extracted calendar text
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'error': f'File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024} MB'
            }), 400
        
        # Save temporary file
        filename = secure_filename(file.filename)
        temp_path = os.path.join(TEMP_DIR, filename)
        file.save(temp_path)
        
        try:
            # Process file
            processor = CalendarFileProcessor()
            extracted_text = processor.process_file(temp_path)
            
            # Detect structure
            structure = processor.detect_calendar_structure(extracted_text)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'text': extracted_text,
                'structure': structure,
                'lines': len(extracted_text.split('\n'))
            }), 200
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        return jsonify({
            'error': f'Processing error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_calendar():
    """
    Analyze calendar text.
    
    Expected JSON:
    {
        "calendarText": "...",
        "startDate": "2025-12-22",
        "nameMapping": "..."
    }
    """
    try:
        data = request.json
        
        if not data or 'calendarText' not in data:
            return jsonify({'error': 'Missing calendarText'}), 400
        
        calendar_text = data.get('calendarText', '')
        start_date = data.get('startDate', '2025-12-22')
        name_mapping = data.get('nameMapping', '')
        
        if not calendar_text.strip():
            return jsonify({'error': 'Calendar text is empty'}), 400
        
        # Parse calendar (this would be done by the React component)
        # Here we just validate the structure
        processor = CalendarFileProcessor()
        structure = processor.detect_calendar_structure(calendar_text)
        
        return jsonify({
            'success': True,
            'structure': structure,
            'textLength': len(calendar_text),
            'lines': len(calendar_text.split('\n'))
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Analysis error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/export', methods=['POST'])
def export_data():
    """
    Export shift analysis data to CSV, JSON or PDF.
    
    Expected JSON:
    {
        "workers": [...],
        "monthlyData": [...],
        "format": "csv", "json" or "pdf",
        "analysisPeriod": "Dec 2024 - Mar 2025"
    }
    """
    try:
        data = request.json
        
        if not data or 'workers' not in data:
            return jsonify({'error': 'Missing workers data'}), 400
        
        workers = data.get('workers', [])
        monthly_data = data.get('monthlyData', [])
        export_format = data.get('format', 'csv').lower()
        period = data.get('analysisPeriod', 'Análisis de Turnos')
        
        print(f"[DEBUG] Export: format={export_format}, workers={len(workers)}, monthly_data={len(monthly_data)}")
        
        if export_format == 'csv':
            # Generate CSV
            csv_content = 'Trabajador,Total,Viernes,Sábado,Domingo,% Fin de Semana,Última Posición\n'
            for worker in workers:
                csv_content += f'"{worker["name"]}",{worker["total"]},{worker["friday"]},{worker["saturday"]},{worker["sunday"]},{worker["weekendPercentage"]},{worker["lastPosition"]}\n'
            
            return jsonify({
                'success': True,
                'format': 'csv',
                'content': csv_content
            }), 200
        
        elif export_format == 'json':
            return jsonify({
                'success': True,
                'format': 'json',
                'workers': workers,
                'monthlyData': monthly_data
            }), 200
        
        elif export_format == 'pdf':
            # Generate PDF with global and monthly data - A4 Landscape
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch, 
                                   leftMargin=0.5*inch, rightMargin=0.5*inch)
            doc.pagesize = (A4[1], A4[0])  # Landscape orientation
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=14,
                textColor=colors.HexColor('#1f2937'),
                spaceAfter=6,
                alignment=1  # Center
            )
            story.append(Paragraph(f"Análisis de Turnos - {period}", title_style))
            story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # GLOBAL DATA SECTION
            story.append(Paragraph("1. Resumen Global", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            global_table_data = [
                ['Trabajador', 'Total', 'Viernes', 'Sábado', 'Domingo', '% Fin de Semana', 'Últ. Pos.']
            ]
            for worker in workers:
                global_table_data.append([
                    worker['name'],
                    str(worker.get('total', 0)),
                    str(worker.get('friday', 0)),
                    str(worker.get('saturday', 0)),
                    str(worker.get('sunday', 0)),
                    f"{worker.get('weekendPercentage', 0)}%",
                    str(worker.get('lastPosition', 0))
                ])
            
            global_table = Table(global_table_data, colWidths=[1.3*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.9*inch, 0.6*inch])
            global_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
            ]))
            story.append(global_table)
            story.append(Spacer(1, 0.2*inch))
            
            # MONTHLY DATA SECTION (if available)
            if monthly_data and len(monthly_data) > 0:
                story.append(PageBreak())
                story.append(Paragraph("2. Desglose Mensual", styles['Heading2']))
                story.append(Spacer(1, 0.1*inch))
                
                # Get only months with data (non-zero totals)
                all_months = set()
                month_totals = {}
                
                for worker_data in monthly_data:
                    for key in worker_data.keys():
                        if key != 'name':
                            value = worker_data.get(key, 0)
                            if value > 0:
                                all_months.add(key)
                                if key not in month_totals:
                                    month_totals[key] = 0
                                month_totals[key] += value
                
                # Order months: Dic, Ene, Feb, Mar, Abr, May, Jun, Jul, Ago, Sep, Oct, Nov
                month_order = ['Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov']
                all_months = sorted(list(all_months), key=lambda x: month_order.index(x) if x in month_order else 999)
                
                if all_months:  # Only show table if there are months with data
                    monthly_table_data = [['Trabajador'] + all_months + ['Total']]
                    
                    for worker_data in monthly_data:
                        row = [worker_data['name']]
                        monthly_total = 0
                        for month in all_months:
                            value = worker_data.get(month, 0)
                            row.append(str(value))
                            monthly_total += value
                        row.append(str(monthly_total))
                        monthly_table_data.append(row)
                    
                    # Adjust column widths for landscape
                    col_width = 5.5 / (len(all_months) + 2)  # A4 landscape is ~7.5 inches, minus margins
                    col_widths = [1.2*inch] + [col_width*inch] * len(all_months) + [0.6*inch]
                    
                    monthly_table = Table(monthly_table_data, colWidths=col_widths)
                    monthly_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 7),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
                    ]))
                    story.append(monthly_table)
            
            # Build PDF
            doc.build(story)
            pdf_buffer.seek(0)
            
            # Return PDF as response with proper headers
            pdf_data = pdf_buffer.getvalue()
            
            response = app.response_class(
                response=pdf_data,
                status=200,
                mimetype='application/pdf',
                headers={
                    'Content-Disposition': f'attachment; filename=analisis_turnos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
                }
            )
            return response
        
        else:
            return jsonify({'error': f'Unsupported format: {export_format}'}), 400
    
    except Exception as e:
        return jsonify({
            'error': f'Export error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Windows compatibility: use 127.0.0.1 instead of 0.0.0.0
    # 0.0.0.0 sometimes has connection issues on Windows
    # use_reloader=False avoids watchdog issues
    import sys
    is_windows = sys.platform.startswith('win')
    host = '127.0.0.1' if is_windows else '0.0.0.0'
    
    print(f"\n{'='*70}")
    print(f"🚀 Starting Calendar Analyzer Backend")
    print(f"{'='*70}")
    print(f"Host: {host}")
    print(f"Port: 5000")
    print(f"Debug: True")
    print(f"Reloader: Disabled (watchdog compatible)")
    print(f"Platform: {'Windows' if is_windows else 'Unix-like'}")
    print(f"{'='*70}\n")
    
    app.run(debug=True, host=host, port=5000, use_reloader=False)
