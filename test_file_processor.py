"""
Unit tests for file processor module.
"""

import unittest
import tempfile
import os
from pathlib import Path
from file_processor import CalendarFileProcessor
import pandas as pd


class TestCalendarFileProcessor(unittest.TestCase):
    """Test cases for CalendarFileProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = CalendarFileProcessor()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove temp directory and files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
    
    def test_detect_calendar_structure(self):
        """Test calendar structure detection."""
        calendar_text = """22 23 24 25 26 27 28
MANUEL MAR SANTI LOLA ELENA MANUEL SANTI
ELENA JOSE REQUE MARINA KIKO MAR LAURA
PATRICIA LAURA MANUEL JOSE SANTI ELENA REQUE
MARINA SANTI ELENA MAR MANUEL PATRICIA JOSE

29 30 31 1 2 3 4
REQUE ELENA MAR SANTI PATRICIA JOSE MANUEL"""
        
        structure = self.processor.detect_calendar_structure(calendar_text)
        
        self.assertIn('days_count', structure)
        self.assertIn('lines_per_week', structure)
        self.assertIn('detected_format', structure)
        self.assertEqual(structure['days_count'], 7)
    
    def test_process_csv_file(self):
        """Test CSV file processing."""
        # Create a test CSV file
        csv_content = """22,23,24,25,26,27,28
MANUEL,MAR,SANTI,LOLA,ELENA,MANUEL,SANTI
ELENA,JOSE,REQUE,MARINA,KIKO,MAR,LAURA
PATRICIA,LAURA,MANUEL,JOSE,SANTI,ELENA,REQUE
MARINA,SANTI,ELENA,MAR,MANUEL,PATRICIA,JOSE"""
        
        csv_path = os.path.join(self.temp_dir, 'test.csv')
        with open(csv_path, 'w') as f:
            f.write(csv_content)
        
        result = self.processor.process_file(csv_path)
        
        self.assertIsNotNone(result)
        self.assertIn('MANUEL', result)
        self.assertIn('ELENA', result)
    
    def test_process_excel_file(self):
        """Test Excel file processing."""
        # Create a test Excel file
        excel_path = os.path.join(self.temp_dir, 'test.xlsx')
        
        data = {
            'A': [22, 'MANUEL', 'ELENA', 'PATRICIA', 'MARINA'],
            'B': [23, 'MAR', 'JOSE', 'LAURA', 'SANTI'],
            'C': [24, 'SANTI', 'REQUE', 'MANUEL', 'ELENA'],
            'D': [25, 'LOLA', 'MARINA', 'JOSE', 'MAR'],
            'E': [26, 'ELENA', 'KIKO', 'SANTI', 'MANUEL'],
            'F': [27, 'MANUEL', 'MAR', 'ELENA', 'PATRICIA'],
            'G': [28, 'SANTI', 'LAURA', 'REQUE', 'JOSE']
        }
        
        df = pd.DataFrame(data)
        df.to_excel(excel_path, index=False, header=False)
        
        result = self.processor.process_file(excel_path)
        
        self.assertIsNotNone(result)
        self.assertIn('MANUEL', result)
    
    def test_file_not_found(self):
        """Test FileNotFoundError for non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.processor.process_file('/nonexistent/file.pdf')
    
    def test_unsupported_format(self):
        """Test ValueError for unsupported file format."""
        # Create a file with unsupported extension
        unsupported_path = os.path.join(self.temp_dir, 'test.txt')
        with open(unsupported_path, 'w') as f:
            f.write('test content')
        
        with self.assertRaises(ValueError):
            self.processor.process_file(unsupported_path)
    
    def test_calendar_text_with_special_characters(self):
        """Test calendar text with special characters."""
        calendar_text = """22 23 24 25 26 27 28
JOSÉ MARÍA SÁNT LOLA ELENA MANUÉL SANTI
ELENA JOSÉ REQUE MARINA KIKO MAR LAURA"""
        
        structure = self.processor.detect_calendar_structure(calendar_text)
        
        self.assertEqual(structure['days_count'], 7)
    
    def test_empty_calendar_text(self):
        """Test with empty calendar text."""
        calendar_text = ""
        
        structure = self.processor.detect_calendar_structure(calendar_text)
        
        self.assertEqual(structure['days_count'], 0)


class TestCalendarParsingEdgeCases(unittest.TestCase):
    """Test edge cases in calendar parsing."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = CalendarFileProcessor()
    
    def test_single_line_calendar(self):
        """Test parsing of single line calendar."""
        calendar_text = "1 2 3 4 5 6 7"
        
        structure = self.processor.detect_calendar_structure(calendar_text)
        
        self.assertEqual(structure['days_count'], 7)
    
    def test_multiline_days(self):
        """Test calendar with days spanning multiple weeks."""
        calendar_text = """22 23 24 25 26 27 28
MANUEL MAR SANTI LOLA ELENA MANUEL SANTI
ELENA JOSE REQUE MARINA KIKO MAR LAURA
PATRICIA LAURA MANUEL JOSE SANTI ELENA REQUE
MARINA SANTI ELENA MAR MANUEL PATRICIA JOSE

29 30 31 1 2 3 4
REQUE ELENA MAR SANTI PATRICIA JOSE MANUEL
SANTI LOLA MANUEL MAR ELENA REQUE JOSE
LOLA MARINA SANTI ELENA MANUEL SANTI MAR
ELENA REQUE JOSE PATRICIA LAURA MANUEL SANTI"""
        
        structure = self.processor.detect_calendar_structure(calendar_text)
        
        self.assertGreater(structure['days_count'], 0)


if __name__ == '__main__':
    unittest.main()
