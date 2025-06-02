import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from task_manager import DataTaskManager
from Helpers.columns import adjust_column_widths
import subprocess


def maxify_spreadsheet(file_path_max, sheet_name, final_name, maxify_col, dest_folder, ref_col, isDate=False):
    # Read the Excel file
    df_max = pd.read_excel(file_path_max, sheet_name=sheet_name)

    if isDate:
        # Convert the maxify_col to datetime, coercing errors to NaT
        df_max[maxify_col] = pd.to_datetime(df_max[maxify_col], errors='coerce')

        # Drop rows where maxify_col could not be converted to datetime
        df_max = df_max.dropna(subset=[maxify_col])

    # Find the index of the maximum value for each group
    idx = df_max.groupby(ref_col)[maxify_col].idxmax()

    # Select the rows with the maximum values
    df_max = df_max.loc[idx]

    df_max = df_max.rename(columns={maxify_col: "Maxified " + maxify_col})

    # Define the output path
    output_path = os.path.join(dest_folder, f"Maxified {final_name}.xlsx")

    # Save the result to an Excel file
    df_max.to_excel(output_path, index=False, sheet_name=sheet_name)

    # Adjust column widths
    adjust_column_widths(output_path)

    # Open the file in Excel
    subprocess.run(["start", "excel", output_path], shell=True)

    print(f"Maxified data with the highest row saved to {output_path}")


# Example usage
manager = DataTaskManager()
# folder_loc ="map_folder"
folder = manager.return_folders()["ode"]
path = os.path.join(folder, "Misc3.xlsx")
sheet_name = "Misc3"
final_name = "Misc3"
maxify_col = "ExitDate"
ref_col = "[students]student_number"

# Call with isDate=True for datetime columns
maxify_spreadsheet(path, sheet_name, final_name, maxify_col, folder, ref_col, isDate=True)

# Example for non-datetime columns
# maxify_spreadsheet(path, sheet_name, final_name, "SomeOtherColumn", folder, ref_col, isDate=False)

