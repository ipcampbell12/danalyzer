import inquirer
import pandas as pd
import subprocess
import sys
import os
import re
import numpy as np
from datetime import timedelta, datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Helpers.columns import adjust_column_widths
from task_manager import DataTaskManager

manager = DataTaskManager()

input_folder = manager.return_folders()["powerschool_folder"]
map_folder = manager.return_folders()["map_folder"]
output_folder = manager.return_folders()["powerschool_folder"]
elpa_folder = manager.return_folders()["elpa_cards"]

def prompt_user(message, question_type, choices=None):
    question_types = {
        'list': inquirer.List,
        'input': inquirer.Text,
        'confirm': inquirer.Confirm,
        'checkbox': inquirer.Checkbox
    }

    if question_type not in question_types:
        raise ValueError(f"Unsupported question type: {question_type}")

    question_class = question_types[question_type]

    # Set up the question based on the type
    question = {
        'message': message,
        'choices': choices if choices else []
    }

    # Handle required arguments based on the question type
    if question_type == 'checkbox':
        question = [question_class('response', **question)]
    else:
        question = [question_class('response', **question)]

    # Prompt the user
    answer = inquirer.prompt(question)
    return answer['response']

def get_shared_columns(df1, df2):
    """Find shared columns between two DataFrames."""
    if df1.empty or df2.empty:
        return []
    shared_columns = list(set(df1.columns) & set(df2.columns))
    return shared_columns

def sanitize_sheet_name(name):
    """Sanitize the sheet name to remove invalid characters for Excel."""
    name = str(name)  # Convert to string if it's not already
    sanitized_name = re.sub(r'[\\/*?:"<>|]', '_', name)  # Replace invalid characters with underscore
    return sanitized_name

def convert_dates(df):
    """Convert only columns that contain the word 'date' in their header to datetime, keeping only the date."""
    for column in df.columns:
        if 'date' in column.lower():  # Check if 'date' is in the column name (case-insensitive)
            print(f"Converting column '{column}' to datetime")

            # Replace empty or NaN values with np.nan
            df[column] = df[column].replace(['', None], np.nan)

            # Check if the column contains numeric values (Excel serial numbers for dates)
            if df[column].dtype in ['float64', 'int64']:
                print(f"Column '{column}' contains numeric values, checking for Excel serial dates.")

                # Convert Excel serial numbers to datetime (if within reasonable range)
                def excel_serial_to_date(serial):
                    if pd.isna(serial):
                        return np.nan
                    try:
                        return (datetime(1900, 1, 1) + timedelta(days=serial - 2)).date()  # Get only the date part
                    except Exception:
                        return np.nan
                
                # Apply conversion to serial dates
                df[column] = df[column].apply(excel_serial_to_date)
            else:
                # Apply the datetime conversion with errors='coerce' to turn invalid values into NaT
                df[column] = pd.to_datetime(df[column], errors='coerce', dayfirst=True).dt.date  # Keep only the date part

            # Checking for any remaining invalid dates after conversion
            invalid_dates = df[column].isna()  # NaT will be generated for invalid dates
            print(f"Found {invalid_dates.sum()} invalid or missing dates in '{column}'")

        else:
            print(f"Skipping non-date column '{column}'")
    import re

    date_columns = [col for col in df.columns if "date" in col.lower()]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime("%m/%d/%Y")
    return df

def distribute_dfs(df, col, output_path):
    """Distribute data into different sheets based on a column."""
    val_list = df[col].unique().tolist()
    with pd.ExcelWriter(output_path) as writer:
        for val in val_list:
            sanitized_val = sanitize_sheet_name(str(val))  # Sanitize sheet name
            filtered_df = df[df[col] == val]
            filtered_df.to_excel(writer, sheet_name=sanitized_val, index=False)

    adjust_column_widths(output_path)
    subprocess.run(["start", "excel", output_path], shell=True)

def save_and_open_excel(df, output_path):
    """Save DataFrame to Excel, adjust column widths, and open in Excel."""
    df.to_excel(output_path, index=False)
    adjust_column_widths(output_path)
    subprocess.run(["start", "excel", output_path], shell=True)

def get_single_file_path(directory):
    """Prompt user to select a single file from a directory."""
    files = [f for f in os.listdir(directory) if f.endswith('.xlsx') or f.endswith('.xls')]
    if not files:
        print(f"No Excel files found in {directory}.")
        return None

    answer = prompt_user(f"Select a file from {directory}", 'list', choices=files)
    return os.path.join(directory, answer)

