import pandas as pd
import os
from columns import adjust_column_widths
import subprocess

file_path = "Valor Classes.xlsx"

# Read the Excel file
basic_df = pd.read_excel(file_path, sheet_name="Actual Classes")

# Filter rows based on the terms
terms = ["24-25", "S2"]
basic_df = basic_df[basic_df["Term Abbr"].isin(terms)]

# Print columns and check the first few rows for debugging
print(basic_df.columns)
print(basic_df.head(25))

# Create a list of the columns to use in the pivot table
cols = ['Student Number', 'Course Name', 'Teacher', 'Last_Name',
        'First_Name', 'Period', '1(A,B)', '2(A,B)', '3(A,B)', '4L(,B)',
        '5(A,B)', '6(A,B)', '7(A,B)', '7(A,B).1', '8(A,B)', 'Advisory']

# Create the pivot table
pivot_df = basic_df.pivot_table(index='Student Number', 
                                columns='Period', 
                                values=['Course Name', 'Teacher'],
                                aggfunc=lambda x: ', '.join(x.unique()))

# Adjust the column names to make them more readable
pivot_df.columns = [f"Period {col[1]} ({col[0]})" if col[0] == 'Teacher' else f"Period {col[1]}" for col in pivot_df.columns]

# Filter out empty rows based on the 'Period 1(A-B)' column
pivot_df = pivot_df[pd.notna(pivot_df['Period 1(A-B)']) & (pivot_df['Period 1(A-B)'] != '')]

# Reset index to ensure 'Student Number' is a column before merging
pivot_df.reset_index(inplace=True)

# Merge the 'Term Abbr' column from the original DataFrame to include it in the final output
pivot_df = pd.merge(pivot_df, basic_df[['Student Number', 'Term Abbr']].drop_duplicates(), on='Student Number', how='left')

periods = ["1", "2", "3", "4", "5", "6", "7", "8","ADV","SS"]

for col in pivot_df.columns:
    # Check if the column contains a period number (e.g., "1", "2", etc.)
    for period in periods:
        if period in col:
            print(period)
            print(col)
            # Construct the corresponding Teacher column name
            teacher_col = f"Period {period}(A-B) (Teacher)"
            print(teacher_col)
            if teacher_col in pivot_df.columns:
                print("This conidtion passed")
                # Combine the Course Name and Teacher columns
                period_col = f"Period {period}(A-B)"
                pivot_df[period_col] = pivot_df[period_col] + ' - ' + pivot_df[teacher_col]
                # Drop the Teacher column after combining
                pivot_df.drop(columns=[teacher_col], inplace=True)


print(pivot_df.head(40))
                
new_path = "Updated Classes.xlsx"
pivot_df.to_excel(new_path, index=False)

adjust_column_widths(new_path)
subprocess.run(["start", "excel", new_path], shell=True)
