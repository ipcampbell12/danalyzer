import pandas as pd
from openpyxl import load_workbook
from Helpers.map_config import fluency_cols, ps_cols, other_cols, race_cols, y_and_n_cols
from Apps.Map_Analyzer.map_fluency_pivot_app import create_pivot_sheets
from Helpers.other_funcs import cleanup_demo_sheet
from Helpers.columns import adjust_column_widths
from Apps.Map_Analyzer.merge_map_and_ps import combine_excel_workbooks

def process_fluency_data(fall_map_input,winter_map_input,spring_map_input, ps_file_path,lang_file, dest_folder):
    combined_fluency_path = dest_folder / "24-25 Combined MAP Fluency Data.xlsx"
    fluency_pivot_path = dest_folder / "Disaggregated Fluency Pivots.xlsx"

    combine_excel_workbooks([fall_map_input,winter_map_input,spring_map_input],combined_fluency_path,fluency_cols,ps_file_path,lang_file)
    # Step 1: Clean PowerSchool data before merging
    # cleanup_demo_sheet(ps_file_path, other_cols, race_cols, y_and_n_cols)

    fluency_df = pd.read_excel(combined_fluency_path)
    # Step 2: Load and filter Fluency data

    # Step 5: Generate pivot sheets
    create_pivot_sheets(fluency_df, fluency_pivot_path)

    # Step 6: Adjust column widths in pivot file
    adjust_column_widths(fluency_pivot_path)


