import pandas as pd
import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Helpers.columns import adjust_column_widths
from task_manager import DataTaskManager
from Apps.course_pivoting_app import pivot_courses

manager = DataTaskManager()
store_folder = manager.return_folders()["avid_folder"]


def to_dataframe(file_path):
     df = pd.read_excel(file_path)
     return df
#paths
# lastyear_historical_grades_df = to_dataframe(store_folder / "23-24 Historical Grades.xlsx")
allhs_historical_grades = to_dataframe(store_folder / "All HS Historical Grades.xlsx")
# cte_courses = to_dataframe(store_folder / "CTE Courses.xlsx")
# cte_courses = cte_courses[["Course Number","Vocational"]]
whs_df = to_dataframe(store_folder / "23-24 WHS Historical Grades.xlsx")
wshs_df = to_dataframe(store_folder / "23-24 WSHS Historical Grades.xlsx")
ap_test = to_dataframe(store_folder / "23-24 AP Scores.xlsx")
# lastyear_hs_students = to_dataframe(store_folder / "All 23-24 HS Students.xlsx")
# current_hs_students = to_dataframe(store_folder / "All Current HS Students.xlsx")
def concatenate_dfs(df1, df2,name,store_folder):
    # Concatenate the two DataFrames
    concatenated_df = pd.concat([df1, df2], ignore_index=True)
    # create_final_excel(concatenated_df,name,store_folder)
    print(f"HS and WHS historical grades combined")
    return concatenated_df

def process_ap_scores(df):
    non_test_cols = ["Student Last Name","Student First Name","[students]student_number","Attending School Name","Grade Level"]
    df["tookAPTest"] = df.apply(lambda row: any(row[col] !='' for col in df.columns if col not in non_test_cols),  axis=1)
    df["passedAPTest"]= df.apply(lambda row: any(row[col] >2 for col in df.columns if col not in non_test_cols),  axis=1)
    df = df[["[students]student_number","tookAPTest","passedAPTest"]]
    print(f"Processed ap test scores")
    return df

def create_final_excel(df, file_name,folder):
    output_path = folder / f"{file_name}.xlsx"
    df.to_excel(output_path, index=False,sheet_name=file_name)
    adjust_column_widths(output_path)
    subprocess.run(["start", "excel", output_path], shell=True)


#merge historical grades with hs students to get current students
# final_df = pd.merge(lastyear_hs_students,lastyear_historical_grades,left_on="student_number",right_on="Student Number",how="outer")
# print(f"Historical grades merges with all hs students. Row count: {len(final_df)}")
# print(f"Unique students in historical grades: {len(final_df['Student Number'].unique())}")
# create_final_excel(final_df,"Intermeditate DF",store_folder)

#merge with cte courses to get which courses were cte courses
# final_df = pd.merge(lastyear_historical_grades, cte_courses, on="Course Number", how="left")
# print(f"Historical grades merges with cte courses. Row count: {len(final_df)}")
#process ap test scores to get the ap test scores and participation
# lastyear_historical_grades_df = concatenate_dfs(whs_df,wshs_df,"23-24 Historical Grades",store_folder)
ap_df = process_ap_scores(ap_test)
# final_df = pd.merge(lastyear_historical_grades_df, ap_df, on="[students]student_number",how="left")
#merge with ap test scores to get the ap test scores and participation

#pivot the courses to get the course names in the correct format and run analysis
# final_df = pivot_courses(lastyear_historical_grades_df)
final_df = pivot_courses(allhs_historical_grades)
final_df = pd.merge(final_df, ap_df, on="[students]student_number",how="left")
# print(f"Pivoted courses and ran AVID Analysis. Row count: {len(final_df)}")

# final_df = pd.merge(final_df, ap_df, on="Student Number", how="left")
# print(f"Pivoted df merges with ap test scores. Row count: {len(final_df)}")

# create_final_excel(final_df,"AVID Analysis",store_folder)




create_final_excel(final_df,"All HS AVID Analysis",store_folder)