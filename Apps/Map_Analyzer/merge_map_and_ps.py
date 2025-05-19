import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill,Font,Alignment
import os
from Apps.Map_Analyzer.create_pivot_sheets import create_pivot_sheets
from Helpers.map_config import rows_to_highlight,other_cols, race_cols, y_and_n_cols
from Helpers.columns import adjust_column_widths
from Helpers.other_funcs import cleanup_demo_sheet
from Helpers.map_config import columns_to_keep
import subprocess

def merge_with_grade_level(map_file, ps_df):
    map_df = map_file
    # ps_df = pd.read_excel(ps_file, sheet_name="Filtered Demographics")
    merged_df = map_df.merge(ps_df, how="left", left_on="StudentID", right_on="DistStdntID")
    print("Grade level column merged")
    return merged_df

import pandas as pd

def merge_with_langauge_file(ps_file, lang_file):
    # Read the PowerSchool file
    ps_df = pd.read_excel(ps_file)
    
    # Read the language file, selecting only needed columns
    lang_df = pd.read_excel(lang_file, usecols=["student_number", "InDualFg", "LangProg"])
    
    # Merge the two DataFrames
    merged_df = ps_df.merge(lang_df, how="left", left_on="DistStdntID", right_on="student_number")
    
    print("Language column merged")
    return merged_df


def combine_excel_workbooks(input_files, output_file, columns_to_keep,ps_file,lang_file):
    """
    Combine multiple sheets from different Excel workbooks vertically with a 'SheetName' column.
    
    Args:
    - input_files (list): List of paths to the input Excel files.
    - output_file (str): Path to save the combined output Excel file.
    """
    # Initialize an empty list to store DataFrames
    
    for file in input_files:
        print(file)
        
    if len(input_files) > 1:
        dfs = []
        # Read each Excel file and add a 'SheetName' column
        for file in input_files:
            # Extract file name without extension as 'SheetName'
            sheet_name = os.path.splitext(os.path.basename(file))[0]
            print(f"Reading {sheet_name} sheet")
            # Read all sheets into pandas DataFrames
            sheets = pd.read_excel(file, sheet_name=None)  # None reads all sheets
            print("Reading sheets")

            # Concatenate each sheet's DataFrame with 'SheetName' column
            for name, df in sheets.items():
                # Filter columns to keep
                print(df.head(4))
                df_filtered = df[columns_to_keep].copy()  # Make a copy to avoid modifying the original DataFrame
                # Add 'SheetName' column using assign
                df_filtered = df_filtered.assign(SheetName=sheet_name)
                # Append to list
                dfs.append(df_filtered)
    

        # Concatenate all DataFrames vertically
        combined_df = pd.concat(dfs, ignore_index=True)
    else:
        combined_df = pd.read_excel(input_files[0])
        combined_df = combined_df[columns_to_keep].copy()  # Ensure columns are filtered

    print("All excel workbooks have been combined")
    
    ps_df = merge_with_langauge_file(ps_file, lang_file)
    # Save the combined DataFrame to a new Excel file

    ps_df = cleanup_demo_sheet(ps_df, other_cols, race_cols, y_and_n_cols)

    final_df = merge_with_grade_level(combined_df, ps_df)

    final_df = final_df.dropna(subset=["EnrlGrdCd"])
    print("Removed rows with no grade level")

    # Save the combined DataFrame to a new Excel file
    with pd.ExcelWriter(output_file) as writer:
        final_df.to_excel(writer, sheet_name="24-25 MAP Data", index=False)
        print("New Excel file created")

    # Adjust column widths based on content using openpyxl
    adjust_column_widths(output_file)

    print('Finished with combining and merging MAP and demographic data')
    return output_file