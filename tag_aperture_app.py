import pandas as pd
import os
from columns import adjust_column_widths
from pathlib import Path
from datetime import date
import calendar
import subprocess
from task_manager import DataTaskManager

manager = DataTaskManager()

def tag_aperture(lower_app_file,):
    current_month = calendar.month_name[date.today().month]
    current_year = date.today().year
    # Make sure to use the correct path to the 'aperture_folder'
    aperture_folder = Path(aperture_folder)

    # Get all CSV files in the aperture_folder
    rating_files = [f for f in os.listdir(aperture_folder) if f.endswith('.csv')]

    # Initialize a list of dataframes
    rating_dfs = []

    # Loop through the rating files and read each one
    for file in rating_files:
        file_path = aperture_folder / file  # Ensure to get the full path
        try:
            df = pd.read_csv(file_path)
            rating_dfs.append(df)
        except Exception as e:
            print(f"Failed to read {file}: {e}")

    # Print the list of files and the corresponding dataframes
    combined_df = pd.concat(rating_dfs, ignore_index=True)

    combined_path = proccess_dessa_folder / f"{current_month}, {current_year} Combined DESSA Ratings"
    combined_df.to_excel(combined_path,index=False)
    subprocess.run(["start", "excel", combined_path], shell=True)