import pandas as pd
from datetime import date
import calendar
from columns import adjust_column_widths
import subprocess
import pathlib as Path
import os

def audit_discipline_discrepancies(file_path_incidents,file_path_absences,dest_folder):
    # manager = DataTaskManager()
    # folders = manager.get_folders("Find Discipline Discrepancies")
    # powerschool_folder = folders['powerschool_folder']

    # Read the Excel files into DataFrames
    # file_path_incidents = powerschool_folder + "/" + '12-17 Incidents.xlsx'
    # file_path_absences = powerschool_folder + "/" + '12-17 Absences.xlsx'
    current_date = pd.Timestamp('today')
    current_month = calendar.month_name[current_date.today().month]
    current_year = current_date.today().year
    # Read the Incident data
    df_incidents = pd.read_excel(file_path_incidents)

    # Function to generate date range excluding weekends with a grace period
    def generate_dates_with_grace(start_date, end_date, grace_days=4):
        # Extend the date range by the grace period
        extended_start = start_date - pd.Timedelta(days=grace_days)
        extended_end = end_date + pd.Timedelta(days=grace_days)
        # Generate date range excluding weekends
        date_range = pd.date_range(start=extended_start, end=extended_end, freq='B')  # 'B' frequency excludes weekends
        return date_range

    # Create an empty list to hold the expanded rows
    expanded_rows = []

    # Iterate through each row in the DataFrame
    for index, row in df_incidents.iterrows():
        try:
            # Parse 'Action plan begin date' and 'Action plan end date'
            start_date = pd.to_datetime(row['Action plan begin date'], errors='coerce')
            end_date = pd.to_datetime(row['Action plan end date'], errors='coerce')
            
            # Check if both dates are valid
            if pd.notna(start_date) and pd.notna(end_date):
                # Generate the list of dates with a grace period
                dates = generate_dates_with_grace(start_date, end_date)
                
                # Create a new row for each date
                for date in dates:
                    new_row = row.copy()
                    new_row['date'] = date.date()  # Keep only the date part
                    expanded_rows.append(new_row)
            else:
                # If dates are invalid, include the original row with a None date
                new_row = row.copy()
                new_row['date'] = None
                expanded_rows.append(new_row)
                print(f"Invalid date(s) for row {index}: begin date = {row['Action plan begin date']}, end date = {row['Action plan end date']}")
        
        except Exception as e:
            print(f"Error processing row {index}: {e}")

    # Create a new DataFrame from the expanded rows
    expanded_df = pd.DataFrame(expanded_rows)

    # Drop the original 'Action plan begin date' and 'Action plan end date' columns if needed
    expanded_df = expanded_df.drop(columns=['Action plan begin date', 'Action plan end date'])

    # Read the Absence data
    df_absences = pd.read_excel(file_path_absences)

    # Ensure the 'Att Date' and 'date' columns are datetime64[ns] type
    df_absences['Att Date'] = pd.to_datetime(df_absences['Att Date'], errors='coerce')
    expanded_df['date'] = pd.to_datetime(expanded_df['date'], errors='coerce')

    # Merge the DataFrames with an indicator
    merged_df = df_absences.merge(expanded_df, how="left", left_on=["Student Number", "Att Date"], right_on=["Student Number", "date"], indicator=True)

    # Filter non-matching rows
    non_matches_df = merged_df[merged_df['_merge'] == 'left_only']


    non_matches_df['Att Date'] = non_matches_df['Att Date'].dt.strftime('%m/%d/%Y')
    # Save the merged DataFrame and the non-matching rows to the same Excel file
    # dest_folder = manager.get_folders("Find Discipline Discrepancies")["discipline_folder"]
    schools_path = dest_folder / f"{current_month},{current_year} Incidents By School.xlsx"

    # with pd.ExcelWriter(output_file_path) as writer:
    #     merged_df.to_excel(writer, sheet_name='Merged Data', index=False)
    #     non_matches_df.to_excel(writer, sheet_name='Non-Matches', index=False)

    # adjust_column_widths(output_file_path)

    schools = non_matches_df["School_x"].unique().tolist()
    cols_to_drop = ["Lastfirst_y", "Grade Level_y", "Incident date", "Location", "Referred by", "Action", "Sub category", "School_y", "Id", "date"]

    with pd.ExcelWriter(schools_path) as writer:
        for school in schools:
            school_df = non_matches_df[non_matches_df["School_x"]==school]
            school_df = school_df.drop(cols_to_drop,axis=1)
            school_df = school_df.drop(['_merge'],axis=1)
            school_df.to_excel(writer, sheet_name=f"{school}", index=False)
            

    adjust_column_widths(schools_path)

    print(f"The data has been expanded and saved to '{schools_path}' with separate worksheets for merged data and non-matching rows.")
    print("The values from the first column of the non-matching rows have been copied to the clipboard.")
        
    subprocess.run(["start", "excel", schools_path], shell=True)
