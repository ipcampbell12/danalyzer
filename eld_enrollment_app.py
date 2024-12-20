import pandas as pd
import os
import calendar
from columns import adjust_column_widths
import subprocess
from datetime import date


def validate_eld_enrollment(el_students_path,eld_classes_path,processed_eld_enrollment_folder):
    # el_students_path = powerschool_folder /"12-16 EL Students.xlsx"
    # eld_classes_path = powerschool_folder /"12-16 ELD Classes.xlsx"
    current_date = pd.Timestamp('today')
    current_month = calendar.month_name[current_date.today().month]
    current_year = current_date.today().year

    el_students_df = pd.read_excel(el_students_path)
    print(el_students_df.columns)
    eld_classes_df= pd.read_excel(eld_classes_path)
    print(eld_classes_df.columns)
    el_students_df = el_students_df[~el_students_df['SchoolID'].isin([95,4230])]
    eld_classes_df = eld_classes_df.rename(columns={"Student Number":"student_number"})
    final_df = el_students_df.merge(eld_classes_df,how="left",on="student_number")
    final_df = final_df[['student_number','Course Name','Student Last, First','Grade_Level','SchoolID']]
    print(final_df.columns)
    final_df["hasELDClass"] = final_df["Course Name"].apply(
        lambda x: "No" if pd.isna(x) or x.strip() == "" else "Yes"
    )
    print(final_df.columns)
    concern_df = final_df[final_df["hasELDClass"] =="No"]
    pivot_eld = (
        final_df.groupby(['SchoolID', 'hasELDClass'])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # pivot_grade_levels = final_df.groupby(['Grade Level', "isDeficient"]).size().unstack(fill_value=0).reset_index()
    final_path = processed_eld_enrollment_folder / f"f{current_month}, {current_year} ELD Enrollment Audit.xlsx"


    with pd.ExcelWriter(final_path, engine='openpyxl') as writer:
    # Save the resulting DataFrame to an Excel file
        concern_df.to_excel(writer, sheet_name="Missing ELD", index=False, startrow=0)
        pivot_eld.to_excel(writer, sheet_name="Summary", index=False, startrow=0)
        final_df.to_excel(writer, sheet_name="All ELs", index=False, startrow=0)
        
        
    adjust_column_widths(final_path)
    subprocess.run(["start", "excel", final_path], shell=True)
