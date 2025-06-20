# import sys
# import os
# import subprocess

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from Helpers.other_funcs import process_date_text, highlight_invalid_rows
# from Helpers.columns import adjust_column_widths
# from Helpers.config import discipline_cols
# from task_manager import DataTaskManager
# import pandas as pd


# def validate_class_schedule_data(class_schedule_file_path):
#      class_schedule_df = pd.read_excel(class_schedule_file_path, sheet_name='Working Tab')

#      date_cols = ['StdntStrtDtTxt', 'StdntEndDtTxt','TchrStrtDtTxt','TchrEndDtTxt']

#      # Step 1: Convert to datetime for calculations
#      for col in date_cols:
#            print("Dateifying column:", col)
#            class_schedule_df[col] = class_schedule_df[col].apply(process_date_text)
#            class_schedule_df[col] = pd.to_datetime(class_schedule_df[col], errors='coerce')

#      # Do your calculations here
#      class_schedule_df['Teacher Days'] = (class_schedule_df['TchrEndDtTxt'] - class_schedule_df['TchrStrtDtTxt']).dt.days
#      print("Teacher Days calculated.")
#      class_schedule_df['Student Days'] = (class_schedule_df['StdntEndDtTxt'] - class_schedule_df['StdntStrtDtTxt']).dt.days
#      print("Student Days calculated.")

#      # Step 2: Format as MM/DD/YYYY for Excel output
#      for col in date_cols:
#           class_schedule_df[col] = class_schedule_df[col].dt.strftime('%m/%d/%Y')
     
#      with pd.ExcelWriter(class_schedule_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
#           class_schedule_df.to_excel(writer, sheet_name='ModifiedData', index=False)
#           print("Modified data written to 'ModifiedData' sheet.")
#      adjust_column_widths(class_schedule_file_path)
#      subprocess.run(["start", "excel", class_schedule_file_path], shell=True)

# path = r"C:\Users\inpcampbell\Desktop\ODE\2025 Class Schedule\WES Class Schedule.xlsx"
# validate_class_schedule_data(path)

import sys
import os
import subprocess
import pandas as pd
import numpy as np

# Local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Helpers.other_funcs import process_date_text
from Helpers.columns import adjust_column_widths


def validate_class_schedule_data(class_schedule_file_path, holiday_ranges):
    # Convert holiday ranges to a sorted unique numpy array of business days
    holiday_dates = set(np.concatenate(holiday_ranges))
    holidays = np.array(sorted(holiday_dates), dtype='datetime64[D]')

    # Load Excel data
    class_schedule_df = pd.read_excel(class_schedule_file_path, sheet_name='Working Tab')

    date_cols = ['StdntStrtDtTxt', 'StdntEndDtTxt', 'TchrStrtDtTxt', 'TchrEndDtTxt']

    for col in date_cols:
        print("Dateifying column:", col)
        class_schedule_df[col] = class_schedule_df[col].apply(process_date_text)
        class_schedule_df[col] = pd.to_datetime(class_schedule_df[col], errors='coerce')

    # Calculate business days excluding weekends and holidays
    def business_days(start, end):
        if pd.notnull(start) and pd.notnull(end):
            return np.busday_count(start.date(), end.date(), holidays=holidays)
        return None

    class_schedule_df['Teacher Days'] = class_schedule_df.apply(
        lambda row: business_days(row['TchrStrtDtTxt'], row['TchrEndDtTxt']),
        axis=1
    )
    print("Teacher Days calculated.")

    class_schedule_df['Student Days'] = class_schedule_df.apply(
        lambda row: business_days(row['StdntStrtDtTxt'], row['StdntEndDtTxt']),
        axis=1
    )
    print("Student Days calculated.")

    # Format dates for Excel
    for col in date_cols:
        class_schedule_df[col] = class_schedule_df[col].dt.strftime('%m/%d/%Y')

    # Write to Excel in a new tab
    with pd.ExcelWriter(class_schedule_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        class_schedule_df.to_excel(writer, sheet_name='ModifiedData', index=False)
        print("Modified data written to 'ModifiedData' sheet.")

    # Post-processing
    adjust_column_widths(class_schedule_file_path)
    subprocess.run(["start", "excel", class_schedule_file_path], shell=True)

from datetime import datetime, timedelta
import numpy as np

def generate_holiday_range(start_str, end_str):
    """
    Generate a list of business days (weekdays only) between two date strings (inclusive).
    Format should be 'YYYY-MM-DD'.
    """
    start = datetime.strptime(start_str, "%Y-%m-%d").date()
    end = datetime.strptime(end_str, "%Y-%m-%d").date()
    delta = timedelta(days=1)
    dates = []
    while start <= end:
        if start.weekday() < 5:
            dates.append(np.datetime64(start))
        start += delta
    return dates

# Your master holiday list to pass in
my_holiday_ranges = [
    generate_holiday_range('2024-09-02', '2024-09-02'),  # Labor Day
    generate_holiday_range('2024-09-23', '2024-09-23'),
    generate_holiday_range('2024-10-07', '2024-10-07'),
    generate_holiday_range('2024-11-01', '2024-11-01'),
    generate_holiday_range('2024-11-11', '2024-11-11'),  # Veterans Day
    generate_holiday_range('2024-11-28', '2024-11-29'),  # Thanksgiving
    generate_holiday_range('2024-12-23', '2025-01-03'),  # Winter Break
    generate_holiday_range('2025-01-07', '2025-01-07'),
    generate_holiday_range('2025-01-20', '2025-01-20'),  # MLK Day
    generate_holiday_range('2025-02-03', '2025-02-03'),
    generate_holiday_range('2025-02-17', '2025-02-17'),  # Presidents’ Day
    generate_holiday_range('2025-03-24', '2025-03-28'),  # Spring Break
    generate_holiday_range('2025-04-14', '2025-04-14'),
    generate_holiday_range('2025-05-12', '2025-05-12'),
    generate_holiday_range('2025-05-26', '2025-05-26'),  # Memorial Day
]

path = r"C:\Users\inpcampbell\Desktop\ODE\2025 Class Schedule\WES Class Schedule.xlsx"
validate_class_schedule_data(path, my_holiday_ranges)