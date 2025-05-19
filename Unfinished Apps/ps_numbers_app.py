import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from Helpers.columns import adjust_column_widths
from folder_organizer import powerschool_folder, processed_yearly_numbers_folder

# File paths
school = "HES"
file_path = powerschool_folder / f"{school}.xlsx"
new_file_path = processed_yearly_numbers_folder / f"{school} LP Numbers.xlsx"

# Load data
ps_df = pd.read_excel(file_path)

# Collapse non-Dual language programs into "English Only"
ps_df['U_StudentsUserFields.LANGUAGE_PROGRAM'] = ps_df['U_StudentsUserFields.LANGUAGE_PROGRAM'].apply(
    lambda x: 'English Only' if isinstance(x, str) and 'Dual' not in x else x
)

# Group by school name and language program
cols_to_group = ['[schools]name', 'U_StudentsUserFields.LANGUAGE_PROGRAM']
ps_group = ps_df.groupby(cols_to_group)

# Create grouped DataFrame with total students per school and language program
grouped_df = ps_group.size().reset_index(name="Total Students").sort_values(by=['[schools]name', 'Total Students'], ascending=False).reset_index(drop=True)

# Calculate the total number of students per school
total_students_per_school = ps_df.groupby('[schools]name')['SchoolID'].count().reset_index(name='School Total')

# Create a new DataFrame to store the final results
final_rows = []
current_school = None

# Loop through the grouped data and add rows for each school and its programs
for index, row in grouped_df.iterrows():
    school_name = row['[schools]name']
    
    # When encountering a new school, check if we need to add the total for the previous school
    if school_name != current_school:
        if current_school is not None:
            # Add total row for the previous school
            total_row = total_students_per_school[total_students_per_school['[schools]name'] == current_school]
            if not total_row.empty:
                final_rows.append(pd.Series({
                    '[schools]name': None,  # Leave the school name blank in the total row for formatting
                    'U_StudentsUserFields.LANGUAGE_PROGRAM': 'Total Students',
                    'Total Students': total_row['School Total'].values[0]
                }))
                final_rows.append(pd.Series([None] * len(grouped_df.columns), index=grouped_df.columns))  # Blank row
            
        current_school = school_name
    
    # Add the current row (for the current school and language program)
    final_rows.append(row)

# Add the total row for the last school after the loop
total_row = total_students_per_school[total_students_per_school['[schools]name'] == current_school]
if not total_row.empty:
    final_rows.append(pd.Series({
        '[schools]name': None,  # Leave the school name blank in the total row for formatting
        'U_StudentsUserFields.LANGUAGE_PROGRAM': 'Total Students',
        'Total Students': total_row['School Total'].values[0]
    }))
    final_rows.append(pd.Series([None] * len(grouped_df.columns), index=grouped_df.columns))  # Blank row

# Create the final DataFrame
final_df = pd.DataFrame(final_rows)

# Write the final_df to an Excel file
final_df.to_excel(new_file_path, index=False, sheet_name='Language Program Totals')


# Adjust column widths in the Excel file
adjust_column_widths(new_file_path)

print("Excel file created with totals and collapsed language programs.")
