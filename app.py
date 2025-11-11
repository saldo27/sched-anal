"""
Flask API for calendar file processing and shift schedule analysis.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
from pathlib import Path
from file_processor import CalendarFileProcessor
import traceback

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
def export_results():
    """
    Export analysis results.
    
    Expected JSON:
    {
        "workers": [...],
        "format": "csv" or "json"
    }
    """
    try:
        data = request.json
        
        if not data or 'workers' not in data:
            return jsonify({'error': 'Missing workers data'}), 400
        
        workers = data.get('workers', [])
        export_format = data.get('format', 'csv').lower()
        
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
                'workers': workers
            }), 200
        
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
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
