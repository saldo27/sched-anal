#!/usr/bin/env python3
"""
Shift Schedule Analyzer
Analyzes PDF or Excel files containing shift schedules and generates statistics per worker.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from tabulate import tabulate


class ShiftData:
    """Represents shift data for analysis."""
    
    def __init__(self):
        self.shifts: List[Dict] = []
    
    def add_shift(self, worker: str, date: datetime, position: Optional[int] = None):
        """Add a shift entry."""
        self.shifts.append({
            'worker': worker,
            'date': date,
            'position': position
        })
    
    def get_dataframe(self) -> pd.DataFrame:
        """Convert shift data to pandas DataFrame."""
        return pd.DataFrame(self.shifts)


class ShiftAnalyzer:
    """Analyzes shift data and generates statistics."""
    
    def __init__(self, shift_data: ShiftData):
        self.df = shift_data.get_dataframe()
        if not self.df.empty:
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.df['weekday'] = self.df['date'].dt.dayofweek  # 0=Monday, 6=Sunday
            self.df['month'] = self.df['date'].dt.to_period('M')
    
    def analyze(self) -> pd.DataFrame:
        """
        Analyze shifts and return statistics for each worker.
        
        Returns:
            DataFrame with columns:
            - Worker
            - Total Shifts
            - Shifts per Month
            - Friday Shifts
            - Saturday Shifts
            - Sunday Shifts
            - Weekend Shift %
            - Last Position Shifts
        """
        if self.df.empty:
            return pd.DataFrame()
        
        results = []
        
        for worker in sorted(self.df['worker'].unique()):
            worker_df = self.df[self.df['worker'] == worker]
            
            # Total shifts
            total_shifts = len(worker_df)
            
            # Shifts per month (as a dict/string for display)
            shifts_by_month = worker_df.groupby('month').size().to_dict()
            shifts_per_month_str = ', '.join([f"{k}: {v}" for k, v in sorted(shifts_by_month.items())])
            
            # Day-specific counts
            friday_shifts = len(worker_df[worker_df['weekday'] == 4])  # Friday
            saturday_shifts = len(worker_df[worker_df['weekday'] == 5])  # Saturday
            sunday_shifts = len(worker_df[worker_df['weekday'] == 6])  # Sunday
            
            # Weekend percentage
            weekend_shifts = friday_shifts + saturday_shifts + sunday_shifts
            weekend_percentage = (weekend_shifts / total_shifts * 100) if total_shifts > 0 else 0
            
            # Last position shifts (if position data available)
            last_position_shifts = 0
            if 'position' in worker_df.columns and worker_df['position'].notna().any():
                # Group by date and find the maximum position for each date
                date_groups = self.df.groupby('date')['position'].max()
                # Count how many times this worker had the max position
                for date in worker_df['date'].unique():
                    if date in date_groups.index:
                        max_pos = date_groups[date]
                        worker_date_positions = worker_df[worker_df['date'] == date]['position'].values
                        if len(worker_date_positions) > 0 and worker_date_positions[0] == max_pos:
                            last_position_shifts += 1
            
            results.append({
                'Worker': worker,
                'Total Shifts': total_shifts,
                'Shifts per Month': shifts_per_month_str,
                'Friday Shifts': friday_shifts,
                'Saturday Shifts': saturday_shifts,
                'Sunday Shifts': sunday_shifts,
                'Weekend Shift %': f"{weekend_percentage:.1f}%",
                'Last Position Shifts': last_position_shifts
            })
        
        return pd.DataFrame(results)


class ExcelParser:
    """Parses Excel files containing shift schedules."""
    
    @staticmethod
    def debug_structure(file_path: Path):
        """Debug: Print the structure of the Excel file."""
        try:
            df = pd.read_excel(file_path, header=None)
            print("\n[DEBUG] Estructura del archivo Excel:")
            print(f"Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
            print("\nPrimeras 10 filas y 5 columnas:")
            print(df.iloc[:10, :5].to_string())
            print("\n")
        except Exception as e:
            print(f"[DEBUG] Error al analizar: {e}", file=sys.stderr)
    
    @staticmethod
    def parse(file_path: Path) -> ShiftData:
        """
        Parse an Excel file containing shift schedules.
        
        Expected format:
        - First column: dates (can be in rows or columns)
        - Worker names in cells where they have shifts
        - Calendar format: Monday to Sunday
        """
        shift_data = ShiftData()
        
        try:
            # Try to read the Excel file
            df = pd.read_excel(file_path, header=None)
            
            if df.empty:
                return shift_data
            
            # Try to identify the calendar structure
            # Look for dates in the first column or first row
            
            # Strategy 1: Dates in rows, workers in columns
            # Try to find date column
            for col_idx in range(min(5, len(df.columns))):
                try:
                    dates = pd.to_datetime(df.iloc[:, col_idx], errors='coerce')
                    if dates.notna().sum() > 5:  # At least 5 valid dates
                        # Found date column
                        for row_idx in range(len(df)):
                            date = dates.iloc[row_idx]
                            if pd.notna(date):
                                # Check other columns for worker names
                                for other_col in range(len(df.columns)):
                                    if other_col != col_idx:
                                        cell_value = df.iloc[row_idx, other_col]
                                        if pd.notna(cell_value) and isinstance(cell_value, str) and cell_value.strip():
                                            worker = cell_value.strip()
                                            shift_data.add_shift(worker, date, other_col - col_idx)
                        return shift_data
                except:
                    continue
            
            # Strategy 2: Dates in columns, workers in rows
            for row_idx in range(min(5, len(df))):
                try:
                    # Try to parse first row as dates
                    dates = pd.to_datetime(df.iloc[row_idx, :], errors='coerce')
                    if dates.notna().sum() > 5:  # At least 5 valid dates
                        # Found date row
                        for col_idx in range(len(df.columns)):
                            date = dates.iloc[col_idx]
                            if pd.notna(date):
                                # Check other rows for worker names
                                for other_row in range(len(df)):
                                    if other_row != row_idx:
                                        cell_value = df.iloc[other_row, col_idx]
                                        if pd.notna(cell_value) and isinstance(cell_value, str) and cell_value.strip():
                                            worker = cell_value.strip()
                                            shift_data.add_shift(worker, date, other_row - row_idx)
                        return shift_data
                except:
                    continue
            
        except Exception as e:
            print(f"Error parsing Excel file: {e}", file=sys.stderr)
        
        return shift_data


class PDFParser:
    """Parses PDF files containing shift schedules."""
    
    @staticmethod
    def debug_structure(file_path: Path):
        """Debug: Print the structure of the PDF file."""
        try:
            import pdfplumber
            
            with pdfplumber.open(file_path) as pdf:
                print(f"\n[DEBUG] PDF con {len(pdf.pages)} página(s)")
                
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    print(f"\nPágina {page_num + 1}: {len(tables)} tabla(s)")
                    
                    for table_num, table in enumerate(tables):
                        if table:
                            print(f"  Tabla {table_num + 1}: {len(table)} filas × {len(table[0])} columnas")
                            print("  Primeras 10 filas:")
                            for i, row in enumerate(table[:10]):
                                print(f"    {row}")
                            print()
        except ImportError:
            print("[DEBUG] pdfplumber no está instalado", file=sys.stderr)
        except Exception as e:
            print(f"[DEBUG] Error: {e}", file=sys.stderr)
    
    @staticmethod
    def parse_calendar_table(table: list, year: int, month: int) -> list:
        """
        Parse a calendar table with days and worker names.
        
        Format can be:
        - Headers: day-of-week names (Mon, Tue, etc)
        - Data rows: mix of day numbers and worker names (often combined like "2\nBob")
        - Each column represents a day of the week
        
        Returns:
            List of shift entries: [(worker, date), ...]
        """
        shifts = []
        
        if not table or len(table) < 2:
            return shifts
        
        # Skip the first row if it contains day-of-week names
        start_row = 0
        first_row = table[0]
        
        day_names = ['lun', 'mar', 'mié', 'jue', 'vie', 'sab', 'dom', 
                     'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
                     'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        
        is_day_header = all(
            (cell and str(cell).strip().lower() in day_names) or not cell
            for cell in first_row
        )
        
        if is_day_header:
            start_row = 1
        
        # Extract all day numbers and collect data by column
        # Each column will have a day number (from any row)
        column_days = [None] * len(table[0]) if table else []
        
        # Scan all rows to find day numbers
        for row_idx in range(start_row, len(table)):
            row = table[row_idx]
            for col_idx, cell in enumerate(row):
                if not column_days[col_idx] and cell:
                    cell_str = str(cell).strip()
                    lines = cell_str.split('\n')
                    for line in lines:
                        line = line.strip()
                        try:
                            day_num = int(line)
                            if 1 <= day_num <= 31:
                                column_days[col_idx] = day_num
                                break
                        except ValueError:
                            pass
        
        # If we couldn't find any day numbers, return empty
        if all(d is None for d in column_days):
            return shifts
        
        # Now process all data rows to extract worker names
        from datetime import datetime
        from calendar import monthrange
        
        max_days_in_month = monthrange(year, month)[1]
        
        for row_idx in range(start_row, len(table)):
            row = table[row_idx]
            
            for col_idx, cell in enumerate(row):
                if not cell or col_idx >= len(column_days) or column_days[col_idx] is None:
                    continue
                
                cell_str = str(cell).strip()
                if not cell_str:
                    continue
                
                # Split by newlines to handle "2\nBob" format
                lines = cell_str.split('\n')
                
                for line in lines:
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    # Skip day numbers and day-of-week names
                    try:
                        int(line)
                        continue  # Skip if it's a number
                    except ValueError:
                        pass
                    
                    if line.lower() in day_names + ['día', 'day', '']:
                        continue
                    
                    # This is a worker name
                    day_num = column_days[col_idx]
                    
                    if day_num <= max_days_in_month:
                        try:
                            date = datetime(year, month, day_num)
                            shifts.append((line, date))
                        except ValueError:
                            continue
        
        return shifts
    
    @staticmethod
    def parse(file_path: Path, year: Optional[int] = None, months: Optional[List[int]] = None) -> ShiftData:
        """
        Parse a PDF file containing shift schedules.
        
        Uses pdfplumber to extract tables from PDF.
        """
        shift_data = ShiftData()
        
        try:
            import pdfplumber
            from datetime import datetime
            
            if year is None:
                year = datetime.now().year
            
            if months is None:
                months = [datetime.now().month]
            
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Extract tables
                    tables = page.extract_tables()
                    
                    for table in tables:
                        if not table or len(table) < 1:
                            continue
                        
                        # Try to identify if this is a calendar format
                        # Strategy 1: Look for day numbers in the first few rows
                        day_count = 0
                        has_day_header = False
                        
                        # Check if first row is a day-of-week header (Mon, Tue, etc)
                        first_row = table[0]
                        day_names_list = ['lun', 'mar', 'mié', 'jue', 'vie', 'sab', 'dom', 
                                        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
                                        'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                        
                        has_day_header = all(
                            (cell and str(cell).strip().lower() in day_names_list) or not cell
                            for cell in first_row
                        )
                        
                        # Search for day numbers in all rows
                        for row_idx in range(len(table)):
                            row = table[row_idx]
                            for cell in row:
                                if cell:
                                    cell_str = str(cell).strip()
                                    lines = cell_str.split('\n')
                                    for line in lines:
                                        try:
                                            day_num = int(line.strip())
                                            if 1 <= day_num <= 31:
                                                day_count += 1
                                        except ValueError:
                                            pass
                        
                        # If we found a day header OR we found several day numbers, treat as calendar
                        if has_day_header or day_count >= 5:
                            # Process each month in the list
                            for month in months:
                                shifts = PDFParser.parse_calendar_table(table, year, month)
                                for worker, date in shifts:
                                    shift_data.add_shift(worker, date)
                        else:
                            # Try old strategy for non-calendar tables
                            df = pd.DataFrame(table[1:], columns=table[0] if table else None)
                            
                            if df.empty:
                                continue
                            
                            # Try to identify date columns and worker names
                            for col_idx in range(len(df.columns)):
                                try:
                                    dates = pd.to_datetime(df.iloc[:, col_idx], errors='coerce')
                                    if dates.notna().sum() > 5:
                                        for row_idx in range(len(df)):
                                            date = dates.iloc[row_idx]
                                            if pd.notna(date):
                                                for other_col in range(len(df.columns)):
                                                    if other_col != col_idx:
                                                        cell_value = df.iloc[row_idx, other_col]
                                                        if pd.notna(cell_value) and isinstance(cell_value, str) and cell_value.strip():
                                                            worker = cell_value.strip()
                                                            shift_data.add_shift(worker, date, other_col - col_idx)
                                except:
                                    continue
        
        except ImportError:
            print("Error: pdfplumber es requerido para analizar PDFs.", file=sys.stderr)
            print("Instálalo con: pip install pdfplumber", file=sys.stderr)
        except Exception as e:
            print(f"Error parsing PDF file: {e}", file=sys.stderr)
        
        return shift_data


def parse_file(file_path: Path, year: Optional[int] = None, months: Optional[List[int]] = None) -> ShiftData:
    """Parse a shift schedule file (PDF or Excel)."""
    suffix = file_path.suffix.lower()
    
    if suffix in ['.xlsx', '.xls']:
        return ExcelParser.parse(file_path)
    elif suffix == '.pdf':
        return PDFParser.parse(file_path, year=year, months=months)
    else:
        print(f"Error: Unsupported file format: {suffix}", file=sys.stderr)
        print("Supported formats: .xlsx, .xls, .pdf", file=sys.stderr)
        return ShiftData()


def ask_for_months():
    """Ask the user which months are included in the calendar."""
    months = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    
    print("\n¿Qué meses incluye el calendario?")
    print("(Ingresa los números separados por comas, ej: 1,2,3 para Enero, Febrero, Marzo)\n")
    
    for i, month in enumerate(months, 1):
        print(f"  {i:2d}. {month}")
    
    print()
    
    while True:
        user_input = input("Meses a analizar: ").strip()
        
        if not user_input:
            print("Error: Debes seleccionar al menos un mes.")
            continue
        
        try:
            month_numbers = [int(x.strip()) for x in user_input.split(',')]
            
            # Validate month numbers
            if not all(1 <= m <= 12 for m in month_numbers):
                print("Error: Los números de mes deben estar entre 1 y 12.")
                continue
            
            selected_months = [months[m - 1] for m in month_numbers]
            print(f"\nMeses seleccionados: {', '.join(selected_months)}\n")
            return month_numbers
        
        except ValueError:
            print("Error: Ingresa números separados por comas (ej: 1,2,3).")


def ask_for_year():
    """Ask the user for the year of the calendar."""
    from datetime import datetime
    current_year = datetime.now().year
    
    print(f"\n¿En qué año está el calendario? [por defecto {current_year}]")
    
    while True:
        user_input = input(f"Año [{current_year}]: ").strip() or str(current_year)
        
        try:
            year = int(user_input)
            if 1900 <= year <= 2100:
                print(f"Año seleccionado: {year}\n")
                return year
            else:
                print("Error: Ingresa un año entre 1900 y 2100.")
        except ValueError:
            print("Error: Ingresa un año válido (número).")


def ask_for_output_format():
    """Ask the user for output format preference."""
    formats = ['table', 'csv', 'json']
    
    print("\n¿En qué formato deseas los resultados?")
    for i, fmt in enumerate(formats, 1):
        print(f"  {i}. {fmt.upper()}")
    
    print()
    
    while True:
        choice = input("Selecciona formato (1-3) [1]: ").strip() or "1"
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(formats):
                selected_format = formats[choice_num - 1]
                print(f"Formato seleccionado: {selected_format.upper()}\n")
                return selected_format
            else:
                print(f"Error: Ingresa un número entre 1 y {len(formats)}.")
        except ValueError:
            print("Error: Ingresa un número válido.")


def ask_for_output_file():
    """Ask the user if they want to save results to a file."""
    print("\n¿Deseas guardar los resultados en un archivo?")
    choice = input("Opción (s/n) [n]: ").strip().lower() or "n"
    
    if choice == 's':
        while True:
            file_path = input("Ruta del archivo de salida (ej: resultados.csv): ").strip()
            
            if not file_path:
                print("Error: Debes ingresar una ruta de archivo.")
                continue
            
            return Path(file_path)
    
    return None


def main():
    """Main entry point for the shift analyzer."""
    parser = argparse.ArgumentParser(
        description='Analyze shift schedules from PDF or Excel files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s schedule.xlsx
  %(prog)s schedule.pdf
  %(prog)s schedule.xlsx -o results.csv
        """
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        type=Path,
        help='Input file (PDF or Excel) containing shift schedule'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file for results (CSV format). If not specified, prints to console.'
    )
    
    parser.add_argument(
        '--format',
        choices=['table', 'csv', 'json'],
        default='table',
        help='Output format (default: table)'
    )
    
    args = parser.parse_args()
    
    # Interactive mode if no arguments provided
    if args.input_file is None:
        print("\n" + "=" * 60)
        print("ANALIZADOR DE HORARIOS DE TURNOS")
        print("=" * 60)
        print("\nBienvenido al analizador de calendarios de turnos")
        print("Soporta archivos en formato: PDF, Excel (.xlsx, .xls)\n")
        
        # Ask for input file
        while True:
            file_input = input("Ruta del archivo: ").strip()
            
            if not file_input:
                print("Error: Debes ingresar una ruta de archivo.")
                continue
            
            args.input_file = Path(file_input)
            
            if args.input_file.exists():
                break
            else:
                print(f"Error: El archivo '{file_input}' no existe.")
                print("Intenta de nuevo o presiona Ctrl+C para salir.\n")
        
        # Ask for year and months
        year = ask_for_year()
        months = ask_for_months()
        
        # Ask for output format
        if args.format == 'table':  # Only ask if using default
            args.format = ask_for_output_format()
        
        # Ask for output file
        if args.output is None:
            args.output = ask_for_output_file()
    else:
        # Non-interactive mode: use defaults
        year = None
        months = None
    
    # Check if input file exists
    if not args.input_file.exists():
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        return 1
    
    print(f"Parsing {args.input_file}...")
    
    # Parse the file
    shift_data = parse_file(args.input_file, year=year, months=months)
    
    if not shift_data.shifts:
        print("\n" + "=" * 60)
        print("⚠️  ADVERTENCIA: No se encontraron turnos en el archivo", file=sys.stderr)
        print("=" * 60)
        print("\nPosibles causas:")
        print("  1. El archivo no contiene un calendario de turnos")
        print("  2. El formato del calendario no es reconocido")
        print("  3. Las fechas o nombres de trabajadores tienen formato inusual")
        print("\nRecomendaciones:")
        print("  • Asegúrate de que el archivo tenga fechas en las filas o columnas")
        print("  • Los nombres de trabajadores deben estar en las celdas con turnos")
        print("  • Usa la opción de debug para ver la estructura del archivo")
        print("=" * 60)
        return 1
    
    print(f"Found {len(shift_data.shifts)} shift entries")
    
    # Analyze the data
    print("Analyzing shifts...")
    analyzer = ShiftAnalyzer(shift_data)
    results = analyzer.analyze()
    
    if results.empty:
        print("No results to display.", file=sys.stderr)
        return 1
    
    # Output results
    if args.output:
        # Save to file
        if args.format == 'json':
            results.to_json(args.output, orient='records', indent=2)
        else:  # CSV format
            results.to_csv(args.output, index=False)
        print(f"Results saved to {args.output}")
    else:
        # Print to console
        if args.format == 'json':
            print(results.to_json(orient='records', indent=2))
        elif args.format == 'csv':
            print(results.to_csv(index=False))
        else:  # table format
            print("\n" + "=" * 80)
            print("SHIFT ANALYSIS RESULTS")
            print("=" * 80)
            print(tabulate(results, headers='keys', tablefmt='grid', showindex=False))
            print("=" * 80)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
