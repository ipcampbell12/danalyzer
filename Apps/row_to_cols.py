import pandas as pd
import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Helpers.columns import adjust_column_widths
from task_manager import DataTaskManager

def process_course_data(student_file,request_file,dest_folder,checkStudents=False):
    requests_df =pd.read_excel(request_file)
    print(requests_df.columns)
    
    if checkStudents:
        # Read the Excel file
        student_df = pd.read_excel(student_file)
        print(student_df.columns)

        requests_df = requests_df.merge(student_df, how="inner", left_on="Student Number", right_on="student_number")
        print(f"Merged DataFrame shape: {requests_df.shape}")
        print(requests_df.head())

        print("Merged requests file with student file")
    # school_name= requests_df.at[2,"School"]

    # print(f"The school name is {school_name}")
    # Ensure no missing values in key columns
    requests_df.dropna(subset=['Student Number', 'Student Name', 'Course_Name', 'Course_Number'], inplace=True)
    print(f"DataFrame shape after dropping missing values: {requests_df.shape}")

    # Extract the first two letters of 'Course #' to classify courses
    requests_df['Course_Category'] = requests_df['Course_Number'].astype(str).str[:2]

    # Define updated course mapping
    course_mapping = {
        'MA': 'Math',
        'SC': 'Science',
        "HE" : "Health",
        'SS': 'Social Studies',
        'PE': 'Physical Education',
        'LA': 'Language Arts'
    }

    # Map courses based on first two letters
    requests_df['Course_Category'] = requests_df['Course_Number'].astype(str).str[:2].map(course_mapping)

    # Default "Elective" for AF and EL
    requests_df.loc[requests_df['Course_Number'].astype(str).str[:2].isin(['AF', 'EL']), 'Course_Category'] = 'Elective'

    # Create a separate column for "Alternative Elective"
    requests_df['Final_Category'] = requests_df.apply(
        lambda row: 'Alternative Elective' if row['Course_Category'] == 'Elective' and str(row['Request Type']).strip() == "Alternate"
        else row['Course_Category'], 
        axis=1
    )

    # Drop rows where Course_Category didn't match any known mapping
    requests_df.dropna(subset=['Course_Category'], inplace=True)

    # Sort by Student Number and Course Category for consistency
    requests_df.sort_values(by=['Student Number', 'Course_Category'], inplace=True)

    # Pivot table using `', '.join` to handle duplicate course names in the same category
    pivot_df = requests_df.pivot_table(
                index=['Student Number', 'Student Name', "Next Grade"], 
                columns='Final_Category', 
                values='Course_Name', 
                aggfunc=lambda x: ', '.join(map(str, x)),
                fill_value=""  # Ensures missing categories get empty strings instead of NaN
                    )

    print("Pivoted table")

    # Reset index
    pivot_df.reset_index(inplace=True)

    # Save to Excel
    new_path = dest_folder / f"Requests.xlsx"
    pivot_df.to_excel(new_path, index=False)

    print("Saved dataframe to excel")
    # Adjust column widths
    adjust_column_widths(new_path)

    # Open file
    subprocess.run(["start", "excel", new_path], shell=True)

