import pandas as pd
from openpyxl import load_workbook
from columns import adjust_column_widths
from config import class_size_excluded
from task_manager import DataTaskManager
from datetime import date
import calendar
import os
from pathlib import Path

manager = DataTaskManager()

def analyze_class_sizes(classes_df,iui_df, quarter, semester, school_year,dest_folder):
    current_month = calendar.month_name[date.today().month]
    year = date.today().year
    output_file_path = dest_folder / f"Teacher Assignment Report for {year}.xlsx"

    # classes_df = pd.read_excel(input_file)

    schools = classes_df["School Abbr"].unique().tolist()
    print(schools)

    headers = ["Teacher Last, First","Course Name", "Course Number", "Term Abbr", "School Abbr","Expression"]

    classes_df = classes_df[classes_df["Expression"] != "-"]
    classes_df = classes_df.groupby(headers).size().reset_index(name="Student Count")
    classes_df = classes_df[~classes_df["Course Name"].isin(class_size_excluded)]
    print("Students counted by class")

    nces_df = pd.merge(iui_df,classes_df,left_on="SchlCrsID",right_on="Course Number",how="right")
    new_headers = ["Teacher Last, First","Course Name", "Course Number","CrsCd","Term Abbr", "School Abbr","Expression"]
    nces_df = nces_df[new_headers]
    # Rename columns for clarity
    nces_df.rename(columns={"Teacher Last, First": "Teacher Name", "Term Abbr": "Term","CrsCd":"NCES Code"}, inplace=True)
    print("Columns renamed")

    def should_include_row(row):
        term = str(row['Term']).strip()  # Ensure term is a string and remove extra whitespace
        if 'Q' in term:
            return f"Q{quarter}" in term
        elif 'S' in term:
            return f"S{semester}" in term
        else:
            return school_year in term

    with pd.ExcelWriter(output_file_path) as writer:
        for school in schools:
            if "ES" in school or school == "NME":
                school_df = nces_df[
                    (nces_df["School Abbr"] == school)
                    & (nces_df["Course Name"].str.contains("Plus|Two-Way", case=False, regex=True) |
                        nces_df["Course Name"].isin(["Music", "Art", "Library", "Wellness/PE"]))
                ]
            else:
                school_df = nces_df[nces_df["School Abbr"] == school]
                
                # Apply the function to each row to filter the DataFrame
                # school_df = school_df[school_df.apply(should_include_row, axis=1)]
                # print(f"DataFrame shape after filtering for {school}: {school_df.shape}")

            # Drop unnecessary columns
            # school_df.drop(["School Abbr", "Term"], axis=1, inplace=True)

            # Write each school’s data to a separate sheet
            # when sorting, need to assign it back to the school_df variable
            school_df = school_df.sort_values(by=["Teacher Name","Course Name"])
            # school_df.drop(columns=["Student Count","SchlCrsID"],inplace=True)
            school_df.to_excel(writer, sheet_name=f"{school}-{current_month}", index=False)
            print(f"Data written for school: {school}")

    print("Class data sorted by schools")

    # Adjust column widths
    try:
        adjust_column_widths(output_file_path)
        print("Column widths adjusted")
    except Exception as e:
        print(f"Error adjusting column widths: {e}")

    print(output_file_path)
    os.system(f'start EXCEL.EXE "{output_file_path}"')
    return output_file_path

# powerschool_folder = Path(manager.get_folders("Audit Class Size")["powerschool_folder"])
# print(powerschool_folder)
# primary_file = powerschool_folder / "student_class_enrollments - primary.xlsx"
# secondary_file = powerschool_folder /  "student_class_enrollments - secondary.xlsx"
# file_list = [primary_file,secondary_file]
# iuid_file = powerschool_folder / "24-25 IUIDs.xlsx"
# analyze_class_sizes(file_to_analyze,1,1,"24-25")

def generate_class_size_lists(primary_file,secondary_file,iuid_file,dest_folder):
    files = [primary_file,secondary_file]
    final_df = pd.concat([pd.read_excel(file) for file in files],ignore_index=True)
    iuid_df = pd.read_excel(iuid_file)
    selected_iuid_df = iuid_df[["SchlCrsID","CrsCd"]].drop_duplicates()
    # nces_df = pd.merge(selected_iuid_df,final_df,left_on="SchlCrsID",right_on="Course Number",how="right")
    analyze_class_sizes(final_df,selected_iuid_df,1,1,"24-25",dest_folder)
