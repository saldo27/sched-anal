#!/usr/bin/env python3
"""
Create a test PDF with calendar format for shift scheduling.
"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta
import calendar

def create_calendar_pdf(filename, year=2026, month=2):
    """Create a PDF with a calendar format for shifts."""
    
    doc = SimpleDocTemplate(filename, pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Get calendar data
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Workers
    workers = [
        ['Ana', 'Bob', 'Carlos', 'Diana', 'Eva', 'Frank', 'Gloria'],
        ['Bob', 'Carlos', 'Diana', 'Eva', 'Frank', 'Gloria', 'Ana'],
        ['Carlos', 'Diana', 'Eva', 'Frank', 'Gloria', 'Ana', 'Bob'],
        ['Diana', 'Eva', 'Frank', 'Gloria', 'Ana', 'Bob', 'Carlos'],
    ]
    
    # Build table data
    table_data = []
    
    # Header with day numbers
    header = []
    day_names = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sab', 'Dom']
    
    for day_name in day_names:
        header.append(day_name)
    
    table_data.append(header)
    
    # Add weeks
    for week_idx, week in enumerate(cal):
        for day_idx, day in enumerate(week):
            if day == 0:
                table_data.append([''] * 7)  # Empty row for weeks with missing days
                break
        else:
            # Add worker rows for this week
            for worker_list in workers[min(week_idx, len(workers)-1)]:
                row = []
                for day_idx, day in enumerate(week):
                    if day == 0:
                        row.append('')
                    else:
                        # Show day number and workers
                        if day_idx == 0:
                            row.append(f"{day}\n{worker_list}")
                        else:
                            row.append(worker_list if day_idx < len(worker_list) else '')
                table_data.insert(len(table_data), row)
    
    # Create table with proper formatting
    table = Table(table_data, colWidths=[1*inch]*7, rowHeights=[0.3*inch]*len(table_data))
    
    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ])
    
    table.setStyle(style)
    
    # Build document
    story = []
    style = getSampleStyleSheet()
    title = Paragraph(f"<b>Horario de Turnos - {month_name} {year}</b>", style['Heading1'])
    story.append(title)
    story.append(table)
    
    doc.build(story)
    print(f"Created test PDF: {filename}")

if __name__ == '__main__':
    create_calendar_pdf('test_calendar.pdf', year=2026, month=2)
