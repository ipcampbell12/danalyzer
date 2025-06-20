import sys
import os
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Helpers.other_funcs import process_date_text, highlight_invalid_rows
from Helpers.columns import adjust_column_widths
from Helpers.config import discipline_cols
from task_manager import DataTaskManager
import pandas as pd



def validate_discipline_data(discipline_file_path, dest_path):
     # Read the discipline data from the Excel file
    discipline_df = pd.read_excel(discipline_file_path)
#     # Ensure 'Incident Date' is in datetime format
#     discipline_df['Incident Date'] = pd.to_datetime(discipline_df['Incident Date'], errors='coerce')

#     # Check for missing or invalid dates
#     invalid_dates = discipline_df[discipline_df['Incident Date'].isna()]
#     if not invalid_dates.empty:
#         print("Invalid or missing Incident Dates found:")
#         print(invalid_dates[['Incident Date', 'Student Number']])

    # Process 'Action plan begin date' and 'Action plan end date'
    discipline_df['Dateified Discipline Date'] = discipline_df['DsplnDtTxt'].apply(process_date_text)
    discipline_df['Dateified Discipline Incident Date'] = discipline_df['DsplnIncdntDtTxt'].apply(process_date_text)
    discipline_df['Dateified Discipline Incident Date'] = pd.to_datetime(
        discipline_df['Dateified Discipline Incident Date'], format='%m/%d/%Y', errors='coerce'
    )
    discipline_df['Dateified Discipline Date'] = pd.to_datetime(
        discipline_df['Dateified Discipline Date'], format='%m/%d/%Y', errors='coerce'
    )
    discipline_df['Valid Discipline Date'] = discipline_df.apply(lambda row: row['Dateified Discipline Date'] >= row['Dateified Discipline Incident Date'], axis=1)
    discipline_df['Dateified Discipline Date'] = discipline_df['Dateified Discipline Date'].dt.strftime('%m/%d/%Y')
    discipline_df['Dateified Discipline Incident Date'] = discipline_df['Dateified Discipline Incident Date'].dt.strftime('%m/%d/%Y')

    # List your weapon and offense columns
    weapon_cols = [col for col in discipline_df.columns if col.endswith('WpnTypCd')]
    offense_cols = [col for col in discipline_df.columns if col.endswith('OffnsTypCd')]

    def is_valid_row(row):
        # Check if any weapon code is not 98
        weapon_involved = any(row[w] != 98 for w in weapon_cols if pd.notna(row[w]))
        # If so, check if any offense code is 3700
        if weapon_involved:
            return any(row[o] == 3700 for o in offense_cols if pd.notna(row[o]))
        return True  # If all weapon codes are 98, it's valid

    # Apply the validation
    discipline_df['Valid Weapons Row'] = discipline_df.apply(is_valid_row, axis=1)
    discipline_df['Valid Days'] = discipline_df['DsplnDays'] != 0

    # Create the 'Valid Record' column as before
    def get_valid_record(row):
        messages = []
        if not row['Valid Discipline Date']:
            messages.append("Invalid discipline date: incident date must be before or equal to discipline date")
        if not row['Valid Weapons Row']:
            messages.append("Invalid weapons row: if a weapon is involved, an offense code of 3700 must be present")
        if not row['Valid Days']:
            messages.append("Invalid days: DsplnDays must not be zero")
        return "; ".join(messages)

    discipline_df['Valid Record'] = discipline_df.apply(get_valid_record, axis=1)

    # Drop the temporary validation columns before saving
    discipline_df.drop(['Valid Discipline Date', 'Valid Weapons Row', 'Valid Days'], axis=1, inplace=True)
    
    schools = discipline_df["AttndSchlInstID"].unique().tolist()
    
    discipline_df = discipline_df[discipline_cols]
#     with pd.ExcelWriter(dest_path) as writer:
#         for school in schools:
#             print("Writing data for school:", school)
#             school_df = discipline_df[discipline_df["AttndSchlInstID"] == school]
#             school_df.to_excel(writer, sheet_name=school, index=False)
    # Now apply highlighting after the file is written
#     highlight_invalid_rows(dest_path, valid_record_col='Valid Record')
    # Now write to Excel
    discipline_df.to_excel(dest_path, index=False)
    adjust_column_widths(dest_path)
    
    print("Discipline data validation complete.")
    print(f"Validated discipline data saved to {dest_path}")

    subprocess.run(["start", "excel", dest_path], shell=True)
    return discipline_df

manager = DataTaskManager()
# folder_loc ="map_folder"
folder = manager.return_folders()["powerschool_folder"]
src_path = os.path.join(folder, "6-18 Discipline Compliance Download.xlsx")
dest_path = os.path.join(folder, "Validated Discipline Data.xlsx")
discipline_df = validate_discipline_data(src_path, dest_path)