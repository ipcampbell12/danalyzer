import pandas as pd
from folder_organizer import processed_sports_folder, powerschool_folder
import os
from datetime import datetime
from Helpers.columns import adjust_column_widths
from task_manager import DataTaskManager


manager = DataTaskManager()
# Read the original Excel file
current_date = datetime.now().strftime("%m/%d/%Y")
excel_path = powerschool_folder / "12-10-24 Sports Attendance.xlsx"
output_path = processed_sports_folder / f"12-12 Sports Attendance.xlsx"
sports_df = pd.read_excel(excel_path)

# List of columns to melt (sports)
cols_to_melt = [
    "Activities.boys_basketball",
    "Activities.girls_basketball",
    "Activities.wrestling",
    "Activities.cheerleader"
]

# Columns to keep (unmelted)
unmelted = [
    'First_Name', 'Last_Name', 'Student_Number', 'Grade_level',
    'Student Attendance Percent', 'Total Days Enrolled', 'Attendance Days',
    'Absence Days', 'Tardy'
]

# Melt the DataFrame
melted_df = sports_df.melt(id_vars=unmelted, value_vars=cols_to_melt, var_name='Sports', value_name='Value')

# Filter rows where 'Value' is 1
result_df = melted_df[melted_df['Value'] == 1]

# Drop the 'Value' column as it's no longer needed
result_df = result_df.drop(columns=['Value'])

# Create a pivot table for the average 'Student Attendance Percent' by sport
pivot_table_avg = result_df.pivot_table(
    index='Sports',
    values='Student Attendance Percent',
    aggfunc='mean'
).reset_index()

pivot_table_avg['Student Attendance Percent'] = pivot_table_avg['Student Attendance Percent'].round(2)

# Create a second pivot table for Attendance Days / Total Days Enrolled by sport
pivot_table_ratio = result_df.groupby('Sports').agg(
    Total_Attendance_Days=('Attendance Days', 'sum'),
    Total_Enrolled_Days=('Total Days Enrolled', 'sum')
).reset_index()

# Calculate the ratio and round to 2 decimal places
pivot_table_ratio['Attendance Ratio'] = (pivot_table_ratio['Total_Attendance_Days'] / pivot_table_ratio['Total_Enrolled_Days']).round(4)*100

# Drop intermediate columns to keep only relevant data
pivot_table_ratio = pivot_table_ratio[['Sports', 'Attendance Ratio']]

# Write the melted DataFrame and both pivot tables to separate sheets in the same Excel file
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    result_df.to_excel(writer, sheet_name='Melted Data', index=False)
    
    # Write the first pivot table (average attendance)
    pivot_table_avg.to_excel(writer, sheet_name='Pivot Table', index=False, startrow=0, startcol=0)
    
    # Write the second pivot table (attendance ratio) next to it
    pivot_table_ratio.to_excel(writer, sheet_name='Pivot Table', index=False, startrow=0, startcol=4)

adjust_column_widths(output_path)
# Open the Excel file automatically
os.system(f"start EXCEL.EXE {output_path}")
