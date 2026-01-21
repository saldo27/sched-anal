"""
Module for processing calendar files (PDF, Excel, CSV) and extracting schedule data.
"""

import pandas as pd
from pathlib import Path
import pdfplumber
from typing import List, Dict, Tuple
import re


class CalendarFileProcessor:
    """Process calendar files in different formats (PDF, Excel, CSV)."""
    
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text from the PDF
        """
        text = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return '\n'.join(text)
        except Exception as e:
            raise ValueError(f"Error extracting PDF: {str(e)}")
    
    @staticmethod
    def extract_from_excel(excel_path: str) -> str:
        """
        Extract calendar data from an Excel file.
        
        Args:
            excel_path: Path to the Excel file
            
        Returns:
            Formatted calendar text
        """
        try:
            # Try to read with openpyxl first (handles .xlsx)
            df = pd.read_excel(excel_path, sheet_name=0, header=None)
            
            # Convert to text format similar to the calendar input
            lines = []
            for _, row in df.iterrows():
                # Remove NaN values and convert to string
                cleaned_row = [str(val).strip() for val in row if pd.notna(val)]
                if cleaned_row:
                    lines.append(' '.join(cleaned_row))
            
            return '\n'.join(lines)
        except Exception as e:
            raise ValueError(f"Error extracting Excel file: {str(e)}")
    
    @staticmethod
    def extract_from_csv(csv_path: str) -> str:
        """
        Extract calendar data from a CSV file.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            Formatted calendar text
        """
        try:
            df = pd.read_csv(csv_path, header=None)
            
            lines = []
            for _, row in df.iterrows():
                cleaned_row = [str(val).strip() for val in row if pd.notna(val)]
                if cleaned_row:
                    lines.append(' '.join(cleaned_row))
            
            return '\n'.join(lines)
        except Exception as e:
            raise ValueError(f"Error extracting CSV file: {str(e)}")
    
    @staticmethod
    def process_file(file_path: str) -> str:
        """
        Process a calendar file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted calendar text
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = path.suffix.lower()
        
        if suffix == '.pdf':
            return CalendarFileProcessor.extract_text_from_pdf(file_path)
        elif suffix in ['.xlsx', '.xls']:
            return CalendarFileProcessor.extract_from_excel(file_path)
        elif suffix == '.csv':
            return CalendarFileProcessor.extract_from_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    @staticmethod
    def detect_calendar_structure(text: str) -> Dict[str, any]:
        """
        Detect the structure of the calendar text.
        
        Args:
            text: The calendar text
            
        Returns:
            Dictionary with detected structure information
        """
        lines = text.strip().split('\n')
        
        # Try to find day numbers (first line typically contains day numbers)
        days_line = lines[0] if lines else ""
        day_numbers = re.findall(r'\b\d{1,2}\b', days_line)
        
        structure = {
            'days_count': len(day_numbers),
            'lines_per_week': len(lines[:5]),  # Assuming 5 lines per week (days + 4 rows)
            'detected_format': 'week_based' if len(day_numbers) <= 7 else 'unknown'
        }
        
        return structure


def batch_process_files(directory: str, pattern: str = "*") -> Dict[str, str]:
    """
    Process multiple calendar files in a directory.
    
    Args:
        directory: Path to the directory containing files
        pattern: File pattern to match (e.g., "*.pdf", "*.xlsx")
        
    Returns:
        Dictionary with filename as key and extracted text as value
    """
    results = {}
    path = Path(directory)
    
    for file_path in path.glob(pattern):
        try:
            extracted_text = CalendarFileProcessor.process_file(str(file_path))
            results[file_path.name] = extracted_text
        except Exception as e:
            results[file_path.name] = f"Error: {str(e)}"
    
    return results


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python file_processor.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    processor = CalendarFileProcessor()
    
    try:
        extracted_text = processor.process_file(file_path)
        print("Extracted text:")
        print(extracted_text)
        
        # Detect structure
        structure = processor.detect_calendar_structure(extracted_text)
        print("\nDetected structure:")
        print(structure)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
