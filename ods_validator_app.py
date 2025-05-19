import pandas as pd
import os
from columns import adjust_column_widths
from config import filtered_ods_cols, filtered_ssid_cols, schools_dict, language_dict
from difference import process_multiple_sheets
import subprocess


def validate_ods(ods_excel_path,ps_excel_path,ods_validations_folder):
    threshold = 5
    # Load the data
    # ods_excel_path = ods_folder / "12-10 ODS Validation.xlsx"
    # ps_excel_path = powerschool_folder / "12-10 SSID PS Download.xlsx"
    ps_df = pd.read_excel(ps_excel_path)
    ods_df = pd.read_excel(ods_excel_path)
    ods_df['Special Ed. Indicator'] = ods_df['Special Ed. Indicator'].replace({None: 'N', 'Special Education': 'Y'})
    ods_df['LEP Indicator'] = ods_df['LEP Indicator'].replace({'No': 'N', 'English Learner': 'Y'})
    ods_df = ods_df[ods_df['Language'].isin(language_dict.values())]
    ps_df = ps_df[ps_df['LangOrgnCd'].isin(language_dict.keys())]
    ps_df['LangOrgnCd'] = ps_df['LangOrgnCd'].replace(language_dict)

    combined_list = [list(pair) for pair in zip(filtered_ssid_cols, filtered_ods_cols)]

    # Path for the output Excel file
    final_path = ods_validations_folder / 'ODS Validation Pivots.xlsx'

    # Create a Pandas Excel writer
    with pd.ExcelWriter(final_path, engine='openpyxl') as writer:
        # Iterate through the combined list
        for idx, (ssid_col, ods_col) in enumerate(combined_list):
            # Create the pivot table for the SSID column from ps_df
            pivot_ssid = ps_df.groupby(['ResdSchlInstID', ssid_col]).size().unstack(fill_value=0).reset_index()

            # Create the pivot table for the ODS column from ods_df
            pivot_ods = ods_df.groupby(['School Name', ods_col]).size().unstack(fill_value=0).reset_index()

            # Replace the school codes with school names using the schools_dict
            pivot_ssid['ResdSchlInstID'] = pivot_ssid['ResdSchlInstID'].map(schools_dict).fillna(pivot_ssid['ResdSchlInstID'])
            
            # Filter the pivot tables to only include schools that are in the schools_dict
            
            valid_schools = list(schools_dict.values())
            pivot_ssid = pivot_ssid[pivot_ssid['ResdSchlInstID'].isin(valid_schools )].sort_values(by="ResdSchlInstID",ascending=True)
            pivot_ods = pivot_ods[pivot_ods['School Name'].isin(valid_schools )].sort_values(by='School Name',ascending=True)
            
            # Generate a sheet name (max 31 characters)
            sheet_name = f"{ssid_col}_{ods_col}"[:31]

            # Write the first pivot table to the sheet (starting from row 0)
            pivot_ssid.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0)

            # Write the second pivot table to the same sheet (starting a few columns after the first pivot)
            pivot_ods.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0, startcol=len(pivot_ssid.columns) + 3)

    # Adjust column widths in the final Excel file
    adjust_column_widths(final_path)

    # Open the Excel file automatically
    # os.system(f"start EXCEL.EXE {final_path}")
    # Example usage
    sheet_column_mapping = {
        'GndrCd_Gender': ('A', 'B'),
        'LangOrgnCd_Language': ('C', 'D'),
        'Sheet3': ('E', 'F'),
        'Sheet3': ('G', 'H'),  # Re-run on Sheet3 with different columns
    }

    # process_multiple_sheets(
    #     file_path=final_path,
    #     sheet_column_mapping=sheet_column_mapping,
    #     threshold_percentage=50,
    #     output_path=final_path
    # )

    subprocess.run(["start", "excel", final_path], shell=True)