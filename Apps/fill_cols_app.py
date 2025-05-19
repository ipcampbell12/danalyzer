import pandas as pd
import os
import calendar
import sys
import subprocess
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Helpers.columns import adjust_column_widths
from task_manager import DataTaskManager

manager = DataTaskManager()

elpa_folder = manager.return_folders()["elpa_cards"]

path = elpa_folder / "All Schools OSAS Testing Info.xlsx"

osas_df = pd.read_excel(path)

print(osas_df.columns)

fill_cols = ['EL Flag', 'IEP Flag', '504 Flag']
other_cols = ['Current IEP Date', 'ELA Accessibility Supports', 'Math Accessibility Supports', 'Science Accessibility Supports']

def process_columns(df, fill_cols, other_cols):
    # Process fill_cols
    for col in fill_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: "Yes" if x == 1 else "No" if pd.isna(x) or x == 0 else x)
    
    # Process other_cols
    for col in other_cols:
        if col in df.columns:
            df[col] = df[col].fillna('NA')
    
    return df

# Process the columns
osas_df = process_columns(osas_df, fill_cols, other_cols)

# Save the updated DataFrame to the same Excel file
osas_df.to_excel(path, index=False)
adjust_column_widths(path)
subprocess.run(["start", "excel", path], shell=True)

print(f"Processed DataFrame saved to {path}")

