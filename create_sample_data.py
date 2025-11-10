#!/usr/bin/env python3
"""
Create sample shift schedule Excel files for testing.
"""

import pandas as pd
from datetime import datetime, timedelta

def create_sample_schedule():
    """Create a sample shift schedule in Excel format."""
    
    # Create dates for one month (Monday to Sunday weeks)
    start_date = datetime(2024, 11, 1)  # November 1, 2024 is a Friday
    dates = []
    current_date = start_date
    
    # Generate 30 days
    for i in range(30):
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Create a schedule with workers assigned to different shifts
    workers = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
    
    # Create a matrix: rows = dates, columns = positions
    data = {'Date': dates}
    
    # Assign 3 positions per day
    for pos in range(1, 4):
        data[f'Position {pos}'] = ['' for _ in dates]
    
    df = pd.DataFrame(data)
    
    # Assign workers in a rotating pattern
    for idx, date in enumerate(dates):
        # Each day has 3 workers
        for pos in range(1, 4):
            worker_idx = (idx + pos) % len(workers)
            df.loc[idx, f'Position {pos}'] = workers[worker_idx]
    
    # Save to Excel
    output_file = 'sample_schedule.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Created sample schedule: {output_file}")
    
    # Display preview
    print("\nPreview:")
    print(df.head(10))
    
    return output_file

if __name__ == '__main__':
    create_sample_schedule()
