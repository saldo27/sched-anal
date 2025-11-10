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
            
            # Try to identify the calendar structure
            # Look for dates in the first column or first row
            
            # Strategy 1: Dates in rows, workers in columns
            # Try to find date column
            for col_idx in range(min(3, len(df.columns))):
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
            for row_idx in range(min(3, len(df))):
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
    def parse(file_path: Path) -> ShiftData:
        """
        Parse a PDF file containing shift schedules.
        
        Uses pdfplumber to extract tables from PDF.
        """
        shift_data = ShiftData()
        
        try:
            import pdfplumber
            
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Extract tables
                    tables = page.extract_tables()
                    
                    for table in tables:
                        if not table:
                            continue
                        
                        # Convert table to DataFrame for easier processing
                        df = pd.DataFrame(table[1:], columns=table[0] if table else None)
                        
                        # Try to identify date columns and worker names
                        for col_idx, col_name in enumerate(df.columns):
                            try:
                                # Try to parse column as dates
                                dates = pd.to_datetime(df.iloc[:, col_idx], errors='coerce')
                                if dates.notna().sum() > 5:
                                    # Found date column
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
            print("Error: pdfplumber is required for PDF parsing. Install with: pip install pdfplumber", file=sys.stderr)
        except Exception as e:
            print(f"Error parsing PDF file: {e}", file=sys.stderr)
        
        return shift_data


def parse_file(file_path: Path) -> ShiftData:
    """Parse a shift schedule file (PDF or Excel)."""
    suffix = file_path.suffix.lower()
    
    if suffix in ['.xlsx', '.xls']:
        return ExcelParser.parse(file_path)
    elif suffix == '.pdf':
        return PDFParser.parse(file_path)
    else:
        print(f"Error: Unsupported file format: {suffix}", file=sys.stderr)
        print("Supported formats: .xlsx, .xls, .pdf", file=sys.stderr)
        return ShiftData()


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
    
    # Check if input file exists
    if not args.input_file.exists():
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        return 1
    
    print(f"Parsing {args.input_file}...")
    
    # Parse the file
    shift_data = parse_file(args.input_file)
    
    if not shift_data.shifts:
        print("Warning: No shift data found in the file.", file=sys.stderr)
        print("Please ensure the file contains a calendar with worker names and dates.", file=sys.stderr)
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
