import pandas as pd
import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Helpers.columns import adjust_column_widths
from task_manager import DataTaskManager
from Apps.avid_validator_app import validate_avid_file

def pivot_courses(enrollment_file):
    # requests_df =pd.read_excel(enrollment_file)
    requests_df = enrollment_file
    # print(requests_df.columns)
    
    
    year= requests_df.at[2,"TermID"]
    
    # print(f"The school name is {school_name}")
    # Ensure no missing values in key columns
    # requests_df.dropna(subset=['[students]student_number', '[students]lastfirst', '[courses]course_name', '[courses]credit_type','[schools]name','[students]grade_level'], inplace=True)
    print(f"DataFrame shape after dropping missing values: {requests_df.shape}")

    # Extract the first two letters of 'Course #' to classify courses
    requests_df['Course_Category'] = requests_df['[courses]credit_type'].astype(str).str[:2]

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
    requests_df['Course_Category'] = requests_df['[courses]credit_type'].astype(str).str[:2].map(course_mapping)

    # Default "Elective" for AF and EL
    requests_df.loc[requests_df['[courses]credit_type'].astype(str).str[:2].isin(['AF', 'EL']), 'Course_Category'] = 'Elective'

    # Drop rows where Course_Category didn't match any known mapping
    requests_df.dropna(subset=['Course_Category'], inplace=True)

    # Sort by [students]student_number and Course Category for consistency
    requests_df.sort_values(by=['[students]student_number', 'Course_Category'], inplace=True)

    # Pivot table using `', '.join` to handle duplicate course names and grades
    pivot_df = requests_df.pivot_table(
                index=['[students]student_number', '[students]lastfirst', '[schools]name','[students]grade_level'], 
                columns='Course_Category', 
                values='[courses]course_name',
                aggfunc=lambda x: ', '.join(map(str, x)),
                fill_value=""  # Ensures missing categories get empty strings instead of NaN
    )
    print(f"Row count after pivoting: {len(pivot_df)}")

        # Concatenate grades into a single string for each student
    # if 'Grade' in requests_df.columns:
    #     grades_df = requests_df.groupby('[students]student_number')['Grade'].apply(
    #         lambda x: ', '.join(map(str, x))
    #     ).reset_index()
    #     grades_df.rename(columns={'Grade': 'All Grades'}, inplace=True)

    #     # Merge grades back using index
    #     pivot_df = pivot_df.merge(grades_df.set_index('[students]student_number'), 
    #                               left_index=True, right_index=True, how='left')
    #     print(f"Row count after adding grades: {len(pivot_df)}")

    if '[courses]Vocational' in requests_df.columns:
        vocational_df = requests_df.groupby('[students]student_number')['[courses]Vocational'].sum().reset_index()
        vocational_df.rename(columns={'[courses]Vocational': 'Vocational Count'}, inplace=True)  # Fix: Rename vocational_df, not grades_df
        # Merge vocational back using index
        pivot_df = pivot_df.merge(vocational_df.set_index('[students]student_number'), 
                                  left_index=True, right_index=True, how='left')
        print(f"Row count after adding vocational: {len(pivot_df)}")

    if "[schools]name" in requests_df.columns:
        vocational_df = requests_df.groupby('[students]student_number')["[schools]name"].apply(
            lambda x: ', '.join(set(map(str, x)))
        ).reset_index()
        vocational_df.rename(columns={"[schools]name": 'Schools Attended'}, inplace=True)
        # Merge vocational back using index
        pivot_df = pivot_df.merge(vocational_df.set_index('[students]student_number'), 
                                  left_index=True, right_index=True, how='left')
        print(f"Row count after adding Schools Attended: {len(pivot_df)}")    

    print("Pivoted table with concatenated grades")
    
    # Save to Excel
    # new_path = dest_folder / f"HS Courses Taken for {year}.xlsx"
    pivot_df.reset_index(inplace=True)

    pivot_df.drop_duplicates(subset=['[students]student_number'], inplace=True)
    pivot_df=validate_avid_file(pivot_df)
    pivot_df.drop(columns=["[schools]name"], inplace=True)
    return pivot_df
    # pivot_df.to_excel(new_path, index=False)  # Keep the hierarchical index

    # print("Saved dataframe to excel")
    # # Adjust column widths
    # adjust_column_widths(new_path)

    # # Open file
    # subprocess.run(["start", "excel", new_path], shell=True)

