import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Helpers.columns import adjust_column_widths
import subprocess
from Apps.fluency_composite_app import get_fluency_composite


def analyzer_kinder_data(
    fall_map_growth_path,
    winter_map_growth_path,
    fall_fluency_path,
    winter_fluency_path,
    quick_path,
    reading_level_path,
    mclass_path,
    dest_folder
):
    quick_df = pd.read_excel(quick_path)
    reading_level_df = pd.read_excel(reading_level_path)


    fall_growth_df = pd.read_excel(fall_map_growth_path)
    fall_growth_df = fall_growth_df[["StudentID", "TestRITScore", "AchievementQuintile"]]
    #can only use idxmax() with one column
    fall_idx = fall_growth_df.groupby("StudentID")["TestRITScore"].idxmax()
    fall_growth_df = fall_growth_df.loc[fall_idx]
    print("Reading Fall MAP Growth")

    winter_growth_df = pd.read_excel(winter_map_growth_path)
    print("Reading Winter MAP Growth")
    winter_growth_df = winter_growth_df[["StudentID", "TestRITScore", "FallToWinterGrowthQuintile"]]
    winter_growth_df.fillna("", inplace=True)
    winter_idx = winter_growth_df.groupby("StudentID")["TestRITScore"].idxmax()
    winter_growth_df = winter_growth_df.loc[winter_idx]

    fall_fluency_df = pd.read_excel(fall_fluency_path)
    print("Reading Fall MAP Fluency")
    fall_fluency_df = get_fluency_composite(fall_fluency_df, "Fall")
    winter_fluency_df = pd.read_excel(winter_fluency_path)
    print("Reading Winter MAP Fluency")
    winter_fluency_df = get_fluency_composite(winter_fluency_df, "Winter")
    boy_mclass_df = pd.read_excel(mclass_path,sheet_name="BOY")
    print("Reading BOY mClass")
    moy_mclass_df = pd.read_excel(mclass_path,sheet_name="MOY")
    print("Reading MOY mClass")


    print(winter_growth_df.head())
    kinder_reading_level_lookup = {
        -2: "NE",
        -1: "P.0",
        -0.9: "P.1",
        -0.8: "P.2",
        -0.7: "P.3",
        -0.6: "P.4",
        -0.5: "P.5",
        -0.4: "P.6",
        -0.3: "P.7",
        -0.2: "P.8",
        -0.1: "P.9"
    }

    def map_grade(grade):
        """Convert grade to its corresponding key in kinder_reading_level_lookup."""
        try:
            for key, value in kinder_reading_level_lookup.items():
                if value == grade or value == str(grade):
                    return key  # Return the corresponding key
            return grade  # If no match, keep the original value
        except ValueError:
            return grade  # Keep text values as they are

    # Get the unique quarters present in the Storecode column
    available_quarters = reading_level_df["Storecode"].unique().tolist()
    print(f"Available quarters: {available_quarters}")

    # Here you define the quarters you want to include
    quarters_to_include = ["Q1", "Q2"]  # Modify this list as needed

    # Filter the quarters to process based on the defined list
    quarters_to_process = [qtr for qtr in available_quarters if qtr in quarters_to_include]

    # If no quarters are selected, skip the processing step
    if not quarters_to_process:
        print("No valid quarters selected for processing.")
        return

    print(f"Processing the following quarters: {quarters_to_process}")

    # Apply grade mapping for each row to get corresponding quarter-level grades
    reading_level_df["Mapped Grade"] = reading_level_df["Grade"].apply(map_grade)

    # Now, we will pivot the data for each quarter selected
    # We first create a list to hold the new columns for each selected quarter
    pivoted_df = reading_level_df.copy()

    for quarter in quarters_to_process:
        quarter_column = f"{quarter} Reading Levels"
        # Filter the rows for each quarter and create a new column with the mapped grade
        quarter_data = pivoted_df[pivoted_df["Storecode"] == quarter]
        pivoted_df[quarter_column] = quarter_data["Mapped Grade"]

    # Drop the columns that are not needed anymore (like the original Storecode, Grade, and Mapped Grade)
    final_df = pivoted_df.drop(columns=["Grade", "Mapped Grade"])

    # Pivot the table so that the students are the rows, and each quarter becomes its own column
    final_df = final_df.pivot_table(
        index="Student Number",  # Rows will be students
        columns="Storecode",      # Columns will be quarters (Q1, Q2)
        values=[f"{qtr} Reading Levels" for qtr in quarters_to_process],
        aggfunc="first"           # In case of duplicates, pick the first value
    )

    # Flatten the columns for better readability
    final_df.columns = [f"{qtr}" for qtr in final_df.columns.get_level_values(0)]
    try:
          final_df = final_df.merge(quick_df,"outer",left_on="Student Number",right_on="student_number")
    except KeyError:
        return KeyError
    
    preschool_list = ["OCDC","Little Lambs","Community Head Start","Headstart","Cipriano"]
    final_df['InPreschool?'] = final_df.apply(
     lambda row: "yes" if 
                    ('pre' in str(row['U_StudentsUserFields.PRESCHOOL']).lower() or 
                    'pre' in str(row['U_StudentsUserFields.PREVIOUS_SCHL']).lower() or
                    row['U_StudentsUserFields.PRESCHOOL'] in preschool_list or 
                    row['U_StudentsUserFields.PREVIOUS_SCHL'] in preschool_list) 
                    else "no", axis=1
     )
    print(final_df.columns)
    
    fall_growth_df.rename()
    map_df = fall_growth_df.merge(winter_growth_df,"left",on="StudentID")
    fluency_df = fall_fluency_df.merge(winter_fluency_df,"left",on="StudentID")
    mclass_df = boy_mclass_df.merge(moy_mclass_df,"left",on="student_number")

    final_df = final_df.merge(map_df,"left",left_on="student_number",right_on="StudentID")
    final_df = final_df.merge(fluency_df,"left",left_on="student_number",right_on="StudentID")
    final_df = final_df.merge(mclass_df,"left",on="student_number")

    final_df = final_df[['student_number','Last_Name','First_Name','Grade_Level',
       '[schools]name', 'Home_Room', 'U_StudentsUserFields.PREVIOUS_SCHL',
       'U_StudentsUserFields.PRESCHOOL', 'Q1 Reading Levels', 'Q2 Reading Levels','InPreschool?',"AchievementQuintile",
       "FallToWinterGrowthQuintile","Fall MapFluencyCompositeScore","Winter MapFluencyCompositeScore",
       "BOY Composite Level","BOY Composite Score","MOY Composite Level","MOY Composite Score"]]
    #,"AchievementQuintile","FallToWinterGrowthQuintile"
    # Save the final output
    output_path = os.path.join(dest_folder, "Kinder Final Output.xlsx")
    final_df.to_excel(output_path, index=False)

    # Adjust column widths and open file
    adjust_column_widths(output_path)
    subprocess.run(["start", "excel", output_path], shell=True)
