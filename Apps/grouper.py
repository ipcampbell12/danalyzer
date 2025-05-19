import pandas as pd
import random
import openpyxl
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from task_manager import DataTaskManager
from Helpers.columns import adjust_column_widths
import subprocess


manager = DataTaskManager()
folder = manager.return_folders()["powerschool_folder"]
file_path = folder / "MS Geometry.xlsx"

ms_df = pd.read_excel(file_path)
# Group by relevant fields and concatenate grades
result = (ms_df.groupby(['Lastfirst', 'Student Number','Course Name','Course Number','Teacher Name', 'Schoolname'])
           .agg({'Grade': lambda x: ','.join(x), 
                 'Storecode': lambda x: ','.join(x)})
           .reset_index())


# Rename columns for clarity
result.rename(columns={'Grade': 'Grades', 'Storecode': 'Quarters'}, inplace=True)

# Create "NO Fs?" column
result["NO Fs?"] = result["Grades"].apply(lambda x: 'F' not in x)

save_path = folder / "Processed MS Geometry.xlsx"
result.to_excel(save_path,index=False)
adjust_column_widths(save_path)
subprocess.run(["start", "excel", save_path], shell=True)