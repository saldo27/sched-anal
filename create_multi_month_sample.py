#!/usr/bin/env python3
"""
Create a multi-month sample shift schedule for better testing.
"""

import pandas as pd
from datetime import datetime, timedelta

def create_multi_month_schedule():
    """Create a sample shift schedule spanning multiple months."""
    
    # Create dates for 3 months
    start_date = datetime(2024, 10, 1)  # October 1, 2024
    dates = []
    current_date = start_date
    
    # Generate 90 days (approximately 3 months)
    for i in range(90):
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Create workers
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
    output_file = 'multi_month_schedule.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Created multi-month schedule: {output_file}")
    print(f"Date range: {dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}")
    print(f"Total days: {len(dates)}")
    
    # Display preview
    print("\nPreview (first 5 days):")
    print(df.head(5))
    print("\nPreview (last 5 days):")
    print(df.tail(5))
    
    return output_file

if __name__ == '__main__':
    create_multi_month_schedule()
