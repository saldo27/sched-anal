# sched-anal
Scheduler analyzer - Analyze shift schedules from PDF or Excel files

## Overview

This application analyzes PDF or Excel files containing shift schedules (calendar format, Monday to Sunday) and generates comprehensive statistics for each worker.

## Features

The analyzer calculates the following statistics for each worker:
- **Total Shifts**: Total number of shifts assigned
- **Shifts per Month**: Breakdown of shifts by month
- **Friday Shifts**: Number of shifts on Fridays
- **Saturday Shifts**: Number of shifts on Saturdays
- **Sunday Shifts**: Number of shifts on Sundays
- **Weekend Shift %**: Percentage of shifts that fall on weekends (Fri-Sun)
- **Last Position Shifts**: Number of times assigned to the last position in a day

## Installation

1. Clone the repository:
```bash
git clone https://github.com/saldo27/sched-anal.git
cd sched-anal
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Analyze a shift schedule file:
```bash
python sched_analyzer.py schedule.xlsx
```

### Output Formats

Display results in different formats:
```bash
# Table format (default)
python sched_analyzer.py schedule.xlsx

# CSV format
python sched_analyzer.py schedule.xlsx --format csv

# JSON format
python sched_analyzer.py schedule.xlsx --format json
```

### Save Results to File

Save the analysis results to a file:
```bash
python sched_analyzer.py schedule.xlsx -o results.csv
```

### Supported File Formats

- Excel files: `.xlsx`, `.xls`
- PDF files: `.pdf`

## Input File Format

The application expects shift schedule files in calendar format with:
- Dates arranged in columns or rows (Monday to Sunday weeks)
- Worker names in cells indicating shift assignments
- Optional: Position numbers (1, 2, 3, etc.) for tracking last position

### Example Excel Format

| Date       | Position 1 | Position 2 | Position 3 |
|------------|------------|------------|------------|
| 2024-11-01 | Alice      | Bob        | Charlie    |
| 2024-11-02 | Bob        | Charlie    | Diana      |
| 2024-11-03 | Charlie    | Diana      | Eve        |

## Testing with Sample Data

Generate and analyze sample data:
```bash
# Create sample schedule
python create_sample_data.py

# Analyze the sample
python sched_analyzer.py sample_schedule.xlsx
```

## Requirements

- Python 3.7+
- pandas
- openpyxl (for Excel files)
- pdfplumber (for PDF files)
- tabulate (for formatted output)

See `requirements.txt` for full dependency list.

## License

MIT License