def get_columns_for_grouping(df, shared_columns):
    """Prompt user to select multiple columns to group by or choose 'No column' to skip."""
    selected_columns = prompt_user("Select columns to group by (or choose 'No column' to skip):", 'checkbox', choices=['No column'] + shared_columns)
    
    # If 'No column' is selected, return an empty list
    if 'No column' in selected_columns:
        return []  

    return selected_columns

def get_column_selection_for_filtering(df, shared_columns):
    """Prompt user to select columns for filtering from the merged DataFrame."""
    selected_columns = prompt_user("Select columns to filter on (or choose 'No column' to skip):", 'checkbox', choices=['No column'] + shared_columns)
    
    if 'No column' in selected_columns:
        return []  # Return empty list if "No column" is selected

    return selected_columns

def filter_columns(df, selected_columns):
    """Filter the DataFrame based on the selected columns."""
    filtered_df = df.copy()

    for column in selected_columns:
        print(f"\nFiltering column '{column}'")
        unique_values = df[column].dropna().unique()

        filter_values = prompt_user(f"Select values to filter for '{column}':", 'checkbox', choices=sorted(map(str, unique_values)))

        if filter_values:
            filtered_df = filtered_df[filtered_df[column].isin(filter_values)]
        else:
            print(f"No values selected for filtering '{column}'. Skipping column.")

    return filtered_df

def sort_df(df, col):
    """Sort the DataFrame based on a column."""
    return df.sort_values(by=col)

def process_data(df):
    """Group, filter, sort, and save the data to Excel."""
    shared_columns = get_shared_columns(df, df)

    # Grouping
    group_by_columns = get_columns_for_grouping(df, shared_columns)
    grouped_df = df.groupby(group_by_columns).size().reset_index(name="Count") if group_by_columns else df

    # Filtering
    selected_columns = get_column_selection_for_filtering(grouped_df, shared_columns)
    filtered_df = filter_columns(grouped_df, selected_columns) if selected_columns else grouped_df
    
    # Dynamically convert date columns (only columns with 'date' in the name)
    filtered_df = convert_dates(filtered_df)

    # Confirm before proceeding
    rows, cols = filtered_df.shape
    print(f"\nFiltered DataFrame with {cols} columns and {rows} rows.")

    # Adjusted comparison logic: now checks for True (yes)
    if prompt_user(f"Proceed with creating the spreadsheet with {rows} rows and {cols} columns?", 'confirm'):
        output_path = os.path.join(elpa_folder, "output.xlsx")

        # Ask if the user wants to sort
        if prompt_user("Would you like to sort the final data?", 'confirm'):
            sort_col = prompt_user("Select column to sort by:", 'list', choices=filtered_df.columns.tolist())
            sorted_df = sort_df(filtered_df, sort_col)
        else:
            sorted_df = filtered_df  # No sorting, keep original

        # Ask if the user wants to distribute data into sheets
        if prompt_user("Would you like to distribute the data into different sheets based on a column?", 'confirm'):
            dist_col = prompt_user("Select column to distribute on:", 'list', choices=sorted_df.columns.tolist())
            distribute_dfs(sorted_df, dist_col, output_path)
        else:
            save_and_open_excel(sorted_df, output_path)

        print(f"Spreadsheet 'output.xlsx' created successfully.")
    else:
        print("Process aborted. No spreadsheet created.")
        return False

    return True

def main():
    """Main function to handle file selection, merging (optional), and processing."""
    while True:
        file1 = get_single_file_path(input_folder)  

        if file1:
            df1 = pd.read_excel(file1)

            merge_answer = prompt_user("Would you like to merge this with another file?", 'confirm')

            if merge_answer:  # Check for True instead of 'Y'
                file2 = get_single_file_path(input_folder)

                if file2:
                    df2 = pd.read_excel(file2)
                    shared_columns = get_shared_columns(df1, df2)

                    if not shared_columns:
                        print("No shared columns to merge on. Proceeding with the first file only.")
                        merged_df = df1
                    else:
                        merged_df = pd.merge(df1, df2, on=shared_columns, how="inner")
                        print(f"Successfully merged the files.\n")
                else:
                    print("No valid second file selected. Proceeding with the first file only.")
                    merged_df = df1
            else:
                print("Proceeding without merging.")
                merged_df = df1

            if process_data(merged_df):
                break  
        else:
            print("No valid file selected. Exiting.")
            break  

if __name__ == "__main__":
    main()
